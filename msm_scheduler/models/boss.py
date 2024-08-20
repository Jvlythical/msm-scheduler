from typing import List

from ..constants.boss import VALID_BOSSES
from ..types import BossParams


class Boss:
    def __init__(self, **kwargs: BossParams):
        self.arcane_power_required = kwargs.get('arcane_power_required', 0)
        self.capacity = kwargs.get('capacity', 0)
        self.clear_probability = kwargs.get('clear_probability', 0)
        self.difficulty = kwargs.get('difficulty', 0)
        self.hp_required = kwargs.get('hp_required', 0)  # New property
        self.name = kwargs.get('name', '')
        self.total_max_damage_cap_required = kwargs.get('total_max_damage_cap_required', 0)  # Renamed property

    @property
    def arcane_power_required(self):
        return self._arcane_power_required

    @arcane_power_required.setter
    def arcane_power_required(self, value: int):
        if value < 0:
            raise ValueError("capacity must be a positive integer")
        self._arcane_power_required = value

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, value: int):
        if value < 0:
            raise ValueError("capacity must be a positive integer")
        self._capacity = value

    @property
    def difficulty(self):
        return self._difficulty

    @difficulty.setter
    def difficulty(self, value: int):
        if value < 0:
            raise ValueError("difficulty must be a positive integer")
        self._difficulty = value

    @property
    def hp_required(self):
        return self._hp_required

    @hp_required.setter
    def hp_required(self, value: int):
        if value < 0:
            raise ValueError("hp_required must be a positive integer")
        self._hp_required = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        if value not in VALID_BOSSES:
            raise ValueError(
                f"boss {value} must be from of the valid bosses {VALID_BOSSES}")
        self._name = value

    @property
    def total_max_damage_cap_required(self):
        return self._total_max_damage_cap_required

    @total_max_damage_cap_required.setter
    def total_max_damage_cap_required(self, value: int):
        if value < 0:
            raise ValueError(
                "total_max_damage_cap_required must be a positive integer")
        self._total_max_damage_cap_required = value

    def __repr__(self):
        return (
            f"Boss(name={self.name}, total_max_damage_cap_required={self.total_max_damage_cap_required}, "
            f"difficulty={self.difficulty}, clear_probability={self.clear_probability}, "
            f"capacity={self.capacity}, hp_required={self.hp_required})"
        )
