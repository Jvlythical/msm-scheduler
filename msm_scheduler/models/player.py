from typing import List

from ..types import Experience, PlayerParams

class Player:
    def __init__(self, **kwargs: PlayerParams):
        self.name = kwargs.get('name', '')
        self.max_damage_cap = kwargs.get('max_damage_cap', 0)
        self.hp = kwargs.get('hp', 0)
        self.arcane_power = kwargs.get('arcane_power', 0)
        self.availability = kwargs.get('availability', [])
        self.experience = kwargs.get('experience', {
            'hard_damien': 0,
            'lucid': 0,
            'lotus': 0,
            'normal_damien': 0,
            'will': 0
        })

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
    def experience(self):
        return self._experience

    @experience.setter
    def experience(self, value: Experience):
        if not all(isinstance(exp, int) for exp in value.values()):
            raise ValueError("All experience values must be integers")
        self._experience = {k: value[k] for k in sorted(value)}

    def __repr__(self):
        return (f"Player(name={self.name}, max_damage_cap={self.max_damage_cap}, hp={self.hp}, "
                f"arcane_power={self.arcane_power}, availability={self.availability}, "
                f"experience={self.experience})")
