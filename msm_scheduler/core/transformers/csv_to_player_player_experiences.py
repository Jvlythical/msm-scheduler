from ...constants.boss import GLOOM, HARD_ARCHON, HARD_DAMIEN, LUCID, LOTUS, NORMAL_DAMIEN, WILL

class CSVToPlayerExperiencesTransformer():

  def __init__(self, rows):
    self.rows = rows

  def tranform(self):
    experiences = []
    for row in self.rows:
      experience = {
        GLOOM: int(row['Gloom']) if row['Gloom'] else 0,
        HARD_ARCHON: int(row['Hard Archon']) if row['Hard Archon'] else 0,
        HARD_DAMIEN: int(row['Hard Damien']) if row['Hard Damien'] else 0,
        LOTUS: int(row['Lotus']) if row['Lotus'] else 0,
        LUCID: int(row['Lucid']) if row['Lucid'] else 0,
        'name': (row['Name'] or '').strip(),
        NORMAL_DAMIEN: int(row['Normal Damien']) if row['Normal Damien'] else 0,
        WILL: int(row['Will']) if row['Will'] else 0
      }

      experiences.append(experience)
    return experiences

