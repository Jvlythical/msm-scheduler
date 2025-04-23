import pdb

from .constants.gapi import SPREADSHEET_COLUMNS
from .core.boss_players import BossPlayers
from .core.config import Config
from .core.database import Database
from .core.importers.file import FileImporter
from .core.importers.google_spreadsheet import GoogleSpreadSheetImporter
from .core.players_builder import PlayersBuilder
from .core.teams_scheduler import TeamsScheduler
from .lib.logger import bcolors, Logger
from .models import Boss, Team, RoleConfig
from .lib.time_utils import get_next_timestamp, format_team_time, parse_team_time
from .core.base_teams import construct_base_teams

LOG_ID = 'Schedule'

def schedule():
    config = Config()
    database = Database(config)
    
    # Load main player data
    database.load_from_google_spreadsheet(
        GoogleSpreadSheetImporter(config.inputs_spreadsheet_id)
    )
    database.load_from_file(FileImporter(config))

    # Load settings data
    if config.settings_spreadsheet_id:
        settings_importer = GoogleSpreadSheetImporter(
            config.settings_spreadsheet_id, 
            SPREADSHEET_COLUMNS
        )
        settings_tables = settings_importer.get()
        database.right_merge_tables(settings_tables)

    # Convert role configs to RoleConfig objects
    role_configs = [RoleConfig(**config) for config in database.role_configs]

    builder = PlayersBuilder()
    builder.with_availabilities(database.player_availabilities)
    builder.with_experiences(database.player_experiences)
    builder.with_interests(database.player_interests)
    builder.with_discord_ids(database.player_discord_ids)
    builder.with_stats(database.player_stats)
    players = builder.build()

    bosses = list(map(lambda row: Boss(**row), database.bosses))
    base_teams = []
    for row in database.base_teams:
        team = Team(**row)
        # Set team name to time if not provided
        if not team.team_name:
            team.team_name = team.time
        base_teams.append(team)
    
    boss_players = BossPlayers(players=players, bosses=bosses)
    
    # Pass role configs to scheduler
    scheduler = TeamsScheduler(boss_players, base_teams, role_configs)
    schedules = scheduler.assign()

    return schedules

if __name__ == '__main__':
    schedules = schedule()

    for _schedule in schedules:
        teams = _schedule.teams
        # Format boss name in Title Case and replace underscores with spaces
        formatted_boss_name = _schedule.boss_name.replace('_', ' ').title()
        Logger.instance(LOG_ID).info(f"{bcolors.OKBLUE}{formatted_boss_name} schedules\n{bcolors.ENDC}")

        for team in teams:
            # Get day from team time
            day, _, _ = parse_team_time(team.time)
            # Format team name as "Boss Name Day: TeamName"
            formatted_team_name = f"{formatted_boss_name} {day.capitalize()}: {team.team_name}"
            Logger.instance(LOG_ID).info(f"{bcolors.OKCYAN}{formatted_team_name}{bcolors.ENDC}")
            Logger.instance(LOG_ID).info(format_team_time(team.time, _schedule.boss_name))

            # Get formatted players
            formatted_players = list(team.get_formatted_players())
            
            # Add numbered entries for all players
            for i, (player, role_label) in enumerate(formatted_players, 1):
                discord_tag = f"@{player.discord_id}" if player.discord_id else player.name
                print(f"{i}. {discord_tag} ({player.name}){role_label}")
            
            # Add FILL entries for remaining slots
            for i in range(len(formatted_players) + 1, team.boss.capacity + 1):
                print(f"{i}. FILL")

            if len(team.availability_conflicts) > 0:
                Logger.instance(LOG_ID).warning(f"{bcolors.WARNING}Availability Conflicts{bcolors.ENDC}")
                for player in team.availability_conflicts:
                    print(f"{player.name}")

            if len(team.interest_conflicts) > 0:
                Logger.instance(LOG_ID).warning(f"{bcolors.WARNING}Interest Conflicts{bcolors.ENDC}")
                for player in team.interest_conflicts:
                    print(f"{player.name}")

            print()

        if len(_schedule.fills) > 0:
            Logger.instance(LOG_ID).info(f"{bcolors.OKGREEN}Fills{bcolors.ENDC}")
            for player in _schedule.fills:
                discord_tag = f"@{player.discord_id}" if player.discord_id else player.name
                print(f"{discord_tag} ({player.name})")
            print()
