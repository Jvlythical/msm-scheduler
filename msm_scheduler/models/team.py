from typing import List

from ..typing import TeamParams

class Team:
    def __init__(self, **kwargs: TeamParams):
        self.boss = kwargs.get('boss')
        self.players = kwargs.get('players', [])
        self.availability = kwargs.get('availability', [])

    @property
    def boss(self):
        return self._boss

    @boss.setter
    def boss(self, value: Boss):
        if not isinstance(value, Boss):
            raise ValueError("boss must be an instance of Boss")
        self._boss = value

    @property
    def players(self):
        return self._players

    @players.setter
    def players(self, value: List[Player]):
        if not all(isinstance(player, Player) for player in value):
            raise ValueError("players must be a list of Player instances")
        self._players = value

    @property
    def availability(self):
        return self._availability

    @availability.setter
    def availability(self, value: List[str]):
        if not all(isinstance(day, str) for day in value):
            raise ValueError("All availability entries must be strings")
        self._availability = value

    def clear_probability(self) -

