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
        ("deep", graphic_dt),  # Graphics for when the tile is in FOV but obscured.
        ("dark", graphic_dt),  # Graphics for when this tile is not in FOV.
        ("light", graphic_dt),  # Graphics for when the tile is in FOV and lit up.
    ]
)


def new_tile(
    *,  # Enforce the use of keywords, so that parameter order doesn't matter.
    walkable: int,
    transparent: int,
    deep: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile types """
    return np.array((walkable, transparent, deep, dark, light), dtype=tile_dt)


# SHROUD represents unexplored, unseen tiles
SHROUD = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)

white_floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(290, color.black, color.black),
    deep=(32, color.black, color.black),
    light=(249, color.neutralgray, color.navy),
)
brown_floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(290, color.mauve, color.deepmauve),
    deep=(32, color.vdkblue, color.black),
    light=(249, color.neutral, color.deep),
)
white_wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(290, color.navy, color.navy),
    deep=(290, color.dkblue, color.dkblue),
    light=(290, color.white, color.offwhite),
)
brown_wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(290, color.hazy, color.hazy),
    deep=(290, color.dkblue, color.dkblue),
    light=(290, color.bone, color.ltbrown),
)
red_wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(290, color.hazy, color.hazy),
    deep=(290, color.dkblue, color.dkblue),
    light=(290, color.dkred, color.red),
)
down_stairs = new_tile(
    walkable=True,
    transparent=True,
    dark=(290, color.deepmagenta, color.deepmagenta),
    deep=(ord(">")+256, color.black, color.deepmagenta),
    light=(ord(">")+256, color.black, color.magenta),
)
