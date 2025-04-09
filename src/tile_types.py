import color
from const import *

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
        ("tileid", int),
        ("walkable", bool),  # True if this tile can be walked over.
        ("transparent", bool),  # True if this tile doesn't block FOV.
        ("not_obscuring", bool),  # False if this tile partially blocks FOV
        ("fall_through", bool),  
        ("light", graphic_dt),  # Graphics for when the tile is in FOV and lit up.
        ("obscured", graphic_dt),  # partially obscured, lighter than dark, darker than light
        ("dark", graphic_dt),  # not lit up but in view
        ("deep", graphic_dt),  # memory (darkest)
    ]
)


def new_tile(
    *,  # Enforce the use of keywords, (so that parameter order doesn't matter -- but it still does...)
    tileid: int,
    walkable: bool,
    transparent: bool,
    not_obscuring: bool,
    fall_through: bool,
    light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    obscured: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    deep: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile types """
    return np.array(
        (tileid, walkable, transparent, not_obscuring, fall_through, light, obscured, dark, deep),
        dtype=tile_dt)


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

# stairways/ chasms
chasm = new_tile(
    tileid=CHASM,
    walkable=False,
    transparent=True,
    not_obscuring=True,
    fall_through=True,
    light=(181, color.deepgray, color.black),
    obscured=(181, color.deepgray, color.black),
    dark=(181, color.deepgray, color.black),
    deep=(181, color.deepgray, color.black),
)
down_stairs = new_tile(
    tileid=DOWN_STAIRCASE,
    walkable=True,
    transparent=True,
    not_obscuring=True,
    fall_through=False,
    light=(ord(">")+256, color.black, color.magenta),
    obscured=(ord(">")+256, color.black, color.dkmagenta),
    dark=(ord(">")+256, color.black, color.dkmagenta),
    deep=(ord(">")+256, color.black, color.deepmagenta),
)
up_stairs = new_tile(
    tileid=UP_STAIRCASE,
    walkable=True,
    transparent=False,
    not_obscuring=True,
    fall_through=False,
    light=(ord("<")+256, color.black, color.magenta),
    obscured=(ord("<")+256, color.black, color.dkmagenta),
    dark=(ord("<")+256, color.black, color.dkmagenta),
    deep=(ord("<")+256, color.black, color.deepmagenta),
)
down_ladder = new_tile(
    tileid=DOWN_LADDER,
    walkable=True,
    transparent=True,
    not_obscuring=True,
    fall_through=False,
    light=(198, color.black, color.magenta),
    obscured=(198, color.black, color.dkmagenta),
    dark=(198, color.black, color.dkmagenta),
    deep=(198, color.black, color.deepmagenta),
)
up_ladder = new_tile(
    tileid=UP_LADDER,
    walkable=True,
    transparent=False,
    not_obscuring=True,
    fall_through=False,
    light=(199, color.black, color.magenta),
    obscured=(199, color.black, color.dkmagenta),
    dark=(199, color.black, color.dkmagenta),
    deep=(199, color.black, color.deepmagenta),
)

# floors
concrete_highway = new_tile(
    tileid=WHITE_FLOOR,
    walkable=True,
    transparent=True,
    not_obscuring=True,
    fall_through=False,
    light=(179, color.neutralgray, color.deepgray),
    obscured=(179, color.hazy, color.black),
    dark=(179, color.hazy, color.black),
    deep=(179, color.deepgray, color.black),
)
wood_floor = new_tile(
    tileid=WOOD_FLOOR,
    walkable=True,
    transparent=True,
    not_obscuring=True,
    fall_through=False,
    light=(207, color.deepgray, color.dkbrown),
    obscured=(207, color.hazy, color.black),
    dark=(207, color.hazy, color.black),
    deep=(207, color.deepgray, color.black),
)
concrete_floor = new_tile(
    tileid=WHITE_FLOOR,
    walkable=True,
    transparent=True,
    not_obscuring=True,
    fall_through=False,
    light=(249, color.neutralgray, color.deepgray),
    obscured=(249, color.hazy, color.black),
    dark=(249, color.hazy, color.black),
    deep=(249, color.deepgray, color.black),
)
regal_floor = new_tile(
    tileid=WHITE_FLOOR, # update this
    walkable=True,
    transparent=True,
    not_obscuring=True,
    fall_through=False,
    light=(249, color.neutralgray, color.navy),
    obscured=(249, color.hazy, color.black),
    dark=(249, color.hazy, color.black),
    deep=(249, color.navy, color.black),
)
brown_floor = new_tile(
    tileid=DIRTY_FLOOR,
    walkable=True,
    transparent=True,
    not_obscuring=True,
    fall_through=False,
    light=(249, color.neutral, color.deep),
    obscured=(290, color.mauve, color.deepmauve),
    dark=(290, color.mauve, color.deepmauve),
    deep=(32, color.vdkblue, color.black),
)

# walls
concrete_wall = new_tile(
    tileid=WHITE_WALL,
    walkable=False,
    transparent=False,
    not_obscuring=False,
    fall_through=False,
    light=(222, color.white, color.offwhite),
    obscured=(222, color.vdkgray, color.vdkgray),
    dark=(222, color.vdkgray, color.vdkgray),
    deep=(222, color.deepgray, color.deepgray),
)
blue_wall = new_tile(
    tileid=WHITE_WALL,
    walkable=False,
    transparent=False,
    not_obscuring=False,
    fall_through=False,
    light=(221, color.offwhite, color.ltblue),
    obscured=(221, color.navy, color.navy),
    dark=(221, color.navy, color.navy),
    deep=(221, color.deepgray, color.deepgray),
)
wood_wall = new_tile(
    tileid=WOOD_WALL,
    walkable=False,
    transparent=False,
    not_obscuring=False,
    fall_through=False,
    light=(207, color.brown, color.dkbrown),
    obscured=(207, color.hazybrown, color.hazybrown),
    dark=(207, color.hazybrown, color.hazybrown),
    deep=(207, color.deepgray, color.deepgray),
)
brown_wall = new_tile(
    tileid=DIRTY_WALL,
    walkable=False,
    transparent=False,
    not_obscuring=False,
    fall_through=False,
    light=(290, color.bone, color.ltbrown),
    obscured=(290, color.hazy, color.hazy),
    dark=(290, color.hazy, color.hazy),
    deep=(290, color.deepgray, color.deepgray),
)
red_wall = new_tile(
    tileid=RUSTED_WALL,
    walkable=False,
    transparent=False,
    not_obscuring=False,
    fall_through=False,
    light=(205, color.rust, color.darkrust),
    obscured=(205, color.hazyred, color.hazyred),
    dark=(205, color.hazyred, color.hazyred),
    deep=(205, color.deepgray, color.deepgray),
)
