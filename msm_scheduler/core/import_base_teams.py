import csv

from typing import List

from ..models import Player

PLAYER_NAMES_DELIMITTER = ','

def import_players(file_path: str) -> List[Player]:
    players = []

    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            boss_name = row['Boss Name']
            player_names = row['Player Names'].split(PLAYER_NAMES_DELIMITTER)
            time = row['Time'].lower()

            players.append({
                'boss_name': boss_name,
                'player_names': player_names,
                'time': time,
            })

    return players
