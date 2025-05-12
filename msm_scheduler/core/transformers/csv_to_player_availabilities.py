import pdb
import re
from ...lib.logger import Logger, bcolors

DELIMITTER = ','
LOG_ID = 'CSVToPlayerAvailabilities'

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
      identity = (row['Identity'] or '').strip()
      Logger.instance(LOG_ID).info(f"{bcolors.OKBLUE}Processing availabilities for {identity}{bcolors.ENDC}")
      
      availability = {
        'friday': self._to_availabilities(row[self.column_map.get('Friday', 'Friday')] or ''),
        'identity': identity,
        'monday': self._to_availabilities(row[self.column_map.get('Monday', 'Monday')] or ''),
        'saturday': self._to_availabilities(row[self.column_map.get('Saturday', 'Saturday')] or ''),
        'sunday': self._to_availabilities(row[self.column_map.get('Sunday', 'Sunday')] or ''),
        'thursday': self._to_availabilities(row[self.column_map.get('Thursday', 'Thursday')] or ''),
        'tuesday': self._to_availabilities(row[self.column_map.get('Tuesday', 'Tuesday')] or ''),
        'wednesday': self._to_availabilities(row[self.column_map.get('Wednesday', 'Wednesday')] or '')
      }
      
      # Log the final availability for this player
      Logger.instance(LOG_ID).info(f"{bcolors.OKGREEN}Final availability for {identity}:{bcolors.ENDC}")
      for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        if availability[day]:
          Logger.instance(LOG_ID).info(f"  {day}: {availability[day]}")
      
      availabilities.append(availability)
    return availabilities

  def _to_availabilities(self, cell: str):
    availabilities = []
    if not cell:
      return availabilities
      
    Logger.instance(LOG_ID).info(f"{bcolors.OKCYAN}Processing cell: {cell}{bcolors.ENDC}")
    
    # Split by comma and handle each availability
    for availability in cell.split(DELIMITTER):
      if not availability:
        continue
      # Handle n+ notation first
      availability = self._replace_n_plus(availability.strip())
      Logger.instance(LOG_ID).info(f"  After n+ replacement: {availability}")
      # Then split by comma again in case n+ generated multiple hours
      availabilities.extend(availability.split(DELIMITTER))

    # Filter out empty strings and duplicates
    result = list(dict.fromkeys(filter(None, availabilities)))
    Logger.instance(LOG_ID).info(f"  Final result: {result}")
    return result

  def _replace_n_plus_func(self, match):
      # Extract the number before the "+" symbol
      n = int(match.group(1))
      # Generate the sequence from n to 23
      replacement = DELIMITTER.join(str(i) for i in range(n, 24))
      Logger.instance(LOG_ID).info(f"  Replacing {match.group(0)} with: {replacement}")
      return replacement

  def _replace_n_plus(self, s):
      # Function changes n+ to n,n+1,...,23
      if isinstance(s, int):
          return str(s)
      return re.sub(r"(\d+)\+", self._replace_n_plus_func, s)