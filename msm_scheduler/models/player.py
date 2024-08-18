import pdb
from typing import List

from ..constants.boss import BOSS_VARIANTS_TABLE, MAX_EXPERIENCE, MIN_EXPERIENCE
from ..constants.player import AVAILABILITY_USAGES
from ..types import PlayerExperience, PlayerParams
from .boss import Boss

class Player:
    def __init__(self, **kwargs: PlayerParams):
        self.arcane_power = kwargs.get('arcane_power', 0)
        self.availability = kwargs.get('availability', [])
        self.availability_count = {}
        for availability in self.availability:
            self.availability_count[availability] = 0
        self.experience = kwargs.get('experience', {})
        self.hp = kwargs.get('hp', 0)
        self.identity = kwargs.get('identity')
        self.interests = kwargs.get('interests', {})
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
    def interests(self) -> List[str]:
        return self._interests

    @interests.setter
    def interests(self, value):
        interests = []
        for boss_name in value:
            experience = self.experience[boss_name]
            if experience >= MIN_EXPERIENCE and experience <= MAX_EXPERIENCE:
                interests.append(boss_name)
        self._interests = interests

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

    def boss_effectiveness(self, boss: Boss):
        if not boss:
            return 0

        boss_experience = self.boss_experience(boss)
        boss_experience_required = boss.experience_required if boss.experience_required > 0 else 1
        boss_total_max_damage_cap_required = boss.total_max_damage_cap_required
        max_damage_cap = self.max_damage_cap

        return max_damage_cap / boss_total_max_damage_cap_required * boss_experience * 525 / boss_experience_required

    def remove_availability(self, time: str):
        if time not in self.availability:
            return

        self.availability_count[time] += 1

        # Each availability time can be used AVAILABILITY_USAGES times
        if self.availability_count[time] >= AVAILABILITY_USAGES:
            self.availability.remove(time)

    def remove_interest(self, boss_name: str):
        if boss_name not in self.interests:
            return

        # A boss can have one or more variants e.g. normal damien and hard damien
        for variants in BOSS_VARIANTS_TABLE:
            if boss_name not in variants:
                continue
            
            # Since a player can only clear one variant a week, if they are no longer
            # interested in the boss, this is interpreted as they are no longer
            # interested in all variants. Remove all variants from their interests
            for boss_name in variants:
                if boss_name not in self.interests:
                    continue

                del self.interests[self.interests.index(boss_name)]

    def __repr__(self):
        return (
            f"Player(name={self.name}, max_damage_cap={self.max_damage_cap}, hp={self.hp}, "
            f"arcane_power={self.arcane_power}, availability={self.availability}, "
            f"experience={self.experience}), interests={self.interests}"
        )
