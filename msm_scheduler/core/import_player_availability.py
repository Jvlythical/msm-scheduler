import csv

from typing import List

from ..models import Player

DELIMITTER = ','

def import_availability(file_path: str) -> List[Player]:
    availability = []

    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            availability.append({
                'friday': (row['Friday'] or '').split(DELIMITTER),
                'identity': row['Identity'],
                'monday': (row['Monday'] or '').split(DELIMITTER),
                'thursday': (row['Thursday'] or '').split(DELIMITTER),
                'tuesday': (row['Tuesday'] or '').split(DELIMITTER),
                'wednesday': (row['Wednesday'] or '').split(DELIMITTER)
            })

    return availability
