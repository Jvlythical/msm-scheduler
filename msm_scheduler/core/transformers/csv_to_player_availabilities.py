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
        'identity': row['Identity'],
        'monday': self._to_availabilities(row['Monday'] or ''),
        'thursday': self._to_availabilities(row['Thursday'] or ''),
        'tuesday': self._to_availabilities(row['Tuesday'] or ''),
        'wednesday': self._to_availabilities(row['Wednesday'] or '')
      })
    return availabilities

  def _to_availabilities(self, cell: str):
    availabilities = []
    for availability in cell.split(DELIMITTER):
      availabilities += self._replace_n_plus(availability).split(DELIMITTER)
    return availabilities

  def _replace_n_plus_func(self, match):
      # Extract the number before the "+" symbol
      n = int(match.group(1))
      # Generate the sequence from n to 23
      replacement = ",".join(str(i) for i in range(n, 24))
      return replacement

  def _replace_n_plus(self, s):
      # Function changes n+ to n,n+1,...,23
      if isinstance(s, int):
          return str(s)
      if s is None:
          return ""
      return re.sub(r"(\d+)\+", self._replace_n_plus_func, s)