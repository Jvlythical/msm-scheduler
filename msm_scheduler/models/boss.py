from typing import List

from ..typing import BossParams

class Boss:
    def __init__(self, **kwargs: BossParams):
        self.availability = kwargs.get('availability', [])
        self.capacity = kwargs.get('capacity', 0)
        self.clear_probability = kwargs.get('clear_probability', 0)
        self.experience = kwargs.get('experience', 0)
        self.hp_required = kwargs.get('hp_required', 0)  # New property
        self.name = kwargs.get('name', '')
        self.total_max_damage_cap_required = kwargs.get('total_max_damage_cap_required', 0)  # Renamed property

    @property
    def availability(self):
        return self._availability

    @availability.setter
    def availability(self, value: List[str]):
        if not all(isinstance(day, str) for day in value):
            raise ValueError("All availability entries must be strings")
        self._availability = value

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, value: int):
        if value < 0:
            raise ValueError("capacity must be a positive integer")
        self._capacity = value

    @property
    def clear_probability(self):
        return self._clear_probability

    @clear_probability.setter
    def clear_probability(self, value: int):
        if value < 0 or value > 100:
            raise ValueError("clear_probability must be between 0 and 100")
        self._clear_probability = value

    @property
    def experience(self):
        return self._experience

    @experience.setter
    def experience(self, value: int):
        if value < 0:
            raise ValueError("experience must be a positive integer")
        self._experience = value

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
        if not value:
            raise ValueError("Name cannot be empty")
        self._name = value

    @property
    def total_max_damage_cap_required(self):
        return self._total_max_damage_cap_required

    @total_max_damage_cap_required.setter
    def total_max_damage_cap_required(self, value: int):
        if value < 0:
            raise ValueError("total_max_damage_cap_required must be a positive integer")
        self._total_max_damage_cap_required = value

    def __repr__(self):
        return (f"Boss(name={self.name}, total_max_damage_cap_required={self.total_max_damage_cap_required}, "
                f"experience={self.experience}, clear_probability={self.clear_probability}, "
                f"availability={self.availability}, capacity={self.capacity}, hp_required={self.hp_required})")
