from math import log
from typing import List

from ..constants.boss import MAX_EXPERIENCE, MIN_EXPERIENCE
from ..types import PlayerExperience, PlayerParams
from .boss import Boss

class Player:
    def __init__(self, **kwargs: PlayerParams):
        self.arcane_power = kwargs.get('arcane_power', 0)
        self.availability = kwargs.get('availability', [])
        self.experience = kwargs.get('experience', {})
        self.hp = kwargs.get('hp', 0)
        self.identity = kwargs.get('identity')
        self.interests = list(self.experience.keys())
        self.max_damage_cap = kwargs.get('max_damage_cap', 0)
        self.name = kwargs.get('name', '')

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        if not value:
            raise ValueError("Name cannot be empty")
        self._name = value

    @property
    def max_damage_cap(self):
        return self._max_damage_cap

    @max_damage_cap.setter
    def max_damage_cap(self, value: int):
        if value < 0:
            raise ValueError("max_damage_cap must be a positive integer")
        self._max_damage_cap = value

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value: int):
        if value < 0:
            raise ValueError("HP must be a positive integer")
        self._hp = value

    @property
    def arcane_power(self):
        return self._arcane_power

    @arcane_power.setter
    def arcane_power(self, value: int):
        if value < 0:
            raise ValueError("Arcane power must be a positive integer")
        self._arcane_power = value

    @property
    def availability(self):
        return self._availability

    @availability.setter
    def availability(self, value: List[str]):
        if not all(isinstance(day, str) for day in value):
            raise ValueError("All availability entries must be strings")
        self._availability = value

    @property
    def interests(self):
        return self._interests

    @interests.setter
    def interests(self, value):
        self._interests = value

    @property
    def experience(self):
        return self._experience

    @experience.setter
    def experience(self, value: PlayerExperience):
        if not all(isinstance(exp, int) for exp in value.values()):
            raise ValueError("All experience values must be integers")
        self._experience = {k: value[k] for k in sorted(value)}

    def boss_experience(self, boss: Boss):
        player_experience = self.experience[boss.name]
        if player_experience < MIN_EXPERIENCE:
            return MIN_EXPERIENCE
        elif player_experience > MAX_EXPERIENCE:
            return MAX_EXPERIENCE
        return player_experience

    def boss_max_damage_cap(self, boss: Boss):
        experience = self.boss_experience(boss)
        return self.max_damage_cap * log(experience, MAX_EXPERIENCE)

    def remove_availability(self, time: str):
        self.availability.remove(time)

    def __repr__(self):
        return (f"Player(name={self.name}, max_damage_cap={self.max_damage_cap}, hp={self.hp}, "
                f"arcane_power={self.arcane_power}, availability={self.availability}, "
                f"experience={self.experience})")
