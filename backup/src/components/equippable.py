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
        acc_range: int = 1
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
        self.acc_range = acc_range


class MeleeWeapon(Equippable):
    def __init__(self, damage=1, attack=1, scary=1, beauty=0, twoh=False, reach=1, av=0, dr=0, acc_range=1) -> None:
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
            acc_range=acc_range,
            )


class Armor(Equippable):
    def __init__(self, av=1, dr=0, scary=0, beauty=0) -> None:
        super().__init__(
            equipment_type=EquipmentType.ARMOR,
            av=av,
            dr=dr,
            scary=scary,
            beauty=beauty
            )

