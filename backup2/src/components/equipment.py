from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from components.base_component import BaseComponent
from equipment_types import EquipmentType

if TYPE_CHECKING:
    from entity import Actor, Item


class Equipment(BaseComponent):
    parent: Actor

    def __init__(self, weapon: Optional[Item] = None, armor: Optional[Item] = None):
        self.weapon = weapon
        self.armor = armor

    @property
    def av_bonus(self) -> int:
        bonus = 0
        if self.weapon is not None and self.weapon.equippable is not None:
            bonus += self.weapon.equippable.av
        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.av
        return bonus
    @property
    def dr_bonus(self) -> int:
        bonus = 0
        if self.weapon is not None and self.weapon.equippable is not None:
            bonus += self.weapon.equippable.dr
        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.dr
        return bonus

    @property
    def attack_bonus(self) -> int:
        bonus = 0
        if self.weapon is not None and self.weapon.equippable is not None:
            bonus += self.weapon.equippable.attack
        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.attack
        return bonus
    @property
    def damage_bonus(self) -> int:
        bonus = 0
        if self.weapon is not None and self.weapon.equippable is not None:
            bonus += self.weapon.equippable.damage
        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.damage
        return bonus

    @property
    def beauty_bonus(self) -> int:
        bonus = 0
        if self.weapon is not None and self.weapon.equippable is not None:
            bonus += self.weapon.equippable.beauty
        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.beauty
        return bonus
    @property
    def scary_bonus(self) -> int:
        bonus = 0
        if self.weapon is not None and self.weapon.equippable is not None:
            bonus += self.weapon.equippable.scary
        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.scary
        return bonus
    
    @property
    def light_bonus(self) -> int:
        bonus = 0
        if self.weapon is not None and self.weapon.equippable is not None:
            bonus += self.weapon.equippable.light
        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.light
        return bonus
    @property
    def vision_bonus(self) -> int:
        bonus = 0
        if self.weapon is not None and self.weapon.equippable is not None:
            bonus += self.weapon.equippable.vision
        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.vision
        return bonus
    
    @property
    def atk_nrg_bonus(self) -> int:
        bonus = 0
        if self.weapon is not None and self.weapon.equippable is not None:
            bonus += self.weapon.equippable.atk_nrg
        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.atk_nrg
        return bonus
    @property
    def mov_nrg_bonus(self) -> int:
        bonus = 0
        if self.weapon is not None and self.weapon.equippable is not None:
            bonus += self.weapon.equippable.mov_nrg
        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.mov_nrg
        return bonus

    def item_is_equipped(self, item: Item) -> bool:
        return self.weapon == item or self.armor == item

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

    def toggle_equip(self, equippable_item: Item, add_message: bool = True) -> None:
        if (
            equippable_item.equippable
            and equippable_item.equippable.equipment_type == EquipmentType.WEAPON
        ):
            slot = "weapon"
        else:
            slot = "armor"

        if getattr(self, slot) == equippable_item:
            self.unequip_from_slot(slot, add_message)
        else:
            self.equip_to_slot(slot, equippable_item, add_message)
