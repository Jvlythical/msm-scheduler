import pdb

from typing import List

PLAYER_NAMES_DELIMITTER = ','

class CSVToBaseTeamsTransformer():

    def __init__(self, rows):
        self.rows = rows

    def tranform(self):
      base_teams = []

      for row in self.rows:
        boss_name = (row['Boss Name'] or '').strip()
        fills = list(map(lambda data: data.strip(), row.get('Fills', '').split(PLAYER_NAMES_DELIMITTER)))
        fills = self.__remove_empty(fills)
        player_names = list(map(lambda data: data.strip(), row['Player Names'].split(PLAYER_NAMES_DELIMITTER)))
        player_names = self.__remove_empty(player_names)
        time = row['Time'].lower()

        base_teams.append({
            'boss_name': boss_name,
            'fills': fills,
            'player_names': player_names,
            'time': time,
        })
      return base_teams

    def __remove_empty(self, l: List[str]):
      return list(filter(lambda e: not not e, l))
