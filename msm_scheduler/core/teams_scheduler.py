import pdb

from typing import List, Union

from ..models import Boss, Player, Team
from .boss_players import BossPlayers

class TeamsScheduler():

    def __init__(self, boss_players: BossPlayers, base_teams: List[Team]):
        self.boss_players = boss_players
        self.base_teams = base_teams
        self.fills = []

        self.__join_base_team_resources(base_teams)

        self.boss_teams_index = {}
        for team in self.base_teams:
            if team.boss_name not in self.boss_teams_index:
                self.boss_teams_index[team.boss_name] = []
            self.boss_teams_index[team.boss_name].append(team)

        self.player_teams_index = {}
        for player in self.players:
            self.player_teams_index[player.name] = []

        # Remove base team players from available boss players
        for team in self.base_teams:
            for player in team.players:
                self.boss_players.remove(team.boss_name, player.name)

    @property
    def base_teams(self) -> List[Team]:
        return self._base_teams

    @base_teams.setter
    def base_teams(self, value: List[Team]):
        self._base_teams = value

    @property
    def boss_teams_index(self):
        return self._boss_teams_index

    @boss_teams_index.setter
    def boss_teams_index(self, value: dict):
        self._boss_teams_index = value

    @property
    def bosses(self):
        return self.boss_players.bosses

    @property
    def bosses_index(self):
        return self.boss_players.bosses_index

    @property
    def players(self):
        return self.boss_players.players

    @property
    def players_index(self):
        return self.boss_players.players_index

    def assign_player(self, player: Player, team: Team):
        team.add_player(player)
        self.player_teams_index[player.name].append(team)

    def next_available_boss_team(self, boss_name: str, player: Player):
        availability = list(map(lambda team: team.availability, player.assigned_teams))
        teams: List[Team] = self.boss_teams_index[boss_name]
        for team in teams:
            if team.availability in availability:
                return team

        for team in teams:
            if team.player_available(player):
                return team

    def assign(self):
        # Sort bosses by difficulty, hardest first
        bosses = self.bosses.copy()
        bosses.sort(key=lambda boss: boss.total_max_damage_cap_required, reverse=True)

        for boss in bosses:
            print(f"=== Assigning teams for {boss.name}")
            print(boss)

            teams: List[Team] = self.boss_teams_index[boss.name]

            # Sort team with lowest clear_propability first
            teams.sort(key=lambda team: team.clear_probability())

            while True:
                player = self.boss_players.next_player(boss.name)

                if not player:
                    break

                assigned = False
                filled = False
                for team in teams:
                    if team.player_available(player):
                        assigned = True
                        self.assign_player(player, team)
                        break
                    
                    filled = filled and team.is_full()

                if not assigned:
                    print(f"{player.name} (availability {player.availability}) is not available to run")
                
                if filled:
                    break

    def __join_base_team_resources(self, base_teams: List[Team]):
        for team in base_teams:
            players = []
            for player_name in team.player_names:
                players.append(self.players_index[player_name])

            team.boss = self.bosses_index.get(team.boss_name)
            team.players = players