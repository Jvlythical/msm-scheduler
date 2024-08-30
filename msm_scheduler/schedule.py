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
from .models import Boss, Team

LOG_ID = 'Schedule'

def schedule():
    config = Config()
    database = Database(config)
    database.load_from_google_spreadsheet(GoogleSpreadSheetImporter(config.inputs_spreadsheet_id))
    database.load_from_file(FileImporter(config))

    # Settings
    importer = GoogleSpreadSheetImporter(config.settings_spreadsheet_id, SPREADSHEET_COLUMNS)
    tables = importer.get()
    database.right_merge_tables(tables)

    builder = PlayersBuilder()
    builder.with_availabilities(database.player_availabilities)
    builder.with_experiences(database.player_experiences)
    builder.with_interests(database.player_interests)
    builder.with_stats(database.player_stats)
    players = builder.build()

    bosses = list(map(lambda row: Boss(**row), database.bosses))
    base_teams = list(map(lambda row: Team(**row), database.base_teams))
    boss_players = BossPlayers(players=players, bosses=bosses)
    scheduler = TeamsScheduler(boss_players, base_teams)
    schedules = scheduler.assign()

    return schedules

if __name__ == '__main__':
    schedules = schedule()

    for _schedule in schedules:
        teams = _schedule.teams
        Logger.instance(LOG_ID).info(f"{bcolors.OKBLUE}{_schedule.boss_name} schedules\n{bcolors.ENDC}")

        for team in teams:
            Logger.instance(LOG_ID).info(f"{bcolors.OKCYAN}{team.time} filled {len(team.players)}/{team.boss.capacity}{bcolors.ENDC}")

            for player in team.players:
                print(f"{player.name}")

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
                print(f"{player.name}")
            print()
