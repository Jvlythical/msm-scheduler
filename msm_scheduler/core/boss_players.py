import pdb

from typing import List, Union

from ..models import Boss, Player
from .boss_effectiveness import BossEffectivenessModel


class BossPlayers():

    def __init__(self, players: List[Player], bosses: List[Boss]):
        self.bosses = bosses
        self.bosses_index = {}

        for boss in bosses:
            self.bosses_index[boss.name] = boss

        self.players_index = {}

        for player in players:
            self.players_index[player.name.strip()] = player

        self.players = players
        self.boss_stacks = {}
        # Organize players by bosses they are interested in
        for player in players:
            for boss_name in player.interests:
                boss_stack = self.get(boss_name)
                boss: Boss = self.bosses_index[boss_name]
                if player.hp >= boss.hp_required and player.arcane_power >= boss.arcane_power_required:
                    boss_stack.append(player)

        bem = BossEffectivenessModel()
        # bem.fit()

        # For each boss, sort players with highest effectiveness last
        for boss_name in self.boss_stacks:
            boss = self.bosses_index.get(boss_name)
            stack = self.get(boss_name)
            stack.sort(key=lambda player: bem.rate(player, boss))

            # TESTING: sort players by availability
            # stack.sort(key=lambda player: len(player.availability))

    def availability_distribution(self):
        boss_availability_distribution = {}
        for boss_name in self.boss_stacks:
            availability_distribution = {}

            boss_availability_distribution[boss_name] = availability_distribution

            players: List[Player] = self.boss_stacks[boss_name]
            for player in players:
                for time in player.availability:
                    if time not in availability_distribution:
                        availability_distribution[time] = []
                    availability_distribution[time].append(player.name)
        return boss_availability_distribution

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
