from typing import TypedDict


class BossParams(TypedDict):
    capacity: int
    experience_required: int
    hp_required: int
    name: str
    total_max_damage_cap_required: int
