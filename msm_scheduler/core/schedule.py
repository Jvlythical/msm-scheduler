from typing import Callable, List

from ..models.player import Player
from ..models.team import Team

class Schedule():

  def __init__(self, boss_name: str, teams: List[Team]):
    self.boss_name = boss_name
    self._fills: List[Player] = []
    self.teams = teams

  @property
  def boss_name(self):
    return self._boss_name

  @boss_name.setter
  def boss_name(self, v: boss_name):
    self._boss_name = v

  @property
  def teams(self):
    return self._teams

  @teams.setter
  def teams(self, v: List[Team]):
    self._teams = v

  @property
  def fills(self):
    return self._fills

  def add_fill(self, player: Player):
    self._fills.append(player)

  def add_team(self, team: Team):
    self._teams.append(team)

  def sorted_teams(self, sort_handler: Callable):
      if not isinstance(self.teams, list):
        self.teams = []

      # Sort team with lowest clear_propability first
      self.teams.sort(key=sort_handler)

      return self.teams