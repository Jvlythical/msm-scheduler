from ...constants.boss import HARD_DAMIEN, LUCID, LOTUS, NORMAL_DAMIEN, WILL

class CSVToPlayerExperiencesTransformer():

  def __init__(self, rows):
    self.rows = rows

  def tranform(self):
    experiences = []
    for row in self.rows:
      experience = {
        HARD_DAMIEN: int(row['Hard Damien']) if row['Hard Damien'] else 0,
        LOTUS: int(row['Lotus']) if row['Lotus'] else 0,
        LUCID: int(row['Lucid']) if row['Lucid'] else 0,
        'name': row['Name'],
        NORMAL_DAMIEN: int(row['Normal Damien']) if row['Normal Damien'] else 0,
        WILL: int(row['Will']) if row['Will'] else 0
      }

      experiences.append(experience)
    return experiences

