from typing import List

from ..models import Team, Player


def construct_base_teams(players: List[Player]):
    boss_time_count = dict()
    for player in players:
        for i in player.interests:
            for a in player.availability:
                boss_time_count[i, a] = boss_time_count.get((i, a), 0) + 1

    base_teams: List[Team] = []
    for (boss, time) in boss_time_count.keys():
        if boss_time_count[boss, time] > 10:
            base_teams.append(Team(time=time, boss_name=boss, player_names=[]))

    return base_teams
