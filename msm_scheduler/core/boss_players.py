import pdb

from typing import List, Union

from ..models import Boss, Player

class BossPlayers():

  def __init__(self, players: List[Player], bosses: List[Boss]):
    self.bosses = bosses
    self.bosses_index = {}

    for boss in bosses:
      self.bosses_index[boss.name] = boss

    self.players_index = {}

    for player in players:
        self.players_index[player.name] = player

    self.players = players
    self.boss_stacks = {}

    # Organize players by bosses they are interested in
    for player in players:
      for boss_name in player.interests:
        self.get(boss_name).append(player)

    # For each boss, sort players with highest effectiveness last
    for boss_name in self.boss_stacks:
      boss = self.bosses_index[boss_name]
      stack = self.get(boss_name)
      stack.sort(key=lambda player: player.boss_effectiveness(boss))

  def get(self, boss_name) -> List[Player]:
    stack = self.boss_stacks.get(boss_name)
    if not stack:
      stack = []
      self.boss_stacks[boss_name] = stack
    return stack

  def next_player(self, boss_name: str) -> Union[Player, None]:
    stack = self.get(boss_name)

    while len(stack) > 0:
      player: Player = stack.pop()

      # A player may have their interests dynamically adjusted once they are assigned
      if boss_name in player.interests:
        return player

  def remove(self, boss_name: str, player_name: str):
    stack = self.get(boss_name)

    i = 0
    for player in stack:
      if player.name == player_name:
        break
      i += 1

    del stack[i]