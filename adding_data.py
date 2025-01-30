import os

commands = [
    "competitions",
    "comp_teams"
    "make_matches",
    "players_matches"
    "standings"
]
for command in commands:
    print(f"Executing: python manage.py {command}")
    os.system(f"python manage.py {command}")