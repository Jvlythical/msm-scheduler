import pdb

from ..core.boss_players import BossPlayers
from ..core.importers.google_spreadsheet import GoogleSpreadSheetImporter
from ..core.players_builder import PlayersBuilder
from ..core.teams_scheduler import TeamsScheduler
from ..core.database import Database
from ..core.import_bosses import import_bosses_from_csv
from ..core.base_teams import construct_base_teams
from ..models import Boss

bosses = import_bosses_from_csv("msm_scheduler/tests/fixtures/bosses.csv")

bosses = list(map(lambda row: Boss(**row), bosses))
importer = GoogleSpreadSheetImporter()
database = Database(importer)

builder = PlayersBuilder()
builder.with_availabilities(database.player_availabilities)
builder.with_experiences(database.player_experiences)
builder.with_interests(database.player_interests)
builder.with_stats(database.player_stats)
players = builder.build()


base_teams = construct_base_teams(players)
boss_players = BossPlayers(players=players, bosses=bosses)
scheduler = TeamsScheduler(boss_players, base_teams)
scheduler.assign()

for idx, team in enumerate(base_teams):
    print(f"=== Team {idx+1} at {team.time}")
    print(f"{[player.name for player in team.players]}")
    print(f"Clear probability: {
          team.clear_probability()}, Team MDC: {team.mdc}")
    print('')
