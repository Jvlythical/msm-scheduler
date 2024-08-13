import csv

from typing import List

from ..models import Boss
from ..types import BossParams

def import_bosses_from_csv(filename: str) -> List[Boss]:
    bosses = []
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            boss_params = BossParams(
                arcane_power_requaired=int(row['Arcane Power Required']) if row['Arcane Power Required'] else 0,
                capacity=int(row['Capacity']) if row['Capacity'] else 0,
                experience_required=int(row['Experience Required']) if row['Experience Required'] else 0,
                hp_required=int(row['HP Required']) if row['HP Required'] else 0,
                name=row['Name'],
                total_max_damage_cap_required=int(row['Total Max Damage Cap Required']) if row['Total Max Damage Cap Required'] else 1
            )
            bosses.append(boss_params)
    return bosses
