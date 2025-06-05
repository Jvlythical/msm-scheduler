from typing import List

from ..models import Team, Player


def construct_base_teams(players: List[Player]):
    # First, create a dictionary to track which players are interested in which bosses at which times
    boss_time_count = dict()
    for player in players:
        for i in player.interests:
            for a in player.availability:
                boss_time_count[i, a] = boss_time_count.get((i, a), 0) + 1

    # Create base teams from the input data
    base_teams: List[Team] = []
    for (boss, time) in boss_time_count.keys():
        if boss_time_count[boss, time] > 10:
            base_teams.append(Team(
                time=time,
                boss_name=boss,
                fills=[],
                player_names=[],
                team_name=time  # Use time as team name
            ))

    return base_teams
