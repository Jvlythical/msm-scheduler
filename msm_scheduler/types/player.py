from typing import List, TypedDict, Union

class PlayerAvailability(TypedDict):
    friday: List[str]
    identity: str
    monday: List[str]
    saturday: List[str]
    sunday: List[str]
    thursday: List[str]
    tuesday: List[str]
    wednesday: List[str]

class PlayerExperience(TypedDict):
    hard_damien: Union[int, None]
    lucid: Union[int, None]
    lotus: Union[int, None]
    normal_damien: Union[int, None]
    will: Union[int, None]

class PlayerStats(TypedDict):
    arcane_power: int
    hp: int
    identity: Union[str, None]
    max_damage_cap: int
    name: str

class PlayerParams(TypedDict):
    name: str
    max_damage_cap: int
    hp: int
    identity: Union[str, None]
    arcane_power: int
    availability: List[str]
    experiences: PlayerExperience
