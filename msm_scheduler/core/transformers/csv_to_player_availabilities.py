import pdb
import re

DELIMITTER = ','

class CSVToPlayerAvailabilitiesTransformer():

  def __init__(self, rows):
    self.rows = list(rows) if hasattr(rows, '__iter__') else rows
    self.column_map = self._create_column_map()

  def _create_column_map(self):
    """Create mapping from day names to actual column headers"""
    if not self.rows:
      return {}
    
    column_map = {}
    first_row = self.rows[0]
    for column in first_row.keys():
      if column == 'Identity':
        continue
      day = self.extract_day(column)
      column_map[day] = column
    return column_map

  def extract_day(self, header: str) -> str:
    """Extract day name from header format like 'Monday-11/18'"""
    if '-' in header:
      return header.split('-')[0]
    return header

  def tranform(self):
    availabilities = []
    for row in self.rows:
      availabilities.append({
        'friday': self._to_availabilities(row[self.column_map.get('Friday', 'Friday')] or ''),
        'identity': (row['Identity'] or '').strip(),
        'monday': self._to_availabilities(row[self.column_map.get('Monday', 'Monday')] or ''),
        'saturday': self._to_availabilities(row[self.column_map.get('Saturday', 'Saturday')] or ''),
        'sunday': self._to_availabilities(row[self.column_map.get('Sunday', 'Sunday')] or ''),
        'thursday': self._to_availabilities(row[self.column_map.get('Thursday', 'Thursday')] or ''),
        'tuesday': self._to_availabilities(row[self.column_map.get('Tuesday', 'Tuesday')] or ''),
        'wednesday': self._to_availabilities(row[self.column_map.get('Wednesday', 'Wednesday')] or '')
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