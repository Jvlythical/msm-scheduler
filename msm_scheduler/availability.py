import os
import pdb

from typing import List

from .core.boss_players import BossPlayers
from .core.config import Config
from .core.database import Database
from .core.importers.file import FileImporter
from .core.importers.google_spreadsheet import GoogleSpreadSheetImporter
from .core.import_base_teams import import_base_teams_from_csv
from .core.import_bosses import import_bosses_from_csv
from .core.players_builder import PlayersBuilder
from .models import Boss, Player, Team

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
availability_distribution = boss_players.availability_distribution()

for boss_name in availability_distribution:
  times = availability_distribution[boss_name]
  print(f"=== {boss_name} availability distribution")

  sorted_times = list(times.keys())
  sorted_times.sort()
  for time in sorted_times:
    key = "{:<15}".format(time)
    print(f"{key}: {' '.join(times[time])}")

  print("")