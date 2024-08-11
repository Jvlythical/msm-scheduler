import csv

from typing import List

from ..models import Player

def import_players(file_path: str) -> List[Player]:
    players = []

    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            arcane_power = int(row['Arcane Power'])
            hp = int(row['HP'])
            identity = int(row['Identity'])
            max_damage_cap = int(row['Max Damage Cap'])
            name = row['Name']

            players.append({
                'arcane_power': arcane_power,
                'hp': hp,
                'identity': identity,
                'max_damage_cap': max_damage_cap,
                'name': name,
            })

    return players
