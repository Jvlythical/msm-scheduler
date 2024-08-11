import pdb
from typing import List

from ..types import PlayerStats, PlayerAvailability, PlayerExperience
from ..models import Player

class PlayersBuilder():

  def __init__(self, stats: List[PlayerStats], availabilities: List[PlayerAvailability], experiences: List[PlayerExperience]):
    self.stats = stats
    self.availabilities = availabilities
    self.experiences = experiences

  def build(self):
    availabilities_index = {}

    # Ensure that players with the same identity have the same availability reference
    for availability in self.availabilities:
      times = []
      for day in availability:
        if day == 'identity':
          continue
        hours = availability[day]
        times += list(map(lambda hour: f"{day}.{hour}", hours))

      availabilities_index[availability['identity']] = times

    experiences_index = {}
    for experience in self.experiences:
      clone = { **experience }
      del clone['name']
      experiences_index[experience['name']] = clone

    players = []
    for stat in self.stats:
      players.append(Player(
        **stat,
        availability=availabilities_index[stat['identity']],
        experience=experiences_index.get(stat['name']) or {}
      ))

    return players