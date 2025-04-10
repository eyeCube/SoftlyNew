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
import tile_types

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap, GameWorld


class Engine:
    game_map: GameMap
    game_world: GameWorld

    def __init__(self, player: Actor):
        self.coming_from = -1 # -1 is from above, 1 from below
        self.message_log = MessageLog()
        self.mouse_location = (0, 0)
        self.player = player
        random.seed(time.time())
        self.world_seed = int(random.random()*1000000)
        self.world_location = [40,0] # x, y
        self.explored_zones = {} # world location (x,y,) : map starting seed location (x,y,)

    def save_dungeon(self):
        """Save this Engine instance as a compressed file."""
        filename = "../sav/wd_{},{}.sav".format(self.world_location[0], self.world_location[1])
        print("saving zone: ({}, {})".format(self.world_location[0], self.world_location[1]))
        self.game_map.engine = None
        _entities = self.game_map.entities
        self.game_map.entities = set()
        save_data = lzma.compress(pickle.dumps(self.game_map))
        with open(filename, "wb") as f:
            f.write(save_data)
        self.game_map.engine = self
        self.game_map.entities = _entities
    def load_dungeon(self):
        filename = "../sav/wd_{},{}.sav".format(self.world_location[0], self.world_location[1])
        print("loading zone: ({}, {})".format(self.world_location[0], self.world_location[1]))
        with open(filename, "rb") as f:
            self.game_map = pickle.loads(lzma.decompress(f.read()))
        self.game_map.engine = self
        self.game_map.entities = set([self.player])
        # load in new set of entities based on what the player has done on this floor

    def descend(self, new_stairs=True, reposition=None):
        self.coming_from = -1
        # save
        self.save_dungeon()
        # change floors
        self.world_location = [self.world_location[0], self.world_location[1] + 1]
        # load or generate new
        if (self.world_location[0],self.world_location[1]) in self.explored_zones:
            self.load_dungeon()
        else:
            self.game_world.generate_floor()

        print("location: ", self.world_location)
        
        if reposition:
            self.player.place(reposition[0], reposition[1], self.game_map)

        self.message_log.add_message(
            "You descend the staircase.", color.descend
        )

        if (new_stairs and self.coming_from == -1 and (self.game_map.tiles[self.player.x, self.player.y]['stairs_up'] == False)):
            self.message_log.add_message(
                "You've unlocked a new ascending staircase on this level.", color.descend
            )
            self.game_map.tiles[self.player.x, self.player.y] = tile_types.up_stairs
            
    def ascend(self, new_stairs=True):
        self.coming_from = 1
        # save
        self.save_dungeon()
        # change floors
        self.world_location = [self.world_location[0], self.world_location[1] - 1]
        # load or generate new
        if (self.world_location[0],self.world_location[1]) in self.explored_zones:
            self.load_dungeon()
        else:
            self.game_world.generate_floor()
        print("location: ", self.world_location)
        self.message_log.add_message(
            "You ascend the staircase.", color.ascend
        )

        if (new_stairs and self.coming_from == -1 and (self.game_map.tiles[self.player.x, self.player.y]['stairs_down'] == False)):
            self.message_log.add_message(
                "You've unlocked a new descending staircase on this level.", color.descend
            )
            self.game_map.tiles[self.player.x, self.player.y] = tile_types.down_stairs


    def handle_ai_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                try:
                    entity.ai.perform()
                except exceptions.Impossible:
                    pass  # Ignore impossible action exceptions from AI.

    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view."""
        
        def _circ(vismap, lgt, actor): # make FOV area into a circle shape
            x, y = np.indices(vismap.shape)
            distance = np.sqrt((x - actor.x)**2 + (y - actor.y)**2)
            return (vismap & (distance <= lgt))

        # compute player's FOV
        # vision level is affected by the player's light radius
        lgt_bonus = 10 if self.world_location[1] == 0 else 0
        rad = int(min(max(self.player.fighter.vision*0.1, (self.player.fighter.light + lgt_bonus)*2), self.player.fighter.vision))
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=rad,
        )
        self.game_map.visible = _circ(self.game_map.visible, rad, self.player)
        # compute player's FOV for things that are obscured
        self.game_map.obscured_but_visible[:] = compute_fov(
            self.game_map.tiles["not_obscuring"],
            (self.player.x, self.player.y),
            radius=self.player.fighter.vision,
        )
        self.game_map.obscured_but_visible = _circ(self.game_map.obscured_but_visible, rad, self.player)
        self.game_map.obscured_but_visible = np.logical_and(self.game_map.obscured_but_visible, np.logical_not(self.game_map.visible))

        # calculate the light grid
        self.game_map.remove_all_light()
        for actor in self.game_map.actors:
            if actor.fighter.light <= 0:
                continue
            if not self.game_map.in_bounds(actor.x, actor.y):
                continue
            lighthere = compute_fov(
                self.game_map.tiles["transparent"],
                (actor.x, actor.y),
                radius=actor.fighter.light + lgt_bonus,
            )
            lighthere = _circ(lighthere, actor.fighter.light + lgt_bonus, actor)
            self.game_map.lit_tiles[:] |= lighthere
        # Update the set of tiles that the player can see clearly, and the set of "explored" tiles
        self.game_map.get_lit_and_visible()
        self.game_map.add_explored()

    def render(self, console: Console) -> None:
        self.game_map.render(console)

        self.message_log.render(console=console, x=21, y=43, width=60, height=5)

        render_functions.render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=18,
        )

        render_functions.render_dungeon_level(
            console=console,
            dungeon_level=self.world_location[1],
            location=(0, 43),
        )

        render_functions.render_names_at_mouse_location(
            console=console, x=21, y=41, engine=self
        )

    def save_as(self, filename: str) -> None:
        """Save this Engine instance as a compressed file."""
        save_data = lzma.compress(pickle.dumps(self))
        with open(filename, "wb") as f:
            f.write(save_data)
