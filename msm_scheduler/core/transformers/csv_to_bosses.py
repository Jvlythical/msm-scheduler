from ...models import Boss
from ...types.boss import BossParams


class CSVToBossesTransformer():

    def __init__(self, rows):
        self.rows = rows

    def tranform(self):
        bosses = []

        for row in self.rows:
            boss_params = BossParams(
                arcane_power_required=int(row['Arcane Power Required']) if row['Arcane Power Required'] else 0,
                capacity=int(row['Capacity']) if row['Capacity'] else 0,
                difficulty=int(row['Difficulty']) if row['Difficulty'] else 0,
                hp_required=int(row['HP Required']) if row['HP Required'] else 0,
                name=row['Name'],
                total_max_damage_cap_required=int(row['Total Max Damage Cap Required']) if row['Total Max Damage Cap Required'] else 1
            )
            bosses.append(boss_params)

        return bosses

