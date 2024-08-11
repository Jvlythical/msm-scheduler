import csv

from typing import List

from ..constants.boss import HARD_DAMIEN, LUCID, LOTUS, NORMAL_DAMIEN, WILL
from ..models import Player

def import_players(file_path: str) -> List[Player]:
    experiences = []

    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            experience = {
                HARD_DAMIEN: int(row['Hard Damien']),
                LOTUS: int(row['Lotus']),
                LUCID: int(row['Lucid']),
                'name': row['Name'],
                NORMAL_DAMIEN: int(row['Normal Damien']),
                WILL: int(row['Will'])
            }

            experiences.append(experience)

    return experiences
