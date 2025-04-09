from __future__ import annotations

from const import *

import random
import math

from typing import Optional, Tuple, TYPE_CHECKING

import color
import exceptions

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor, Entity, Item


class Action:
    def __init__(self, entity: Actor, performedByPlayer: bool) -> None:
        super().__init__()
        self.entity = entity
        self.performedByPlayer = performedByPlayer

    @property
    def engine(self) -> Engine:
        """Return the engine this action belongs to."""
        return self.entity.gamemap.engine

    def perform(self) -> None:
        """Perform this action with the objects needed to determine its scope.

        `self.engine` is the scope this action is being performed in.

        `self.entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class PickupAction(Action):
    """Pickup an item and add it to the inventory, if there is room for it."""

    def __init__(self, entity: Actor, performedByPlayer: bool):
        super().__init__(entity, performedByPlayer)

    def perform(self) -> None:
        actor_location_x = self.entity.x
        actor_location_y = self.entity.y
        inventory = self.entity.inventory
        
        if len(inventory.items) >= inventory.capacity:
            raise exceptions.Impossible("Your inventory is full.")
        
        le = self.engine.game_map.get_items_at_location(actor_location_x, actor_location_y)
        entities_sorted_for_retrieval = sorted(
            le, key=lambda x: x.value * 10000 + x.id, reverse=True
        )
        if len(le) > 0:
            item = entities_sorted_for_retrieval[0]

            self.engine.game_map.entities.remove(item)
            item.parent = self.entity.inventory
            inventory.items.append(item)

            self.engine.message_log.add_message(f"You picked up the {item.name}.")
            return

        raise exceptions.Impossible("There is nothing here worth getting.")


class ItemAction(Action):
    def __init__(
        self, entity: Actor, performedByPlayer: bool, item: Item, target_xy: Optional[Tuple[int, int]] = None
    ):
        super().__init__(entity, performedByPlayer)
        self.item = item
        if not target_xy:
            target_xy = entity.x, entity.y
        self.target_xy = target_xy

    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this actions destination."""
        return self.engine.game_map.get_actor_at_location(*self.target_xy)

    def perform(self) -> None:
        """Invoke the items ability, this action will be given to provide context."""
        if self.item.consumable:
            self.item.consumable.activate(self)


class DropItem(ItemAction):
    def perform(self) -> None:
        if self.entity.equipment.item_is_equipped(self.item):
            self.entity.equipment.toggle_equip(self.item)

        self.entity.inventory.drop(self.item)


class EquipAction(Action):
    def __init__(self, entity: Actor, performedByPlayer: bool, item: Item):
        super().__init__(entity, performedByPlayer)

        self.item = item

    def perform(self) -> None:
        offhand = True if self.entity.equipment.mainhand is not None else False
        self.entity.equipment.toggle_equip(self.item, offhand=offhand)


class WaitAction(Action):
    def perform(self) -> None:
        pass


class TakeStairsDownAction(Action):
    def perform(self) -> None:
        """
        Take the stairs down, if any exist at the entity's location.
        """
        if (   DOWN_STAIRCASE == self.engine.game_map.get_tile_at_location(self.entity.x, self.entity.y)
            or DOWN_LADDER == self.engine.game_map.get_tile_at_location(self.entity.x, self.entity.y)
            ):
            self.engine.descend()
        else:
            raise exceptions.Impossible("There are no stairs here.")
class TakeStairsUpAction(Action):
    def perform(self) -> None:
        """
        Take the stairs up, if any exist at the entity's location.
        """
        if (   UP_STAIRCASE == self.engine.game_map.get_tile_at_location(self.entity.x, self.entity.y)
            or UP_LADDER == self.engine.game_map.get_tile_at_location(self.entity.x, self.entity.y)
            ):
            self.engine.ascend()
        else:
            raise exceptions.Impossible("There are no stairs here.")


class ActionWithDirection(Action):
    def __init__(self, entity: Actor, performedByPlayer:bool, dx: int, dy: int):
        super().__init__(entity, performedByPlayer)

        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> Tuple[int, int]:
        """Returns this actions destination."""
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[Entity]:
        """Return the blocking entity at this action's destination."""
        return self.engine.game_map.get_blocking_entity_at_location(*self.dest_xy)

    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this action's destination."""
        return self.engine.game_map.get_actor_at_location(*self.dest_xy)

    @property
    def target_entity(self) -> Optional[Entity]:
        """Return the entity at this action's destination."""
        le = self.engine.game_map.get_entities_at_location(*self.dest_xy)
        entities_sorted_for_retrieval = sorted(
            le, key=lambda x: x.value * 100000 + x.id, reverse=True
        )
        if len(le) > 0:
            return entities_sorted_for_retrieval[0]
        return None

    def perform(self) -> None:
        raise NotImplementedError()


class MeleeAction(ActionWithDirection):
    def perform(self) -> None:
        target = self.target_actor
        if not target:
            raise exceptions.Impossible("Nothing to attack.")

        p2 = 0.5 * self.entity.fighter.power
        damage = max(0, math.ceil(p2 + random.random()*p2) - target.fighter.defense)
        miss = False
        if (random.random()*self.entity.fighter.attack <= target.fighter.dodge):
            damage = 0
            miss = True

        attack_desc = f"{self.entity.title.capitalize()}{self.entity.name} attacks {target.title}{target.name}"
        attack_color = color.player_atk if self.entity is self.engine.player else color.enemy_atk

        if damage > 0:
            self.engine.message_log.add_message(
                f"{attack_desc} for {damage} hit points.", attack_color
            )
            target.fighter.hp -= damage
        elif miss:
            self.engine.message_log.add_message(
                f"{attack_desc}, but misses.", attack_color
            )
        else:
            self.engine.message_log.add_message(
                f"{attack_desc}, but the attack is ineffective.", attack_color
            )


class MovementAction(ActionWithDirection):
    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy

        if (self.performedByPlayer and self.target_entity is not None):
            self.engine.message_log.add_message(
                f"Here: {self.target_entity.name}", (128,128,128,)
                )
            
        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            # Destination is out of bounds.
            raise exceptions.Impossible("That way is blocked.")
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            # Destination is blocked by a tile.
            raise exceptions.Impossible("That way is blocked.")
        if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            # Destination is blocked by an entity.
            raise exceptions.Impossible("That way is blocked.")

        self.entity.move(self.dx, self.dy)


class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        if self.target_actor:
            return MeleeAction(self.entity, self.performedByPlayer, self.dx, self.dy).perform()

        else:
            return MovementAction(self.entity, self.performedByPlayer, self.dx, self.dy).perform()
