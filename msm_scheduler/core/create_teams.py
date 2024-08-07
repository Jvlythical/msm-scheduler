from typing import List
from itertools import combinations

def create_teams(boss: Boss, players: List[Player], team_properties: List[List[Team]]) -> List[List[Team]]:
    def valid_player(player: Player) -> bool:
        return player.hp >= boss.hp_required

    def can_fill_team(team: List[Player]) -> bool:
        return sum(player.max_damage_cap for player in team) >= boss.total_max_damage_cap_required

    def fill_team(players: List[Player], capacity: int) -> List[Player]:
        # Try to find a combination of players that meets the boss's requirements
        for team_size in range(1, len(players) + 1):
            for team in combinations(players, team_size):
                if can_fill_team(team) and len(team) <= capacity:
                    return list(team)
        return []

    # Filter valid players
    valid_players = [player for player in players if valid_player(player)]

    # Sort players by max_damage_cap in descending order
    valid_players.sort(key=lambda p: p.max_damage_cap, reverse=True)

    # Set to keep track of used players
    used_players = set()

    # List to hold the created teams
    created_teams = []

    # Create teams based on available team properties
    for team_property_list in team_properties:
        for team_property in team_property_list:
            team_capacity = team_property.capacity
            team_list = []

            while valid_players:
                available_players = [p for p in valid_players if p not in used_players]
                if not available_players:
                    break

                team = fill_team(available_players, team_capacity)
                if not team:
                    break

                team_list.append(Team(boss=boss, players=team, availability=[]))  # Placeholder for availability
                # Mark players as used
                used_players.update(team)

                # Remove used players from valid_players
                valid_players = [p for p in valid_players if p not in used_players]

            created_teams.append(team_list)

    return created_teams
