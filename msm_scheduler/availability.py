import pdb

from .constants.gapi import SPREADSHEET_COLUMNS
from .core.boss_players import BossPlayers
from .core.config import Config
from .core.database import Database
from .core.importers.file import FileImporter
from .core.importers.google_spreadsheet import GoogleSpreadSheetImporter
from .core.players_builder import PlayersBuilder
from .lib.logger import bcolors, Logger
from .models import Boss

LOG_ID = 'Availability'

def build_boss_players():
  config = Config()
  database = Database(config)
  database.load_from_google_spreadsheet(GoogleSpreadSheetImporter())
  database.load_from_file(FileImporter(config))

    # Settings
  importer = GoogleSpreadSheetImporter(config.settings_spreadsheet_id, SPREADSHEET_COLUMNS)
  tables = importer.get()
  bosses = list(map(lambda row: Boss(**row), tables[4]))

  builder = PlayersBuilder()
  builder.with_availabilities(database.player_availabilities)
  builder.with_experiences(database.player_experiences)
  builder.with_interests(database.player_interests)
  builder.with_stats(database.player_stats)
  players = builder.build()

  boss_players = BossPlayers(players=players, bosses=bosses)
  return boss_players

if __name__ == '__main__':
  boss_players = build_boss_players()
  availability_distribution = boss_players.availability_distribution()

  for boss_name in availability_distribution:
    Logger.instance(LOG_ID).info(f"{bcolors.OKBLUE}{boss_name} availability distribution{bcolors.ENDC}")
    Logger.instance(LOG_ID).info(f"{bcolors.OKCYAN}There are {len(boss_players.get(boss_name))} available players{bcolors.ENDC}")

    times = availability_distribution[boss_name]

    sorted_times = list(times.keys())
    sorted_times.sort()
    for time in sorted_times:
      key = "{:<15}".format(time)
      print(f"{key}: {' '.join(times[time])}")

    print("")