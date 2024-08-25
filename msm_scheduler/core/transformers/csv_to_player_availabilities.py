import pdb
import re

DELIMITTER = ','

class CSVToPlayerAvailabilitiesTransformer():

  def __init__(self, rows):
    self.rows = rows

  def tranform(self):
    availabilities = []
    for row in self.rows:
      availabilities.append({
        'friday': self._to_availabilities(row['Friday'] or ''),
        'identity': (row['Identity'] or '').strip(),
        'monday': self._to_availabilities(row['Monday'] or ''),
        'saturday': self._to_availabilities(row['Saturday'] or ''),
        'sunday': self._to_availabilities(row['Sunday'] or ''),
        'thursday': self._to_availabilities(row['Thursday'] or ''),
        'tuesday': self._to_availabilities(row['Tuesday'] or ''),
        'wednesday': self._to_availabilities(row['Wednesday'] or '')
      })
    return availabilities

  def _to_availabilities(self, cell: str):
    availabilities = []
    for availability in cell.split(DELIMITTER):
      if availability == None:
        continue
      availabilities += self._replace_n_plus(availability.strip()).split(DELIMITTER)

    return list(filter(lambda time: not not time, availabilities))

  def _replace_n_plus_func(self, match):
      # Extract the number before the "+" symbol
      n = int(match.group(1))
      # Generate the sequence from n to 23
      replacement = DELIMITTER.join(str(i) for i in range(n, 24))
      return replacement

  def _replace_n_plus(self, s):
      # Function changes n+ to n,n+1,...,23
      if isinstance(s, int):
          return str(s)
      return re.sub(r"(\d+)\+", self._replace_n_plus_func, s)