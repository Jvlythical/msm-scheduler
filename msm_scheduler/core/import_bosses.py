import csv
from typing import List

from ..types import Boss

def import_bosses_from_csv(filename: str) -> List[Boss]:
    bosses = []
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            boss_params = BossParams(
                availability=row['availability'].split(';'),  # Assuming availability is a semicolon-separated string
                capacity=int(row['capacity']),
                clear_probability=int(row['clear_probability']),
                experience=int(row['experience']),
                hp_required=int(row['hp_required']),
                name=row['name'],
                total_max_damage_cap_required=int(row['total_max_damage_cap_required'])
            )
            boss = Boss(**boss_params)
            bosses.append(boss)
    return bosses

