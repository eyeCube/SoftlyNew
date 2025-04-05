from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from components.base_component import BaseComponent
from equipment_types import EquipmentType

if TYPE_CHECKING:
    from entity import Actor, Item


class Equipment(BaseComponent):
    parent: Actor

    def __init__(self, mainhand: Optional[Item] = None, offhand: Optional[Item] = None, armor: Optional[Item] = None):
        self.mainhand = mainhand
        self.offhand = offhand
        self.armor = armor

    @property
    def av_bonus(self) -> int:
        bonus = 0
        if self.offhand is not None and self.offhand.equippable is not None:
            bonus += self.offhand.equippable.av
        if self.mainhand is not None and self.mainhand.equippable is not None:
            bonus += self.mainhand.equippable.av
        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.av
        return bonus
    @property
    def dr_bonus(self) -> int:
        bonus = 0
        if self.offhand is not None and self.offhand.equippable is not None:
            bonus += self.offhand.equippable.dr
        if self.mainhand is not None and self.mainhand.equippable is not None:
            bonus += self.mainhand.equippable.dr
        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.dr
        return bonus

    @property
    def attack_bonus(self) -> int:
        bonus = 0
        if self.mainhand is not None and self.mainhand.equippable is not None:
            bonus += self.mainhand.equippable.attack
        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.attack
        return bonus
    @property
    def damage_bonus(self) -> int:
        bonus = 0
        if self.mainhand is not None and self.mainhand.equippable is not None:
            bonus += self.mainhand.equippable.damage
        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.damage
        return bonus

    @property
    def beauty_bonus(self) -> int:
        bonus = 0
        if self.offhand is not None and self.offhand.equippable is not None:
            bonus += self.offhand.equippable.beauty
        if self.mainhand is not None and self.mainhand.equippable is not None:
            bonus += self.mainhand.equippable.beauty
        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.beauty
        return bonus
    @property
    def scary_bonus(self) -> int:
        bonus = 0
        if self.offhand is not None and self.offhand.equippable is not None:
            bonus += self.offhand.equippable.scary
        if self.mainhand is not None and self.mainhand.equippable is not None:
            bonus += self.mainhand.equippable.scary
        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.scary
        return bonus

    @property
    def light_bonus(self) -> int:
        bonus = 0
        if self.offhand is not None and self.offhand.equippable is not None:
            bonus = max(bonus, self.offhand.equippable.light)
        if self.mainhand is not None and self.mainhand.equippable is not None:
            bonus = max(bonus, self.mainhand.equippable.light)
        if self.armor is not None and self.armor.equippable is not None:
            bonus = max(bonus, self.armor.equippable.light)
        return bonus
    @property
    def vision_bonus(self) -> int:
        bonus = 0
        if self.offhand is not None and self.offhand.equippable is not None:
            bonus += self.offhand.equippable.vision
        if self.mainhand is not None and self.mainhand.equippable is not None:
            bonus += self.mainhand.equippable.vision
        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.vision
        return bonus
    
    @property
    def accuracy_bonus(self) -> int:
        bonus = 0
        if self.offhand is not None and self.offhand.equippable is not None:
            bonus += self.offhand.equippable.accuracy
        if self.mainhand is not None and self.mainhand.equippable is not None:
            bonus += self.mainhand.equippable.accuracy
        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.accuracy
        return bonus
    @property
    def missile_damage_bonus(self) -> int:
        bonus = 0
        if self.mainhand is not None and self.mainhand.equippable is not None:
            bonus += self.mainhand.equippable.missile_damage
        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.missile_damage
        return bonus

    def item_is_equipped(self, item: Item) -> bool:
        return (
            self.mainhand == item
            or self.armor == item
            or self.offhand == item
            )
    def get_slot_item_is_equipped_to(self, item: Item) -> bool:
        if self.mainhand == item:
            return "mainhand"
        if self.offhand == item:
            return "offhand"
        if self.armor == item:
            return "armor"

    def unequip_message(self, item_name: str) -> None:
        self.parent.gamemap.engine.message_log.add_message(
            f"You remove the {item_name}."
        )

    def equip_message(self, item_name: str) -> None:
        self.parent.gamemap.engine.message_log.add_message(
            f"You equip the {item_name}."
        )

    def equip_to_slot(self, slot: str, item: Item, add_message: bool) -> None:
        current_item = getattr(self, slot)

        if current_item is not None:
            self.unequip_from_slot(slot, add_message)

        setattr(self, slot, item)

        if add_message:
            self.equip_message(item.name)

    def unequip_from_slot(self, slot: str, add_message: bool) -> None:
        current_item = getattr(self, slot)

        if add_message:
            self.unequip_message(current_item.name)

        setattr(self, slot, None)

    def toggle_equip(self, equippable_item: Item, add_message: bool = True, offhand: bool = False) -> None:
        '''
            TODO
            fix this -- doesn't work well with offhand
        '''
        if (
            equippable_item.equippable
            and equippable_item.equippable.equipment_type == EquipmentType.WEAPON
        ):
            if getattr(self, "offhand") == equippable_item:
                equipped_already = True
                slot = "offhand"
            elif getattr(self, "mainhand") == equippable_item:
                equipped_already = True
                slot = "mainhand"
            else:
                equipped_already = False
                slot = "offhand" if offhand else "mainhand"
        else:
            slot = "armor"
            equipped_already = True if getattr(self, slot) == equippable_item else False

        if equipped_already:
            self.unequip_from_slot(slot, add_message)
        else:
            self.equip_to_slot(slot, equippable_item, add_message)
