from __future__ import annotations

import numpy as np
import color
import random
import time
import lzma
import pickle
from typing import TYPE_CHECKING

from tcod.console import Console
from tcod.map import compute_fov

import exceptions
from message_log import MessageLog
import render_functions

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap, GameWorld


class Engine:
    game_map: GameMap
    game_world: GameWorld

    def __init__(self, player: Actor):
        self.message_log = MessageLog()
        self.mouse_location = (0, 0)
        self.player = player
        random.seed(time.time())
        self.world_seed = int(random.random()*1000)
        self.world_location = [40,0] # x, y

    def descend(self):
        self.game_world.current_floor += 1
        self.world_location = [self.world_location[0], self.game_world.current_floor]
        self.game_world.generate_floor()
        self.message_log.add_message(
            "You descend the staircase.", color.descend
        )

    def handle_ai_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                try:
                    entity.ai.perform()
                except exceptions.Impossible:
                    pass  # Ignore impossible action exceptions from AI.

    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view."""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=int(min(max(self.player.fighter.vision*0.1, self.player.fighter.light*2), self.player.fighter.vision)),
        )
        x, y = np.indices(self.game_map.visible.shape)
        distance = np.sqrt((x - self.player.x)**2 + (y - self.player.y)**2)
        self.game_map.visible = (self.game_map.visible & (distance <= self.player.fighter.vision))
        self.game_map.remove_all_light()
        for actor in self.game_map.actors:
            if actor.fighter.light <= 0:
                continue
            lighthere = compute_fov(
                self.game_map.tiles["transparent"],
                (actor.x, actor.y),
                radius=actor.fighter.light,
            )
            x, y = np.indices(lighthere.shape)
            distance = np.sqrt((x - actor.x)**2 + (y - actor.y)**2)
            lighthere = (lighthere & (distance <= actor.fighter.light))
            self.game_map.lit_tiles[:] |= lighthere
        # If a tile is "visible" it should be added to "explored".
        self.game_map.get_lit_and_visible()
        self.game_map.add_explored()

    def render(self, console: Console) -> None:
        self.game_map.render(console)

        self.message_log.render(console=console, x=21, y=45, width=60, height=5)

        render_functions.render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=20,
        )

        render_functions.render_dungeon_level(
            console=console,
            dungeon_level=self.game_world.current_floor,
            location=(0, 47),
        )

        render_functions.render_names_at_mouse_location(
            console=console, x=21, y=44, engine=self
        )

    def save_as(self, filename: str) -> None:
        """Save this Engine instance as a compressed file."""
        save_data = lzma.compress(pickle.dumps(self))
        with open(filename, "wb") as f:
            f.write(save_data)
