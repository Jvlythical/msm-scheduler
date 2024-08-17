from ...constants.boss import HARD_DAMIEN, LUCID, LOTUS, NORMAL_DAMIEN, WILL

class CSVToPlayerInterestsTransformer():

  def __init__(self, rows):
    self.rows = rows

  def tranform(self):
    experiences = []
    for row in self.rows:
      experience = {
        HARD_DAMIEN: self.is_interested(row['Hard Damien']),
        LOTUS: self.is_interested(row['Lotus']),
        LUCID: self.is_interested(row['Lucid']),
        'name': row['Name'],
        NORMAL_DAMIEN: self.is_interested(row['Normal Damien']),
        WILL: self.is_interested(row['Will'])
      }

      experiences.append(experience)
    return experiences

  def is_interested(self, cell: str):
    if not isinstance(cell, str):
      return False

    return cell.lower() == 'y'
