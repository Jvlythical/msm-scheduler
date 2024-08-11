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
                arcane_power_requaired=int(row['Arcane Power Required']),
                capacity=int(row['Capacity']),
                experience_required=int(row['Experience']),
                hp_required=int(row['HP Required']),
                name=row['Name'],
                total_max_damage_cap_required=int(row['Total Max Damage Cap Required'])
            )
            boss = Boss(**boss_params)
            bosses.append(boss)
    return bosses
