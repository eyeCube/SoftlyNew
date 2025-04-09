from __future__ import annotations

import random
from typing import Dict, Iterator, List, Tuple, TYPE_CHECKING
import tcod
import numpy as np

from const import *
import entity_factories
from game_map import GameMap
import tile_types


if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


max_items_by_floor = [
    (1, 0),
    (2, 1),
    (4, 2),
]

max_monsters_by_floor = [
    (1, 0),
    (2, 1),
    (3, 2),
    (4, 3),
    (6, 5),
]

item_chances: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(entity_factories.health_potion, 35), (entity_factories.weapons[CLASS_SWORDS][MAT_POLYMER], 5), (entity_factories.weapons[CLASS_DAGGERS][MAT_POLYMER], 5), (entity_factories.weapons[CLASS_AXES][MAT_POLYMER], 5)],
    2: [(entity_factories.confusion_scroll, 10), (entity_factories.weapons[CLASS_SWORDS][MAT_METAL], 5), (entity_factories.weapons[CLASS_DAGGERS][MAT_METAL], 5), (entity_factories.weapons[CLASS_AXES][MAT_METAL], 5)],
    4: [(entity_factories.lightning_scroll, 25), (entity_factories.weapons[CLASS_SWORDS][MAT_ALLOY], 5), (entity_factories.weapons[CLASS_DAGGERS][MAT_ALLOY], 5), (entity_factories.weapons[CLASS_AXES][MAT_ALLOY], 5)],
    6: [(entity_factories.fireball_scroll, 25)],
}

enemy_chances: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(entity_factories.omnibot, 80), (entity_factories.zetabie, 5)],
    1: [(entity_factories.zetabie, 15)],
    2: [(entity_factories.zetabie, 25)],
}


def get_max_value_for_floor(
    max_value_by_floor: List[Tuple[int, int]], floor: int
) -> int:
    current_value = 0

    for floor_minimum, value in max_value_by_floor:
        if floor_minimum > floor:
            break
        else:
            current_value = value

    return current_value


def get_entities_at_random(
    weighted_chances_by_floor: Dict[int, List[Tuple[Entity, int]]],
    number_of_entities: int,
    floor: int,
) -> List[Entity]:
    entity_weighted_chances = {}

    for key, values in weighted_chances_by_floor.items():
        if key > floor:
            break
        else:
            for value in values:
                entity = value[0]
                weighted_chance = value[1]

                entity_weighted_chances[entity] = weighted_chance

    entities = list(entity_weighted_chances.keys())
    entity_weighted_chance_values = list(entity_weighted_chances.values())

    chosen_entities = random.choices(
        entities, weights=entity_weighted_chance_values, k=number_of_entities
    )

    return chosen_entities


class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    @property
    def outer(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(self.x1, self.x2 + 1), slice(self.y1, self.y2 + 1)

    def intersects(self, other: RectangularRoom) -> bool:
        """Return True if this room overlaps with another RectangularRoom."""
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )


def place_entities(room: RectangularRoom, dungeon: GameMap, floor_number: int,) -> None:
    number_of_monsters = random.randint(
        0, get_max_value_for_floor(max_monsters_by_floor, floor_number)
    )
    number_of_items = random.randint(
        0, get_max_value_for_floor(max_items_by_floor, floor_number)
    )

    monsters: List[Entity] = get_entities_at_random(
        enemy_chances, number_of_monsters, floor_number
    )
    items: List[Entity] = get_entities_at_random(
        item_chances, number_of_items, floor_number
    )

    for entity in monsters + items:
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            entity.spawn(dungeon, x, y)


