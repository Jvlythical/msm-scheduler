import pdb

from typing import List

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
        self.__initialize_base_teams()

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

    def assign_player(self, player: Player, teams: List[Team]):
        player_teams: List[Team] = self.player_teams_index[player.name]

        for team in teams:
            if not team.player_available(player):
                continue

            if team.add_player(player):
                player_teams.append(team)
                break

    def assign_player_interests(self, player: Player):
        for boss_name in player.interests:
            teams = self.player_boss_teams(player, boss_name)
            self.assign_player(player, teams)

    def assign(self, verbose=True):
        # Sort bosses by difficulty, hardest first
        boss_names = list(map(lambda team: team.boss_name, self.base_teams))
        boss_names = set(boss_names)
        bosses: List[Boss] = list(map(lambda boss_name: self.bosses_index[boss_name], boss_names))
        bosses.sort(key=lambda boss: boss.total_max_damage_cap_required, reverse=True)

        for boss in bosses:
            if verbose:
                print(f"=== Assigning teams for {boss.name}")
                print("=== Boss Stats")
                print(boss)
                print("=== Boss Available Teams")
                for team in self.boss_teams(boss.name):
                    print(team)

            while True:
                player = self.boss_players.next_player(boss.name)
                # Continue while there are still players to assign
                if not player:
                    break

                teams: List[Team] = self.boss_teams(boss.name)
                self.assign_player(player, teams)
                self.assign_player_interests(player)

                filled = True
                for team in teams:
                    if not team.is_full():
                        filled = False
                        break

                # Continue while teams are not filled
                if filled:
                    break

    def boss_teams(self, boss_name: str):
        teams: List[Team] = self.boss_teams_index.get(boss_name)

        if not isinstance(teams, list):
            return []

        # Sort team with lowest clear_propability first
        teams.sort(key=lambda team: team.clear_probability())

        # # TESTING
        # teams.sort(key=lambda team: -len(team.player_names))

        return teams

    def player_boss_teams(self, player: Player, boss_name: str):
        player_teams: List[Team] = self.player_teams_index[player.name]
        availability = list(map(lambda team: team.time_by_day, player_teams))
        boss_teams: List[Team] = self.boss_teams(boss_name)

        # Find teams that are on the same days as when the player is already running
        teams = list(filter(lambda team: team.time_by_day in availability, boss_teams))

        if len(teams) == 0:
            return boss_teams

        return teams

    def __initialize_base_teams(self):
        # Since the player is already part of a base team,
        # they are no longer interested in running that boss
        for team in self.base_teams:
            for player in team.players:
                player.remove_interest(team.boss_name)

        # For the base team player's remaining interests, assign them a team
        for team in self.base_teams:
            for player in team.players:
                self.assign_player_interests(player)

    def __join_base_team_resources(self, base_teams: List[Team]):
        for team in base_teams:
            players = []
            for player_name in team.player_names:
                players.append(self.players_index[player_name])

            team.boss = self.bosses_index.get(team.boss_name)
            team.players = players
