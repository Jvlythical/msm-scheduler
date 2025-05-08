import numpy as np
import pdb
from typing import List, Optional

from ..constants.boss import VALID_BOSSES
from ..core.team_clear_prbs import TeamClearProbabilityModel
from ..types import TeamParams
from .boss import Boss
from .player import Player
from ..core.team_roles import TeamRoles
from ..lib.time_utils import parse_team_time

class Team:
    def __init__(self, **kwargs: TeamParams):
        self.time = kwargs.get('time')
        self.database = kwargs.get('database')
        self.availability_conflicts: List[Player] = []
        self.boss = None
        self.boss_name = kwargs.get('boss_name')
        self.fills = kwargs.get('fills', []) 
        self.interest_conflicts: List[Player] = []
        self.players: List[Player] = [] # This has to be set first otherwise self.player_names will be cleared
        self.player_names = kwargs.get('player_names', [])
        self.tcpm = TeamClearProbabilityModel()
        # self.tcpm.fit()
        self._roles = None
        self.team_name = kwargs.get('team_name', self.time)

    @property
    def time(self) -> str:
        return self._time

    @time.setter
    def time(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Time must be a string")
        # Validate the time format
        parse_team_time(value)  # This will raise ValueError if format is invalid
        self._time = value

    @property
    def time_by_day(self) -> str:
        day, _, _ = parse_team_time(self._time)
        return day

    @property
    def alternative_players(self):
        return self._alternative_players

    @alternative_players.setter
    def alternative_players(self, value: List[Player]):
        self._alternative_players = value
        self._fills = list(map(lambda player: player.name, value))

        for player in value:
            try:
                player.remove_interest(self.boss_name, ignore_variants=True)
            except RuntimeError:
                # For fills we don't care if they are interested
                pass

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
    def fills(self):
        return self._fills

    @fills.setter
    def fills(self, value: List[str]):
        if not all(isinstance(fill, str) for fill in value):
            raise ValueError("All player entries must be strings")
        self._fills = value

    @property
    def player_names(self):
        return self._player_names

    @player_names.setter
    def player_names(self, value: List[str]):
        if not all(isinstance(player, str) for player in value):
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
            try:
                player.remove_availability(self.time)
            except RuntimeError:
                self.availability_conflicts.append(player)

            try:
                player.remove_interest(self.boss_name)
            except RuntimeError:
                self.interest_conflicts.append(player)

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

    @property
    def roles(self) -> TeamRoles:
        if not self._roles and self.boss and self.boss_name in ['hard_damien', 'normal_damien']:
            # Debug print role configs
            print(f"Creating TeamRoles for {self.boss_name} with role configs: {self.database.role_configs if hasattr(self, 'database') else 'No database'}")
            role_configs = []
            if hasattr(self, 'database') and hasattr(self.database, 'role_configs'):
                role_configs = self.database.role_configs
            self._roles = TeamRoles(self.players, self.boss, role_configs)
        return self._roles

    def get_formatted_players(self) -> List[tuple[Player, str]]:
        """Returns players with their role labels"""
        if not self.roles:
            return [(p, '') for p in self.players]
            
        ordered = self.roles.get_ordered_players()
        return [(p, f" - {'/'.join(roles)}" if roles else '') for p, roles in ordered]

    @property
    def team_name(self) -> str:
        return self._team_name

    @team_name.setter
    def team_name(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Team name must be a string")
        self._team_name = value

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        self._timestamp = value

    def __repr__(self):
        return (f"Team(boss_name={self.boss_name}, player_names={self.player_names}, "
                f"time={self.time})")

    def __str__(self) -> str:
        return f"{self.team_name} - {self.boss_name} ({len(self.players)}/{self.boss.capacity if self.boss else 0})"
