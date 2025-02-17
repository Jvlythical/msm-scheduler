from ...constants.boss import GLOOM, HARD_ARCHON, HARD_DAMIEN, LUCID, LOTUS, NORMAL_DAMIEN, WILL

class CSVToPlayerInterestsTransformer():

  def __init__(self, rows):
    self.rows = rows

  def tranform(self):
    experiences = []
    for row in self.rows:
      experience = {
        GLOOM: self.is_interested(row.get('GLoom') or row.get('Gloom')),
        HARD_ARCHON: self.is_interested(row.get('Hard Archon') or row.get('Hard Archon')),
        HARD_DAMIEN: self.is_interested(row.get('Hard Damien') or row.get('Hard Damien')),
        LOTUS: self.is_interested(row.get('Lotus') or row.get('Lotus')),
        LUCID: self.is_interested(row.get('Lucid') or row.get('Lucid')),
        'name': (row['Name'] or '').strip(),
        NORMAL_DAMIEN: self.is_interested(row.get('Normal Damien') or row.get('Normal Damien')),
        WILL: self.is_interested(row.get('Will') or row.get('Will'))
      }

      experiences.append(experience)
    return experiences

  def is_interested(self, cell: str):
    if not isinstance(cell, str):
      return False

    return cell.lower() == 'y'
