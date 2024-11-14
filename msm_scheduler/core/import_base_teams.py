import csv
import pdb

from typing import List

from ..models import Player

PLAYER_NAMES_DELIMITTER = ','

def import_base_teams_from_csv(file_path: str) -> List[Player]:
    players = []

    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            boss_name = row['Boss Name']
            fills = list(map(lambda data: data.strip(), row.get('Fills', '').split(PLAYER_NAMES_DELIMITTER)))
            player_names = list(map(lambda data: data.strip(), row['Player Names'].split(PLAYER_NAMES_DELIMITTER)))
            time = row['Time'].lower()

            players.append({
                'boss_name': boss_name,
                'fills': fills,
                'player_names': player_names,
                'time': time,
            })

    return players
