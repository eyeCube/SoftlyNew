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

        if (dungeon.in_bounds(x,y) and not any(entity.x == x and entity.y == y for entity in dungeon.entities)):
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




    # -------------------------------------------------- #
    #          Main dungeon generator function           #
    # -------------------------------------------------- #


def generate_dungeon(map_width, map_height, engine) -> GameMap:
    """Generate a new dungeon map based on the player's location."""

    # set the seed to the correct value based on player location
    print("creating new zone: ({}, {})".format(engine.world_location[0], engine.world_location[1]))
    random.seed(engine.world_location[0]*10000 + engine.world_location[1]*100 + engine.world_seed)
    
    if engine.world_location[1] == 0:
        dungeon = _generate_superhighway(map_width, map_height, engine)
    elif engine.world_location[1] <= 4:
        dungeon = _generate_warehouse(map_width, map_height, engine)
    else: # default (should never get here...)
        dungeon = _generate_warehouse(map_width, map_height, engine)
    
    #print("seeding new zone: ", dungeon.seed_xy)
    engine.explored_zones.update({(engine.world_location[0],engine.world_location[1]) : dungeon.seed_xy})

    return dungeon

def _generate_superhighway(map_width, map_height, engine) -> GameMap:
    """Generate a superhighway style map."""
    
    player = engine.player
    dungeon = GameMap(engine, map_width, map_height, entities=[player], default_fill=tile_types.chasm)

    rooms: List[RectangularRoom] = []
    
    first_room = RectangularRoom(0, 13, map_width, 16)
    rooms.append(first_room)

    max_iterations = 60
    max_rooms = 7
    room_min_size = 9
    room_max_size = 12
    
    __make_rooms(
        map_width, map_height, engine, dungeon, rooms, player, max_rooms, room_min_size, room_max_size,
        max_iterations=max_iterations,
        connect_back=1, connect_back_min_rooms=0, tunnel_from_prev=0.2, walls=True, wall_tile=tile_types.red_wall,
        max_tunnel_distance=999,
        downstairs_tile=tile_types.down_ladder, tunnel_tile=tile_types.wood_floor
        )
    
    dungeon.tiles[first_room.outer] = tile_types.concrete_highway
        
    # Place player in the dungeon
    if engine.coming_from == 1:
        engine.player.place(*dungeon.downstairs_location, dungeon)
    else:
        player.place(*first_room.center, dungeon)

    return dungeon
    

def _generate_warehouse(map_width, map_height, engine) -> GameMap:
    """Generate a warehouse style map."""

    complexity = 5 # temporary -- adjust as needed...
    max_rooms = min(200, engine.world_location[1] * complexity)
    room_min_size = 6
    room_max_size = 13
    
    player = engine.player
    dungeon = GameMap(engine, map_width, map_height, entities=[player], default_fill=tile_types.chasm)

    rooms: List[RectangularRoom] = []

    max_iterations = max_rooms*30
    __make_rooms(
        map_width, map_height, engine, dungeon, rooms, player, max_rooms, room_min_size, room_max_size,
        max_iterations=max_iterations
        )

    # Generate upward staircase
    dungeon.upstairs_location = rooms[0].center
    dungeon.tiles[dungeon.upstairs_location] = tile_types.up_ladder if engine.world_location[1] == 1 else tile_types.up_stairs
    dungeon.tiles[rooms[-1].center] = tile_types.down_stairs
    dungeon.downstairs_location = rooms[-1].center

    if (engine.coming_from == -1 and (dungeon.tiles[player.x,player.y]['stairs_up'] == False)):
        dungeon.tiles[player.x,player.y] = tile_types.up_stairs
        
    # Place player in the dungeon
    engine.player.place(player.x, player.y, dungeon)
    
    return dungeon

def __make_rooms(
    map_width, map_height, engine, dungeon, rooms, player, max_rooms, room_min_size, room_max_size,
    max_iterations=1000, starting_position=None,
    connect_back=0.4, connect_back_min_rooms=5, tunnel_from_prev=1, max_tunnel_distance=16,
    walls=False, wall_tile=None, floor_tile=tile_types.concrete_floor,
    downstairs_tile=tile_types.down_stairs, tunnel_tile=tile_types.concrete_floor
    ):

    center_of_last_room = (0, 0)
    center_of_first_room = (0,0)

    new_room = None

    i = 0
    iterations = 0
    
    while (iterations < max_iterations and len(rooms) < max_rooms):
        iterations += 1
        
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        #if tuple(engine.world_location) in engine.explored_zones.keys():
        #    x,y = engine.explored_zones[tuple(engine.world_location)]
        if starting_position is not None:
            assert(type(starting_position) == type(tuple([])))
            x,y = starting_position
        elif (i==0 and engine.world_location[1] > 0):
            x = player.x - int(room_width * 0.5)
            y = player.y - int(room_height * 0.5)
        else:
            x = random.randint(0, dungeon.width - room_width - 1)
            y = random.randint(0, dungeon.height - room_height - 1)
        dungeon.seed_xy = (x,y)
        new_room = RectangularRoom(x, y, room_width, room_height)

        # Run through the other rooms and see if they intersect with this one.
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue    # This room intersects, so go to the next attempt.
                        # If there are no intersections then the room is valid.

        if len(rooms) > 0:
            d = max(abs(new_room.center[0] - rooms[-1].center[0]), abs(new_room.center[1] - rooms[-1].center[1]))
            if d >= max_tunnel_distance:
                continue

        # Build up walls around the room
        if walls:
            dungeon.tiles[new_room.outer][np.logical_and(
                dungeon.tiles[new_room.outer]['tileid'] != floor_tile['tileid'],
                dungeon.tiles[new_room.outer]['tileid'] != tunnel_tile['tileid']
                )] = wall_tile

        if i == 0:
            center_of_first_room = new_room.center
        # Dig out a tunnel between this room and the previous one.
        if (i > 0 and random.random() < tunnel_from_prev):
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                if dungeon.tiles[x, y] != floor_tile:
                    dungeon.tiles[x, y] = tunnel_tile
        # randomly connect back to first room to reduce linearity
        if (len(rooms) >= connect_back_min_rooms and random.random() < connect_back):
            index = 0
            center_of_last_room = new_room.center
            for x, y in tunnel_between(rooms[index].center, new_room.center):
                if dungeon.tiles[x, y] != floor_tile:
                    dungeon.tiles[x, y] = tunnel_tile
            
        # Dig out this room's inner area
        dungeon.tiles[new_room.inner] = floor_tile
        
        i += 1

        place_entities(new_room, dungeon, engine.world_location[1])

        # Finally, append the new room to the list.
        rooms.append(new_room)

    dungeon.tiles[center_of_last_room] = downstairs_tile
    dungeon.downstairs_location = center_of_last_room
        
