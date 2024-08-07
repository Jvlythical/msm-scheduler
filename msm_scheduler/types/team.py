from typing import List, TypedDict

from .boss import Boss
from .player import Player

class TeamParams(TypedDict):
    boss: Boss
    players: List[Player]
    availability: List[str]
