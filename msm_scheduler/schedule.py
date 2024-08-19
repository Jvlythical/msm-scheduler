import pdb

from .core.boss_players import BossPlayers
from .core.config import Config
from .core.database import Database
from .core.importers.file import FileImporter
from .core.importers.google_spreadsheet import GoogleSpreadSheetImporter
from .core.import_base_teams import import_base_teams_from_csv
from .core.import_bosses import import_bosses_from_csv
from .core.players_builder import PlayersBuilder
from .core.teams_scheduler import TeamsScheduler
from .lib.logger import bcolors, Logger
from .models import Boss, Team

LOG_ID = 'Schedule'

config = Config()
database = Database(config)
database.load_from_google_spreadsheet(GoogleSpreadSheetImporter())
database.load_from_file(FileImporter(config))

bosses = list(map(lambda row: Boss(**row),
              import_bosses_from_csv(config.bosses_csv_path)))
base_teams = list(map(lambda row: Team(**row),
                  import_base_teams_from_csv(config.base_teams_csv_path)))

builder = PlayersBuilder()
builder.with_availabilities(database.player_availabilities)
builder.with_experiences(database.player_experiences)
builder.with_interests(database.player_interests)
builder.with_stats(database.player_stats)
players = builder.build()

boss_players = BossPlayers(players=players, bosses=bosses)
scheduler = TeamsScheduler(boss_players, base_teams)
scheduler.assign()

for team in base_teams:
    Logger.instance(LOG_ID).info(f"{bcolors.OKBLUE}{team.boss_name} team at {team.time}{bcolors.ENDC}")
    Logger.instance(LOG_ID).info(f"{bcolors.OKCYAN}Filled {len(team.players)}/{team.boss.capacity}{bcolors.ENDC}")
    for player in team.players:
        print(f"{player.name}")
    print(f"\nClear probability: {team.clear_probability()}")