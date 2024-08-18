import pdb
import os
from typing import List

from ..core.boss_players import BossPlayers
from ..core.importers.google_spreadsheet import GoogleSpreadSheetImporter
from ..core.players_builder import PlayersBuilder
from ..core.teams_scheduler import TeamsScheduler
from ..core.database import Database
from ..core.import_bosses import import_bosses_from_csv
from ..core.base_teams import construct_base_teams
from ..models import Boss, Team, Player
from ..core.config import Config


def boss_interest_count(players: List[Player]):
    d = dict()
    for player in players:
        for interest in player.interests:
            d[interest] = d.get(interest, 0) + 1
    return d


def which_teams(player_identity: str, base_teams: List[Team]):
    # Usage:
    # print(which_teams("Model", base_teams))
    team_list = []
    for team in base_teams:
        team_ids = [p.identity for p in team.players]
        if player_identity in team_ids:
            team_list.append(team)
    return team_list


dirname = os.path.dirname(__file__)
config_path = os.path.join(dirname, 'fixtures', 'config.yml')
config = Config(config_path)

bosses = list(map(lambda row: Boss(**row), import_bosses_from_csv(config.bosses_csv_path)))
importer = GoogleSpreadSheetImporter()
database = Database(config)
database.load_from_google_spreadsheet(importer)

builder = PlayersBuilder()
builder.with_availabilities(database.player_availabilities)
builder.with_experiences(database.player_experiences)
builder.with_interests(database.player_interests)
builder.with_stats(database.player_stats)
players = builder.build()

base_teams = construct_base_teams(players)
boss_players = BossPlayers(players=players, bosses=bosses)
scheduler = TeamsScheduler(boss_players, base_teams)
scheduler.assign(verbose=False)

for idx, team in enumerate(base_teams):
    if len(team.player_names) != 10:
        continue
    # if len(team.player_names) == 0:
    #     continue
    # if team.boss.name != 'lotus':
    #     continue
    print(f"=== Team {idx+1} fighting {team.boss.name} on {team.time}")
    print(f"{[player.name for player in team.players]}")
    print(f"Clear probability: {team.clear_probability()}, Team MDC: {team.mdc}, Team Size: {team.size}")
    print('')
