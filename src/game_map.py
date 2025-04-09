from __future__ import annotations

from typing import Iterable, Iterator, Optional, TYPE_CHECKING

import numpy as np  # type: ignore
from tcod.console import Console
from tcod import libtcodpy

from const import *
import color
from entity import Actor, Item
import tile_types

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


class GameMap:
    def __init__(
        self, engine: Engine, width: int, height: int, entities: Iterable[Entity] = (),
        default_fill: tile_types.tile_dt = tile_types.concrete_wall
    ):
        self.engine = engine
        self.width, self.height = width, height
        self.entities = set(entities)
            # tiles: what is actually there in the game world
        self.tiles = np.full((width, height), fill_value=default_fill, dtype=tile_types.tile_dt)
            # tiles_memory: what the player remembers seeing / what is currently displayed
        self.tiles_memory = np.full((width, height), fill_value=default_fill, dtype=tile_types.tile_dt)
        
        self.lit_tiles = np.full(  # Tiles lit up by light sources
            (width, height), fill_value=False, dtype=bool
        )
        self.obscured_but_visible = np.full(  # Tiles the player can currently see but which are obscured partially by an obstacle
            (width, height), fill_value=False, dtype=bool
        )
        self.lit_and_visible = np.full(  # Tiles the player can currently see
            (width, height), fill_value=False, dtype=bool
        )
        self.visible = np.full(  # Tiles the player can currently see but are not illuminated
            (width, height), fill_value=False, dtype=bool
        )
        self.explored = np.full(  # Tiles the player has seen before
            (width, height), fill_value=False, dtype=bool
        )

        self.downstairs_location = (0, 0)
        self.upstairs_location = (0, 0)

    @property
    def gamemap(self) -> GameMap:
        return self

    @property
    def actors(self) -> Iterator[Actor]:
        """Iterate over this maps living actors."""
        yield from (
            entity
            for entity in self.entities
            if isinstance(entity, Actor) and entity.is_alive
        )

    @property
    def items(self) -> Iterator[Item]:
        yield from (entity for entity in self.entities if isinstance(entity, Item))

    def get_entities_at_location(self, location_x: int, location_y: int) -> list:
        list_entities = []
        for entity in self.entities:
            if (
                entity.x == location_x
                and entity.y == location_y
            ):
                list_entities.append(entity)

        return list_entities

    def get_items_at_location(self, location_x: int, location_y: int) -> list:
        list_items = []
        for item in self.entities:
            if (
                isinstance(item, Item)
                and item.x == location_x
                and item.y == location_y
            ):
                list_items.append(item)

        return list_items

    def get_blocking_entity_at_location(self, location_x: int, location_y: int) -> Optional[Entity]:
        for entity in self.entities:
            if (
                entity.blocks_movement
                and entity.x == location_x
                and entity.y == location_y
            ):
                return entity

        return None

    def get_actor_at_location(self, x: int, y: int) -> Optional[Actor]:
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor

        return None

    def get_tile_at_location(self, x: int, y: int) -> tile_types.tile_dt:
        return self.tiles["tileid"][x,y]

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def get_lit_and_visible(self):
        self.lit_and_visible = np.logical_and(self.visible, self.lit_tiles)
        return self.lit_and_visible
    def add_explored(self):
        if self.engine.player.fighter.light >= 1:
            self.explored |= self.visible
            self.explored |= self.obscured_but_visible
    def remove_all_light(self):
        self.lit_tiles = np.full(  # Tiles that are in the light
            (self.width, self.height), fill_value=False, order="F"
            )

    def render(self, console: Console) -> None:
        """
        Renders the map.

        If a tile is in the "visible" array, then draw it with the "light" colors.
        If it isn't, but it's in the "explored" array, then draw it with the "dark" colors.
        Otherwise, the default is "SHROUD".
        """
        
        self.tiles_memory = np.where(self.visible, self.tiles, self.tiles_memory)
        
        console.rgb[0 : self.width, 0 : self.height] = np.select(
            condlist=[self.lit_and_visible, self.visible, self.obscured_but_visible, self.explored],
            choicelist=[self.tiles_memory["light"], self.tiles_memory["dark"], self.tiles_memory["obscured"], self.tiles_memory["deep"]],
            default=tile_types.SHROUD,
        )

        # draw all other entities
        entities_sorted_for_rendering = sorted(
            self.entities - {self.engine.player}, key=lambda x: x.render_order.value*10000000 + x.value * 100000 + x.id
        )
        for entity in entities_sorted_for_rendering:
            bghere = tuple(console.bg[entity.x, entity.y])
            tile = self.get_tile_at_location(entity.x, entity.y)
            banned = (DOWN_STAIRCASE, UP_STAIRCASE,)
            if tile in banned:
                fgcol = entity.color
                bgcol = bghere
            else:
                if len(self.get_entities_at_location(entity.x, entity.y)) <= 1:
                    fgcol = entity.color
                    bgcol = bghere
                else:
                    fgcol = color.black
                    bgcol = color.dkgreen
            
            if self.lit_and_visible[entity.x, entity.y]:
                libtcodpy.console_put_char_ex(
                    console,
                    entity.x, entity.y, entity.char, fgcol, bgcol
                )
            elif self.obscured_but_visible[entity.x, entity.y]:
                console.print(
                    x=entity.x, y=entity.y, string='?', fg=color.gray
                )
            elif self.visible[entity.x, entity.y]:
                console.print(
                    x=entity.x, y=entity.y, string='?', fg=color.gray
                )

        # draw player lastly
        console.print(
            x=self.engine.player.x, y=self.engine.player.y, string=self.engine.player.char, fg=self.engine.player.color
        )


class GameWorld:
    """
    Holds the settings for the GameMap, and generates new maps when moving down the stairs.
    """

    def __init__(
        self,
        *,
        engine: Engine,
        map_width: int,
        map_height: int,
        current_floor: int = 1
    ):
        self.engine = engine

        self.map_width = map_width
        self.map_height = map_height

    def generate_floor(self) -> None:
        from procgen import generate_dungeon

        self.engine.game_map = generate_dungeon(
            map_width=self.map_width,
            map_height=self.map_height,
            engine=self.engine,
        )
