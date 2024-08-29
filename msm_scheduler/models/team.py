import numpy as np
import pdb

from typing import List

from ..constants.boss import VALID_BOSSES
from ..types import TeamParams
from .boss import Boss
from .player import Player
from ..core.team_clear_prbs import TeamClearProbabilityModel


class Team:
    def __init__(self, **kwargs: TeamParams):
        self.time = kwargs.get('time')
        self.boss = None
        self.boss_name = kwargs.get('boss_name')
        self.players = [] # This has to be set first otherwise self.player_names will be cleared
        self.player_names = kwargs.get('player_names', [])
        self.tcpm = TeamClearProbabilityModel()
        # self.tcpm.fit()

    @property
    def time(self):
        return self._time

    @property
    def time_by_day(self):
        return self._time.split('.')[0]

    @time.setter
    def time(self, value: List[str]):
        if not isinstance(value, str):
            raise ValueError("Time must be a string")
        self._time = value

    @property
    def boss(self):
        return self._boss

    @boss.setter
    def boss(self, value: Boss):
        self._boss = value

    @property
    def boss_name(self):
        return self._boss_name

    @boss_name.setter
    def boss_name(self, value: str):
        if value not in VALID_BOSSES:
            raise ValueError(
                f"boss_name {value} must be from of the valid boss_names {VALID_BOSSES}")
        self._boss_name = value

    @property
    def player_names(self):
        return self._player_names

    @player_names.setter
    def player_names(self, value: List[str]):
        if not all(isinstance(day, str) for day in value):
            raise ValueError("All player entries must be strings")
        self._player_names = value

    @property
    def players(self):
        return self._players

    @players.setter
    def players(self, value: List[Player]):
        self._players = value
        self._player_names = list(map(lambda player: player.name, value))

        for player in value:
            player.remove_availability(self.time)
            player.remove_interest(self.boss_name)

    def add_player(self, player: Player):
        if self.size >= self.boss.capacity:
            return False

        self._players.append(player)
        self.player_names.append(player.name)
        player.remove_availability(self.time)
        player.remove_interest(self.boss_name)

        return True

    @property
    def experience(self):
        team_experience = 0
        if len(self.players) == 0:
            return 0
        for player in self.players:
            team_experience += player.boss_experience(self.boss)
        return team_experience / len(self.players)

    @property
    def mdc(self):
        team_mdc = 0
        for player in self.players:
            team_mdc += player.max_damage_cap
        return team_mdc

    @property
    def size(self):
        return len(self.players)

    def clear_probability(self):
        if self.size == 0:
            return 0
        e = self.experience
        d = self.boss.difficulty
        m0 = self.boss.total_max_damage_cap_required
        m = self.mdc
        return self.tcpm.transform(e, d, m0, m)

    # def clear_probability(self):
    #     e = self.experience
    #     d = self.boss.difficulty
    #
    #     x = self.mdc / self.boss.total_max_damage_cap_required
    #     k = 0.5 * e + 0.3 * d - 2
    #     x0 = 0.2 * e + 0.1 * d - 0.5
    #
    #     return round(self._logistic(x, k, x0), 2)
    # def _logistic(self, x, k, x0):
    #     return 1 / (1 + np.exp(-k * (x - x0)))

    def is_full(self):
        if not self.boss:
            return True
        return self.size >= self.boss.capacity

    def player_available(self, player: Player):
        for assigned_player in self.players:
            if player.identity == assigned_player.identity:
                return False
        return self.time in player.availability

    def __repr__(self):
        return (f"Team(boss_name={self.boss_name}, player_names={self.player_names}, "
                f"time={self.time})")
