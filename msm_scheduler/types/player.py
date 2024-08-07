from typing import TypedDict

class Experience(TypedDict):
    hard_damien: int
    lucid: int
    lotus: int
    normal_damien: int
    will: int

class PlayerParams(TypedDict):
    name: str
    max_damage_cap: int
    hp: int
    arcane_power: int
    availability: List[str]
    experience: Experience
