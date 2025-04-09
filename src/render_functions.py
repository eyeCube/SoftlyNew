from __future__ import annotations

from typing import Tuple, TYPE_CHECKING
import math

import color

if TYPE_CHECKING:
    from tcod import Console
    from engine import Engine
    from game_map import GameMap


def get_names_at_location(x: int, y: int, game_map: GameMap) -> str:
    if not game_map.in_bounds(x, y):
        return [""]

    if not game_map.visible[x, y]:
        return ["<out of sight>"]

    if not game_map.lit_tiles[x, y]:
        return ["<obscured but visible>"]

    def func(en):
        return en.value
    entities = sorted([entity for entity in game_map.entities if entity.x == x and entity.y == y], key=func, reverse=True)
    names = [en.name for en in entities]

    return names
def render_names_at_mouse_location(
    console: Console, x: int, y: int, engine: Engine
) -> None:
    mouse_x, mouse_y = engine.mouse_location

    names_at_mouse_location = get_names_at_location(
        x=mouse_x, y=mouse_y, game_map=engine.game_map
    )
    ln = len(names_at_mouse_location)
    if ln > 0:
        name = names_at_mouse_location[0]
        _and = f" and {ln - 1} others" if ln >= 2 else ""
    else:
        name = _and = ""

    d = round(math.sqrt((mouse_x-engine.player.x)**2 + (mouse_y-engine.player.y)**2))
    console.print(x=x, y=y, string=f"{d}m: {name}{_and}")


def render_bar(
    console: Console, current_value: int, maximum_value: int, total_width: int
) -> None:
    bar_width = int(float(current_value) / maximum_value * total_width)

    console.draw_rect(x=0, y=45, width=20, height=1, ch=32, bg=color.bar_empty)

    if bar_width > 0:
        console.draw_rect(
            x=0, y=45, width=bar_width, height=1, ch=32, bg=color.bar_filled
        )

    console.print(
        x=1, y=45, string=f"HP: {current_value}/{maximum_value}", fg=color.bar_text
    )


def render_dungeon_level(
    console: Console, dungeon_level: int, location: Tuple[int, int]
) -> None:
    """
    Render the level the player is currently on, at the given location.
    """
    x, y = location

    console.print(x=x, y=y, string=f"Dungeon level: {dungeon_level}")

