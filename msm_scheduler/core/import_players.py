import csv
from typing import List

from ..types import Player

def import_players(file_path: str) -> List[Player]:
    players = []

    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            name = row['name']
            max_damage_cap = int(row['max_damage_cap'])
            hp = int(row['hp'])
            arcane_power = int(row['arcane_power'])
            availability = row['availability'].split(',')
            experience = {
                'hard_damien': int(row['hard_damien']),
                'lucid': int(row['lucid']),
                'lotus': int(row['lotus']),
                'normal_damien': int(row['normal_damien']),
                'will': int(row['will'])
            }
            player = Player(
                name=name,
                max_damage_cap=max_damage_cap,
                hp=hp,
                arcane_power=arcane_power,
                availability=availability,
                experience=experience
            )
            players.append(player)

    return players
