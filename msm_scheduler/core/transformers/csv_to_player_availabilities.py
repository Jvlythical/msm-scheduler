DELIMITTER = ','

class CSVToPlayerAvailabilitiesTransformer():

  def __init__(self, rows):
    self.rows = rows

  def tranform(self):
    availabilities = []
    for row in self.rows:
      availabilities.append({
        'friday': (row['Friday'] or '').split(DELIMITTER),
        'identity': row['Identity'],
        'monday': (row['Monday'] or '').split(DELIMITTER),
        'thursday': (row['Thursday'] or '').split(DELIMITTER),
        'tuesday': (row['Tuesday'] or '').split(DELIMITTER),
        'wednesday': (row['Wednesday'] or '').split(DELIMITTER)
      })
    return availabilities
