import color

from typing import Tuple

import numpy as np  # type: ignore

# Tile graphics structured type compatible with Console.tiles_rgb.
graphic_dt = np.dtype(
    [
        ("ch", np.int32),  # Unicode codepoint.
        ("fg", "3B"),  # 3 unsigned bytes, for RGB colors.
        ("bg", "3B"),
    ]
)

# Tile struct used for statically defined tile data.
tile_dt = np.dtype(
    [
        ("walkable", bool),  # True if this tile can be walked over.
        ("transparent", bool),  # True if this tile doesn't block FOV.
        ("not_obscuring", bool),  # False if this tile partially blocks FOV
        ("light", graphic_dt),  # Graphics for when the tile is in FOV and lit up.
        ("obscured", graphic_dt),  # partially obscured, lighter than dark, darker than light
        ("dark", graphic_dt),  # not lit up but in view
        ("deep", graphic_dt),  # memory (darkest)
    ]
)


def new_tile(
    *,  # Enforce the use of keywords, so that parameter order doesn't matter.
    walkable: int,
    transparent: int,
    not_obscuring: int,
    light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    obscured: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    deep: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile types """
    return np.array((walkable, transparent, not_obscuring, light, obscured, dark, deep), dtype=tile_dt)


# SHROUD represents unexplored, unseen tiles
SHROUD = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)

# floor tile / open air
#   transparent=True,
#   not_obscuring=True,
# wall tile / dark glass (blocking light)
#   transparent=False,
#   not_obscuring=False,
# partial light blocker (up staircase, foggy glass, a column, etc.)
#   transparent=False,
#   not_obscuring=True,

white_floor = new_tile(
    walkable=True,
    transparent=True,
    not_obscuring=True,
    light=(249, color.neutralgray, color.navy),
    obscured=(290, color.navy, color.navy),
    dark=(290, color.black, color.black),
    deep=(32, color.black, color.black),
)
brown_floor = new_tile(
    walkable=True,
    transparent=True,
    not_obscuring=True,
    light=(249, color.neutral, color.deep),
    obscured=(290, color.deep, color.deep),
    dark=(290, color.mauve, color.deepmauve),
    deep=(32, color.vdkblue, color.black),
)
white_wall = new_tile(
    walkable=False,
    transparent=False,
    not_obscuring=False,
    light=(290, color.white, color.offwhite),
    obscured=(290, color.ltblue, color.ltblue),
    dark=(290, color.dkblue, color.dkblue),
    deep=(290, color.navy, color.navy),
)
brown_wall = new_tile(
    walkable=False,
    transparent=False,
    not_obscuring=False,
    light=(290, color.bone, color.ltbrown),
    obscured=(290, color.brown, color.brown),
    dark=(290, color.hazy, color.hazy),
    deep=(290, color.deepbrown, color.deepbrown),
)
red_wall = new_tile(
    walkable=False,
    transparent=False,
    not_obscuring=False,
    light=(290, color.dkred, color.red),
    obscured=(290, color.dkred, color.dkred),
    dark=(290, color.hazy, color.hazy),
    deep=(290, color.deepred, color.deepred),
)
down_stairs = new_tile(
    walkable=True,
    transparent=True,
    not_obscuring=True,
    light=(ord(">")+256, color.black, color.magenta),
    obscured=(290, color.magenta, color.magenta),
    dark=(290, color.deepmagenta, color.deepmagenta),
    deep=(ord(">")+256, color.black, color.deepmagenta),
)
up_stairs = new_tile(
    walkable=True,
    transparent=False,
    not_obscuring=True,
    light=(ord("<")+256, color.black, color.magenta),
    obscured=(290, color.magenta, color.magenta),
    dark=(290, color.deepmagenta, color.deepmagenta),
    deep=(ord("<")+256, color.black, color.deepmagenta),
)
