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
        self.discord_id = kwargs.get('discord_id', '')
        self.player_class = kwargs.get('class', '')

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        if not value:
            raise ValueError("Name cannot be empty")
        self._name = value

    @property
    def discord_id(self):
        return self._discord_id

    @discord_id.setter
    def discord_id(self, value: str):
        self._discord_id = value

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
    def interests(self, value: dict):
        interests = []
        for boss_name in value:
            if value[boss_name]:
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
        if boss.name not in self.experience:
            return MIN_EXPERIENCE
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
        boss_difficulty = boss.difficulty if boss.difficulty > 0 else 1
        boss_total_max_damage_cap_required = boss.total_max_damage_cap_required
        max_damage_cap = self.max_damage_cap

        return max_damage_cap / boss_total_max_damage_cap_required * boss_experience * 525 / boss_difficulty

    def boss_ready(self, boss: Boss):
        return self.hp >= boss.hp_required and self.arcane_power >= boss.arcane_power_required

    def remove_availability(self, time: str):
        if time not in self.availability:
            availabilities = "\n".join(self.availability)
            raise RuntimeError(f"=== {self.name} is not available at {time}\n~ Availabilities\n{availabilities}")

        self.availability_count[time] += 1

        # Each availability time can be used AVAILABILITY_USAGES times
        if self.availability_count[time] >= AVAILABILITY_USAGES:
            self.availability.remove(time)

    def remove_interest(self, boss_name: str, **options):
        if boss_name not in self.interests:
            interests = "\n".join(self.interests)
            raise RuntimeError(f"=== {self.name} is not interested in {boss_name}\n~ Interests\n{interests}")

        # A boss can have one or more variants e.g. normal damien and hard damien
        for variants in BOSS_VARIANTS_TABLE:
            if boss_name not in variants:
                continue

            # Since a player can only clear one variant a week, if they are no longer
            # interested in the boss, this is interpreted as they are no longer
            # interested in all variants. Remove all variants from their interests
            for variant in variants:
                if variant not in self.interests:
                    continue
                    
                # Provide the option to not remove variants from interests
                if options.get('ignore_variants') and variant != boss_name:
                    continue
                
                del self.interests[self.interests.index(variant)]

    def __repr__(self):
        return (
            f"Player(name={self.name}, max_damage_cap={self.max_damage_cap}, hp={self.hp}, "
            f"arcane_power={self.arcane_power}, availability={self.availability}, "
            f"experience={self.experience}), interests={self.interests}"
        )
