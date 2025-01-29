import os

# Lista komend do wykonania
commands = [
    "makemigrations",
    "migrate",
    "competitions",
    "make_matches",
    "make_teams"
]

# Wykonanie każdej komendy
for command in commands:
    print(f"Executing: python manage.py {command}")
    os.system(f"python manage.py {command}")