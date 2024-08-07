from .core.create_teams import create_teams

player1 = Player(name="Warrior", hp=100, arcane_power=50, max_damage_cap=200, availability=["Monday"], experience=1000)
player2 = Player(name="Mage", hp=80, arcane_power=70, max_damage_cap=150, availability=["Tuesday"], experience=1200)
player3 = Player(name="Rogue", hp=90, arcane_power=60, max_damage_cap=180, availability=["Wednesday"], experience=1100)
boss = Boss(name="Dark Lord", total_max_damage_cap_required=400, experience=1000, clear_probability=75, availability=["Monday", "Wednesday"], capacity=3, hp_required=80)

# Example team properties
team_properties = [
    [Team(boss=boss, players=[], availability=[])],
    [Team(boss=boss, players=[], availability=[])]
]

# Create teams
teams = create_teams(boss, [player1, player2, player3], team_properties)

# Print created teams
for team_list in teams:
    for team in team_list:
        print(team)
