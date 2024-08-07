from typing import List, TypedDict

class BossParams(TypedDict):
    availability: List[str]
    capacity: int
    clear_probability: int
    experience: int
    hp_required: int
    name: str
    total_max_damage_cap_required: int
