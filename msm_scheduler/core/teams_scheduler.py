import pdb

from typing import Callable, Dict, List, Optional

from ..lib.logger import bcolors, Logger
from ..models import Boss, Player, Team, RoleConfig
from .boss_players import BossPlayers
from .schedule import Schedule
from .team_roles import TeamRoles
from ..lib.time_utils import parse_team_time, get_next_timestamp

LOG_ID = 'TeamsScheduler'

class TeamsScheduler():

    def __init__(self, boss_players: BossPlayers, base_teams: List[Team], role_configs: Optional[Dict] = None):
        self.boss_players = boss_players
        self.base_teams = base_teams
        self.role_configs = role_configs or {}
        self.fills = []
        self._processed_teams = set()

        self.__join_base_team_resources(base_teams)
        
        self.boss_schedules_index: Dict[str, Schedule] = {}
        for team in self.base_teams:
            if team.boss_name not in self.boss_schedules_index:
                self.boss_schedules_index[team.boss_name] = Schedule(team.boss_name, [])
            self.boss_schedules_index[team.boss_name].add_team(team)

        self.player_teams_index: Dict[str, Player] = {}
        for player in self.players:
            self.player_teams_index[player.name] = []

        self.__assign_base_team_fills()
        self.__assign_base_team_interests()

    @property
    def base_teams(self) -> List[Team]:
        return self._base_teams

    @base_teams.setter
    def base_teams(self, value: List[Team]):
        self._base_teams = value

    @property
    def boss_schedules_index(self):
        return self._boss_schedules_index

    @boss_schedules_index.setter
    def boss_schedules_index(self, value: dict):
        self._boss_schedules_index = value

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
        assigned = False
        player_teams: List[Team] = self.player_teams_index[player.name]

        Logger.instance(LOG_ID).info(f"{bcolors.OKBLUE}Attempting to assign {player.name} to teams{bcolors.ENDC}")
        Logger.instance(LOG_ID).info(f"Player availability: {player.availability}")

        for team in teams:
            Logger.instance(LOG_ID).info(f"Checking team {team.team_name} at {team.time}")
            
            if not team.player_available(player):
                Logger.instance(LOG_ID).warning(f"{bcolors.WARNING}{player.name} not available for team {team.team_name} at {team.time}{bcolors.ENDC}")
                continue

            if team.add_player(player):
                assigned = True
                player_teams.append(team)
                Logger.instance(LOG_ID).info(f"{bcolors.OKGREEN}Successfully assigned {player.name} to team {team.team_name} at {team.time}{bcolors.ENDC}")
                break
            else:
                Logger.instance(LOG_ID).warning(f"{bcolors.WARNING}Failed to add {player.name} to team {team.team_name} at {team.time}{bcolors.ENDC}")

        if not assigned:
            Logger.instance(LOG_ID).warning(f"{bcolors.WARNING}Could not assign {player.name} to any team{bcolors.ENDC}")
            
        return assigned

    def assign_player_interests(self, player: Player):
        for boss_name in player.interests:
            boss = self.bosses_index[boss_name]
            if not player.boss_ready(boss):
                continue
            teams = self.player_schedule_teams(player, boss_name)
            self.assign_player(player, teams)

    def assign(self):
        # Sort bosses by difficulty, hardest first
        boss_names = list(map(lambda team: team.boss_name, self.base_teams))
        boss_names = set(boss_names)
        bosses: List[Boss] = list(map(lambda boss_name: self.bosses_index[boss_name], boss_names))
        bosses.sort(key=lambda boss: boss.total_max_damage_cap_required, reverse=True)

        for boss in bosses:
            schedule = self.boss_schedules_index.get(boss.name)
            if not schedule: 
                continue

            Logger.instance(LOG_ID).info(f"{bcolors.OKBLUE}Assigning teams for {boss.name}{bcolors.ENDC}")
            Logger.instance(LOG_ID).info(boss)
            Logger.instance(LOG_ID).info(f"{bcolors.OKCYAN}Boss Available Teams{bcolors.ENDC}")
            for team in self.schedule_teams(boss.name):
                Logger.instance(LOG_ID).info(team)

            while True:
                player = self.boss_players.next_player(boss.name)
                # Continue while there are still players to assign
                if not player:
                    break

                teams: List[Team] = self.schedule_teams(boss.name)
                if self.assign_player(player, teams):
                    self.assign_player_interests(player)
                else:
                    schedule.add_fill(player)

                # Check if all teams are full
                all_teams_full = True
                for team in teams:
                    if not team.is_full():
                        all_teams_full = False
                        break

                # Only break if all teams are full
                if all_teams_full:
                    break
                    
        # Add remaining players as fills for the boss
        schedules = list(self.boss_schedules_index.values())
        for schedule in schedules:
            while True:
                player = self.boss_players.next_player(schedule.boss_name)
                if not player:
                    break
                schedule.add_fill(player)

        # After all teams are filled, assign roles to each team
        for schedule in schedules:
            for team in schedule.teams:
                if team.boss and team.boss_name in ['hard_damien', 'normal_damien']:
                    # Create TeamRoles with all available players
                    team._roles = TeamRoles(team.players, team.boss, self.role_configs)

        return schedules

    def schedule_teams(self, boss_name: str):
        schedule: Schedule = self.boss_schedules_index.get(boss_name)
        if not schedule:
            return []

        handler: Callable[[Team], None] = lambda team: team.clear_probability()

        # Sort team with lowest clear_propability first
        return schedule.sorted_teams(handler)

    def player_schedule_teams(self, player: Player, boss_name: str):
        player_teams: List[Team] = self.player_teams_index[player.name]
        availability = list(map(lambda team: team.time_by_day, player_teams))
        schedule_teams: List[Team] = self.schedule_teams(boss_name)

        # Find teams that are on the same days as when the player is already running
        teams = list(filter(lambda team: team.time_by_day in availability, schedule_teams))

        if len(teams) == 0:
            return schedule_teams

        return teams

    def __assign_base_team_interests(self):
        # For the base team player's remaining interests, assign them a team
        for team in self.base_teams:
            for player in team.players:
                self.assign_player_interests(player)

    def __assign_base_team_fills(self):
        # For the base team player's remaining interests, assign them a team
        for team in self.base_teams:
            schedule: Schedule = self.boss_schedules_index[team.boss_name]
            for player in team.alternative_players:
                schedule.add_fill(player)

    def __join_base_team_resources(self, base_teams: List[Team]):
        for team in base_teams:
            players = []
            for player_name in team.player_names:
                players.append(self.players_index[player_name])

            alternative_players = []
            for player_name in team.fills:
                alternative_players.append(self.players_index[player_name])

            team.boss = self.bosses_index.get(team.boss_name)
            team.players = players
            team.alternative_players = alternative_players

    def schedule(self) -> List[Team]:
        for team in self.base_teams:
            if team.time in self._processed_teams:
                continue
            self._processed_teams.add(team.time)
            self._schedule_team(team)
        return self.base_teams

    def _schedule_team(self, team: Team):
        day, hour, minutes = parse_team_time(team.time)
        timestamp = get_next_timestamp(day, hour, minutes)
        team.timestamp = timestamp

        # Find available bosses for this time
        available_bosses = [b for b in self.bosses if b.is_available_at(timestamp)]
        if not available_bosses:
            return

        # Sort bosses by priority and assign the highest priority available boss
        available_bosses.sort(key=lambda b: b.priority, reverse=True)
        team.boss = available_bosses[0]
        team.boss_name = team.boss.name

        # Assign roles after boss is set
        if self.role_configs:
            team._roles = TeamRoles(team, self.role_configs)