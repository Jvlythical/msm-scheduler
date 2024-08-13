import pdb
import sys

from .core.boss_players import BossPlayers
from .core.import_base_teams import import_base_teams_from_csv
from .core.import_bosses import import_bosses_from_csv
from .core.import_players import import_players_from_csv
from .core.import_player_availabilities import import_player_availabilities_from_csv
from .core.import_player_experiences import import_player_experiences_from_csv
from .core.players_builder import PlayersBuilder
from .core.teams_scheduler import TeamsScheduler
from .models import Boss, Team

# Example usage
player_stats = import_players_from_csv(sys.argv[1])
player_availabilities = import_player_availabilities_from_csv(sys.argv[2])
player_experiences = import_player_experiences_from_csv (sys.argv[3])
bosses = list(map(lambda row: Boss(**row), import_bosses_from_csv(sys.argv[4])))
base_teams = list(map(lambda row: Team(**row), import_base_teams_from_csv(sys.argv[5])))

players = PlayersBuilder(player_stats, player_availabilities, player_experiences).build()

boss_players = BossPlayers(players=players, bosses=bosses)
scheduler = TeamsScheduler(boss_players, base_teams)
scheduler.assign()

for team in base_teams:
    print(f"=== {team.boss_name} Team at {team.time}, filled {len(team.players)}/{team.boss.capacity}")
    for player in team.players:
        print(f"{player.name}")
    print(f"\nClear probability: {team.clear_probability()}")