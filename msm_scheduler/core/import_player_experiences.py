import csv

from typing import List

from ..constants.boss import HARD_DAMIEN, LUCID, LOTUS, NORMAL_DAMIEN, WILL
from ..models import Player

def import_player_experiences_from_csv(file_path: str) -> List[Player]:
    experiences = []

    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            experience = {
                HARD_DAMIEN: int(row['Hard Damien']) if row['Hard Damien'] else 0,
                LOTUS: int(row['Lotus']) if row['Lotus'] else 0,
                LUCID: int(row['Lucid']) if row['Lucid'] else 0,
                'name': row['Name'],
                NORMAL_DAMIEN: int(row['Normal Damien']) if row['Normal Damien'] else 0,
                WILL: int(row['Will']) if row['Will'] else 0
            }

            experiences.append(experience)

    return experiences