def tunnel_between(
    start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    """Return an L-shaped tunnel between these two points."""
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:  # 50% chance.
        # Move horizontally, then vertically.
        corner_x, corner_y = x2, y1
    else:
        # Move vertically, then horizontally.
        corner_x, corner_y = x1, y2

    # Generate the coordinates for this tunnel.
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y


def generate_dungeon(
    map_width: int,
    map_height: int,
    engine: Engine,
) -> GameMap:
    """Generate a dungeon map based on the player's location."""

    # set the seed to the correct value based on player location
    random.seed(engine.world_location[0]*10000 + engine.world_location[1]*100 + engine.world_seed)
    
    if engine.world_location[1] == 0:
        dungeon = _generate_superhighway(map_width, map_height, engine)
    elif engine.world_location[1] <= 4:
        dungeon = _generate_warehouse(map_width, map_height, engine)
    else: # default (should never get here...)
        dungeon = _generate_warehouse(map_width, map_height, engine)
        
    # Place player in the dungeon
    if engine.coming_from == 1:
        engine.player.place(*dungeon.downstairs_location, dungeon)

    # Generate upward staircase
    if engine.world_location[1] >= 1: # TODO: only do this if this floor has not been generated before. Otherwise remember where the staircase is.
        dungeon.tiles[(engine.player.x, engine.player.y)] = tile_types.up_stairs

    return dungeon

def _generate_superhighway(
    map_width: int,
    map_height: int,
    engine: Engine,
) -> GameMap:
    """Generate a superhighway style map."""
    
    player = engine.player
    dungeon = GameMap(engine, map_width, map_height, entities=[player], default_fill=tile_types.chasm)

    rooms: List[RectangularRoom] = []
    
    first_room = RectangularRoom(0, 13, map_width, 16)
    rooms.append(first_room)

    max_rooms = 60
    room_min_size = 9
    room_max_size = 12
    __make_rooms(
        map_width, map_height, engine, dungeon, rooms, player, max_rooms, room_min_size, room_max_size,
        connect_back=1, connect_back_min_rooms=0, tunnel_from_prev=0.2, walls=True, wall_tile=tile_types.blue_wall
        )
    
    dungeon.tiles[first_room.outer] = tile_types.concrete_highway

    player.place(*first_room.center, dungeon)

    return dungeon
    

def _generate_warehouse(
    map_width: int,
    map_height: int,
    engine: Engine,
) -> GameMap:
    """Generate a warehouse style map."""
    
    max_rooms = min(200, engine.world_location[1] * 50)
    room_min_size = 6
    room_max_size = 13
    
    player = engine.player
    dungeon = GameMap(engine, map_width, map_height, entities=[player])

    rooms: List[RectangularRoom] = []

    __make_rooms(map_width, map_height, engine, dungeon, rooms, player, max_rooms, room_min_size, room_max_size)
    
    return dungeon

def __make_rooms(
    map_width, map_height, engine, dungeon, rooms, player, max_rooms, room_min_size, room_max_size,
    connect_back=0.4, connect_back_min_rooms=5, tunnel_from_prev=1,
    walls=False, wall_tile=None, floor_tile=tile_types.concrete_floor
    ):

    center_of_last_room = (40, 20)

    new_room = None

    i = 0
    
    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        # "RectangularRoom" class makes rectangles easier to work with
        new_room = RectangularRoom(x, y, room_width, room_height)

        # Run through the other rooms and see if they intersect with this one.
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue  # This room intersects, so go to the next attempt.
        # If there are no intersections then the room is valid.

        # Dig out this rooms inner area.
        if walls:
            dungeon.tiles[new_room.outer] = wall_tile
            '''t = dungeon.tiles[new_room.outer]
            np.where(np.equal(t, np.full((room_width, room_height), fill_value=floor_tile, order="F")), floor_tile, wall_tile)'''
        dungeon.tiles[new_room.inner] = floor_tile

        if i == 0:
            # The first room, where the player starts.
            if (engine.coming_from == -1):
                player.place(*new_room.center, dungeon)
        else:  # All rooms after the first.
            # Dig out a tunnel between this room and the previous one.
            if random.random() < tunnel_from_prev:
                for x, y in tunnel_between(rooms[-1].center, new_room.center):
                    dungeon.tiles[x, y] = floor_tile
            # randomly connect back to first room to reduce linearity
            if (len(rooms) >= connect_back_min_rooms and random.random() < connect_back):
                index = 0
                for x, y in tunnel_between(rooms[index].center, new_room.center):
                    dungeon.tiles[x, y] = floor_tile

            center_of_last_room = new_room.center
        
        i += 1

        place_entities(new_room, dungeon, engine.world_location[1])

        # Finally, append the new room to the list.
        rooms.append(new_room)

    dungeon.tiles[center_of_last_room] = tile_types.down_stairs
    dungeon.downstairs_location = center_of_last_room
