class CSVToPlayersTransformer():

  def __init__(self, rows):
    self.rows = rows

  def tranform(self):
    players = []
    for row in self.rows:
      arcane_power = int(row['Arcane Power']) if row['Arcane Power'] else 0
      hp = int(row['HP']) if row['HP'] else 0
      identity = (row['Identity'] or '').strip()
      max_damage_cap = float(row['Max Damage Cap']) if row['Max Damage Cap'] else 0
      name = (row['Name'] or '').strip()

      players.append({
        'arcane_power': arcane_power,
        'hp': hp,
        'identity': identity,
        'max_damage_cap': max_damage_cap,
        'name': name,
      })

    return players