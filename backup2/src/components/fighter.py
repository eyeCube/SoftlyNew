from __future__ import annotations

from typing import TYPE_CHECKING

import color
from components.base_component import BaseComponent
from render_order import RenderOrder

if TYPE_CHECKING:
    from entity import Actor


class Fighter(BaseComponent):
    parent: Actor

    def __init__(self, hp = 1, av = 0, dmg = 1, atk = 100, dr = 0, beauty = 0, scary = 0, light = 0, vision = 20):
        self.max_hp         = hp
        self._hp            = hp
        self.base_defense   = av
        self.base_power     = dmg
        self.base_attack    = atk
        self.base_dodge     = dr
        self.base_beauty    = beauty
        self.base_scary     = scary
        self.base_light     = light
        self.base_vision    = vision

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))
        if self._hp == 0 and self.parent.ai:
            self.die()
            
    @property
    def beauty(self) -> int:
        return self.base_beauty + self.beauty_bonus
    @property
    def scary(self) -> int:
        return self.base_scary + self.scary_bonus

    @property
    def defense(self) -> int:
        return self.base_defense + self.defense_bonus
    @property
    def dodge(self) -> int:
        return self.base_dodge + self.dodge_bonus

    @property
    def power(self) -> int:
        return self.base_power + self.power_bonus
    @property
    def attack(self) -> int:
        return self.base_attack + self.attack_bonus
    
    @property
    def light(self) -> int:
        return self.base_light + self.light_bonus
    @property
    def vision(self) -> int:
        return self.base_vision + self.vision_bonus

    @property
    def beauty_bonus(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.beauty_bonus
        else:
            return 0
    @property
    def scary_bonus(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.scary_bonus
        else:
            return 0

    @property
    def defense_bonus(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.av_bonus
        else:
            return 0
    @property
    def dodge_bonus(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.dr_bonus
        else:
            return 0

    @property
    def power_bonus(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.damage_bonus
        else:
            return 0
    @property
    def attack_bonus(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.attack_bonus
        else:
            return 0
        
    @property
    def light_bonus(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.light_bonus
        else:
            return 0
    @property
    def vision_bonus(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.vision_bonus
        else:
            return 0

    def die(self) -> None:
        if self.engine.player is self.parent:
            death_message = "You died!"
            death_message_color = color.player_die
        else:
            death_message = f"{self.parent.title.capitalize()}{self.parent.name} dies."
            death_message_color = color.enemy_die

        self.parent.char = "%"
        self.parent.color = (191, 0, 0)
        self.parent.blocks_movement = False
        self.parent.ai = None
        self.parent.name = f"remains of {self.parent.name}"
        self.parent.render_order = RenderOrder.CORPSE

        self.engine.message_log.add_message(death_message, death_message_color)

        self.engine.player.level.add_xp(self.parent.level.xp_given)

    def heal(self, amount: int) -> int:
        if self.hp == self.max_hp:
            return 0

        new_hp_value = self.hp + amount

        if new_hp_value > self.max_hp:
            new_hp_value = self.max_hp

        amount_recovered = new_hp_value - self.hp

        self.hp = new_hp_value

        return amount_recovered

    def take_damage(self, amount: int) -> None:
        self.hp -= amount
