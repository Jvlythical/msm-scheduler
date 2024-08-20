import pdb

from ..constants.boss import HARD_DAMIEN
from ..core.boss_players import BossPlayers
from ..core.players_builder import PlayersBuilder
from ..core.teams_scheduler import TeamsScheduler
from ..models import Boss, Team

# Example usage
base_teams = [
    Team(time="monday.18", boss_name=HARD_DAMIEN, player_names=[]),
    Team(time="tuesday.19", boss_name=HARD_DAMIEN, player_names=[])
]
bosses = [
    Boss(name=HARD_DAMIEN, total_max_damage_cap_required=400, difficulty=10,
         clear_probability=75, availability=["Monday", "Wednesday"], capacity=3, hp_required=80)
]

player_stats = [
    {'arcane_power': 50, 'hp': 50, 'identity': '1',
        'max_damage_cap': 200, 'name': 'Archer'},
    {'arcane_power': 70, 'hp': 80, 'identity': '2',
        'max_damage_cap': 150, 'name': 'Mage'},
    {'arcane_power': 60, 'hp': 90, 'identity': '3',
        'max_damage_cap': 180, 'name': 'Rogue'},
    {'arcane_power': 50, 'hp': 100, 'identity': '4',
        'max_damage_cap': 200, 'name': 'Warrior'},
]

player_availabilities = [
    {'friday': [], 'identity': '1', 'monday': ['18'], 'saturday': [],
        'sunday': [], 'thursday': [], 'tuesday': [], 'wednesday': []},
    {'friday': [], 'identity': '2', 'monday': [], 'saturday': [],
        'sunday': [], 'thursday': [], 'tuesday': ['19'], 'wednesday': []},
    {'friday': [], 'identity': '3', 'monday': [], 'saturday': [],
        'sunday': [], 'thursday': [], 'tuesday': [], 'wednesday': ['18']},
    {'friday': [], 'identity': '4', 'monday': ['18'], 'saturday': [],
        'sunday': [], 'thursday': [], 'tuesday': [], 'wednesday': []},
]

player_experiences = [
    {'name': 'Archer', 'hard_damien': 4},
    {'name': 'Mage', 'hard_damien': 8},
    {'name': 'Rogue', 'hard_damien': 6},
    {'name': 'Warrior', 'hard_damien': 10},
]

player_interests = [
    {'name': 'Archer', 'hard_damien': 'Y'},
    {'name': 'Mage', 'hard_damien': 'Y'},
    {'name': 'Rogue', 'hard_damien': 'Y'},
    {'name': 'Warrior', 'hard_damien': 'Y'},
]

builder = PlayersBuilder()
builder.with_availabilities(player_availabilities)
builder.with_experiences(player_experiences)
builder.with_interests(player_interests)
builder.with_stats(player_stats)
players = builder.build()

boss_players = BossPlayers(players=players, bosses=bosses)
scheduler = TeamsScheduler(boss_players, base_teams)
scheduler.assign()

for idx, team in enumerate(base_teams):
    print(f"=== Team {idx+1}")
    print(f"{[player for player in team.players]}")
    print(f"Clear probability: {team.clear_probability()}")
