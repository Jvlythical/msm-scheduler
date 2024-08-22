PLAYER_NAMES_DELIMITTER = ','

class CSVToBaseTeamsTransformer():

    def __init__(self, rows):
        self.rows = rows

    def tranform(self):
      base_teams = []

      for row in self.rows:
        boss_name = row['Boss Name']
        player_names = list(map(lambda data: data.strip(), row['Player Names'].split(PLAYER_NAMES_DELIMITTER)))
        time = row['Time'].lower()

        base_teams.append({
            'boss_name': boss_name,
            'player_names': player_names,
            'time': time,
        })
      return base_teams
