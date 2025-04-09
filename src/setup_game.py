"""Handle the loading and initialization of game sessions."""
from __future__ import annotations

import copy
import lzma
import pickle
import traceback
from typing import Optional

import tcod
from tcod import libtcodpy

import color
from engine import Engine
import entity_factories
from game_map import GameWorld
import input_handlers
from const import *


# Load the background image and remove the alpha channel.
background_image = tcod.image.load("../img/softly-main-menu.png")[:, :, :3]


def new_game() -> Engine:
    """Return a brand new game session as an Engine instance."""
    map_width = 80
    map_height = 41

    player = copy.deepcopy(entity_factories.player)

    engine = Engine(player=player)

    engine.game_world = GameWorld(
        engine=engine,
        map_width=map_width,
        map_height=map_height,
    )

    engine.game_world.generate_floor()
    engine.update_fov()

    engine.message_log.add_message(
        f"{engine.player.name} enters the town of Ka'tyyk", color.welcome_text
    )

    dagger = copy.deepcopy(entity_factories.weapons[CLASS_DAGGERS][MAT_METAL])
    dagger.parent = player.inventory
    player.inventory.items.append(dagger)
    player.equipment.toggle_equip(dagger, add_message=False)
    
    armor = copy.deepcopy(entity_factories.gambeson)
    armor.parent = player.inventory
    player.inventory.items.append(armor)
    player.equipment.toggle_equip(armor, add_message=False)
    
    torch = copy.deepcopy(entity_factories.torch)
    torch.parent = player.inventory
    player.inventory.items.append(torch)
    player.equipment.toggle_equip(torch, add_message=False, offhand=True)

    player.fighter.hp = player.fighter.max_hp
    
    engine.player_x = -1
    engine.player_y = -1
    
    engine.update_fov()

    return engine


def load_game(filename: str) -> Engine:
    """Load an Engine instance from a file."""
    with open(filename, "rb") as f:
        engine = pickle.loads(lzma.decompress(f.read()))
    assert isinstance(engine, Engine)
    return engine


class MainMenu(input_handlers.BaseEventHandler):
    """Handle the main menu rendering and input."""

    def on_render(self, console: tcod.Console) -> None:
        """Render the main menu on a background image."""
        console.draw_semigraphics(background_image, 0, 0)

        xs = console.width // 2
        ys = console.height // 2
        
        '''console.print(
            xs,
            ys,
            "S O F T L Y  I N T O  T H E  N I G H T",
            fg=color.menu_title,
            alignment=libtcodpy.CENTER,
        )'''
        console.print(
            xs,
            ys + 4,
            "eyeCube Productions",
            fg=color.menu_title,
            alignment=libtcodpy.CENTER,
        )

        menu_width = 24
        for i, text in enumerate(
            ["[N] Play a new game", "[C] Continue last game", "[Q] Quit"]
        ):
            console.print(
                xs,
                ys + 8 + i,
                text.ljust(menu_width),
                fg=color.menu_text,
                bg=color.black,
                alignment=libtcodpy.CENTER,
                bg_blend=libtcodpy.BKGND_ALPHA(64),
            )

    def ev_keydown(
        self, event: tcod.event.KeyDown
    ) -> Optional[input_handlers.BaseEventHandler]:
        if event.sym in (tcod.event.KeySym.q, tcod.event.KeySym.ESCAPE):
            raise SystemExit()
        elif event.sym == tcod.event.KeySym.c:
            try:
                return input_handlers.MainGameEventHandler(load_game("../sav/game.sav"))
            except FileNotFoundError:
                return input_handlers.PopupMessage(self, "No saved game to load.")
            except Exception as exc:
                traceback.print_exc()  # Print to stderr.
                return input_handlers.PopupMessage(self, f"Failed to load save:\n{exc}")
        elif event.sym == tcod.event.KeySym.n:
            return input_handlers.MainGameEventHandler(new_game())

        return None
