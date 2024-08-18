from ...constants.boss import HARD_DAMIEN, LUCID, LOTUS, NORMAL_DAMIEN, WILL

class CSVToPlayerInterestsTransformer():

  def __init__(self, rows):
    self.rows = rows

  def tranform(self):
    experiences = []
    for row in self.rows:
      experience = {
        HARD_DAMIEN: self.is_interested(row.get('Hard Damien') or row.get('Hard Damien_interest')),
        LOTUS: self.is_interested(row.get('Lotus') or row.get('Lotus_interest')),
        LUCID: self.is_interested(row.get('Lucid') or row.get('Lucid_interest')),
        'name': row['Name'],
        NORMAL_DAMIEN: self.is_interested(row.get('Normal Damien') or row.get('Normal Damien_interest')),
        WILL: self.is_interested(row.get('Will') or row.get('Will_interest'))
      }

      experiences.append(experience)
    return experiences

  def is_interested(self, cell: str):
    if not isinstance(cell, str):
      return False

    return cell.lower() == 'y'
