import os
import pdb
import sys

from ..core.boss_players import BossPlayers
from ..core.config import Config
from ..core.importers.file import FileImporter
from ..core.import_base_teams import import_base_teams_from_csv
from ..core.import_bosses import import_bosses_from_csv
from ..core.players_builder import PlayersBuilder
from ..core.teams_scheduler import TeamsScheduler
from ..models import Boss, Team

dirname = os.path.dirname(__file__)
config_path = os.path.join(dirname, 'fixtures', 'config.yml')
config = Config(config_path)
importer = FileImporter(config)

# Example usage
player_stats = importer.player_stats
player_availabilities = importer.player_availabilities
player_interests = importer.player_interests
player_experiences = importer.player_experiences
bosses = list(map(lambda row: Boss(**row),
              import_bosses_from_csv(config.bosses_csv_path)))
base_teams = list(map(lambda row: Team(**row),
                  import_base_teams_from_csv(config.base_teams_csv_path)))

builder = PlayersBuilder()
builder.with_availabilities(player_availabilities)
builder.with_experiences(player_experiences)
builder.with_interests(player_interests)
builder.with_stats(player_stats)
players = builder.build()

boss_players = BossPlayers(players=players, bosses=bosses)
scheduler = TeamsScheduler(boss_players, base_teams)
scheduler.assign()

for team in base_teams:
    print(f"=== {team.boss_name} Team at {team.time}, filled {len(team.players)}/{team.boss.capacity}")
    for player in team.players:
        print(f"{player.name}")
    print(f"\nClear probability: {team.clear_probability()}")

