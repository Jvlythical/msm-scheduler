class CSVToPlayersTransformer():

  def __init__(self, rows):
    self.rows = rows

  def tranform(self):
    players = []
    for row in self.rows:
      arcane_power = int(row['Arcane Power']) if row['Arcane Power'] else 0
      hp = int(row['HP'])
      identity = row['Identity']
      max_damage_cap = float(row['Max Damage Cap'])
      name = row['Name']

      players.append({
        'arcane_power': arcane_power,
        'hp': hp,
        'identity': identity,
        'max_damage_cap': max_damage_cap,
        'name': name,
      })

    return players