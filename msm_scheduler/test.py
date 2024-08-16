import pdb

from .core.boss_players import BossPlayers
from .core.players_builder import PlayersBuilder
from .core.teams_scheduler import TeamsScheduler
from .core.import_player_data import import_player_data
from .core.import_bosses import import_bosses_from_csv
from .core.base_teams import construct_base_teams

bosses = import_bosses_from_csv("msm_scheduler/data/bosses.csv")
stats, availabilities, experiences = import_player_data()

players = PlayersBuilder(stats, availabilities, experiences).build()
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
