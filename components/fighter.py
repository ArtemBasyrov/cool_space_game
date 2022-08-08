from __future__ import annotations

from typing import TYPE_CHECKING

import color
from components.base_component import BaseComponent
from render_order import RenderOrder
from components.ai import ExplodingAI
import numpy as np

if TYPE_CHECKING:
    from entity import Actor


class Fighter(BaseComponent):
    parent: Actor

    def __init__(self, hp: int, base_defense: int, base_power: int, base_mass: int):
        self.max_hp = hp
        self._hp = hp
        self.base_defense = base_defense
        self.base_power = base_power
        self.base_mass = base_mass

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))
        if self._hp == 0 and self.parent.ai:
            self.die()

    @property
    def defense(self) -> int:
        return self.base_defense + self.defense_bonus

    @property
    def power(self) -> int:
        return self.base_power + self.power_bonus

    @property
    def mass(self) -> int:
        return self.base_mass + self.mass_bonus

    @property
    def defense_bonus(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.defense_bonus
        else:
            return 0

    @property
    def power_bonus(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.power_bonus
        else:
            return 0

    @property
    def mass_bonus(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.mass_bonus
        else:
            return 0

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

    def die(self) -> None:
        if self.engine.player is self.parent:
            death_message = "You died!"
            death_message_color = color.player_die
        else:
            death_message = f"{self.parent.name} drifts dead!"
            death_message_color = color.enemy_die


        self.parent.char = "%"
        self.parent.blocks_movement = False
        self.parent.stored_action = None
        if np.random.randint(low=1,high=7) <= 6 and self.parent.name != 'Player':
            death_message = f"{self.parent.name} explodes!"
            self.parent.ai = ExplodingAI(entity=self.parent)
        else:
            self.parent.ai = None
        self.parent.name = f"remains of {self.parent.name}"
        self.parent.render_order = RenderOrder.CORPSE

        self.engine.message_log.add_message(death_message, death_message_color)