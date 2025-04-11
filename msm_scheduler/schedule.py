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
from .lib.time_utils import get_next_timestamp, format_team_time
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
    base_teams = list(map(lambda row: Team(**row), database.base_teams))
    boss_players = BossPlayers(players=players, bosses=bosses)
    
    # Pass role configs to scheduler
    scheduler = TeamsScheduler(boss_players, base_teams, role_configs)
    schedules = scheduler.assign()

    return schedules

if __name__ == '__main__':
    schedules = schedule()

    for _schedule in schedules:
        teams = _schedule.teams
        Logger.instance(LOG_ID).info(f"{bcolors.OKBLUE}{_schedule.boss_name} schedules\n{bcolors.ENDC}")

        for team in teams:
            day, hour = team.time.split('.')
            timestamp = get_next_timestamp(day, int(hour))
            
            Logger.instance(LOG_ID).info(f"{bcolors.OKCYAN}{team.time} filled {len(team.players)}/{team.boss.capacity}{bcolors.ENDC}")
            Logger.instance(LOG_ID).info(format_team_time(team.time))

            for player, role_label in team.get_formatted_players():
                discord_tag = f"@{player.discord_id}" if player.discord_id else player.name
                print(f"{discord_tag} ({player.name}){role_label}")

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
