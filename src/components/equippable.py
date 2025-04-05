from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_component import BaseComponent
from equipment_types import EquipmentType

if TYPE_CHECKING:
    from entity import Item


class Equippable(BaseComponent):
    parent: Item

    def __init__(
        self,
        equipment_type: EquipmentType,
        damage: int = 0,
        attack: int = 0,
        av: int = 0,
        dr: int = 0,
        scary: int = 0,
        beauty: int = 0,
        reach: int = 1,
        twoh: bool = False,
        light: int = 0,
        vision: int = 0,
        accuracy: int = 0,
        missile_range: int = 0,
        missile_damage: int = 0,
        is_missile_weapon: bool = False,
    ):
        self.equipment_type = equipment_type

        self.damage = damage
        self.attack = attack
        self.av = av
        self.dr = dr
        self.scary = scary
        self.beauty = beauty
        self.reach = reach
        self.twoh = twoh
        self.vision = vision
        self.light = light
        self.accuracy = accuracy
        self.missile_range = missile_range
        self.missile_damage = missile_damage
        self.is_missile_weapon = is_missile_weapon
        

class MeleeWeapon(Equippable):
    def __init__(self,
                 damage=1, attack=1,
                 scary=1, beauty=0,
                 twoh=False, reach=1,
                 av=0, dr=0,
                 is_missile_weapon=False, missile_range=1, missile_damage=0, accuracy=0,
                 light=0, vision=0) -> None:
        super().__init__(
            equipment_type=EquipmentType.WEAPON,
            av = av,
            dr = dr,
            scary=scary,
            beauty=beauty,
            damage=damage,
            attack=attack,
            reach=reach,
            twoh=twoh,
            missile_range=missile_range,
            light=light,
            vision=vision,
            accuracy=accuracy,
            missile_damage=missile_damage,
            is_missile_weapon=is_missile_weapon
            )


class Armor(Equippable):
    def __init__(self, av=1, dr=0, scary=0, beauty=0, light=0, vision=0, accuracy=0, attack=0) -> None:
        super().__init__(
            equipment_type=EquipmentType.ARMOR,
            av=av,
            dr=dr,
            scary=scary,
            beauty=beauty,
            light=light,
            vision=vision,
            accuracy=accuracy,
            attack=attack,
            )

