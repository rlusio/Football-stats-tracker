import pandas as pd
import json
import matplotlib.pyplot as plt
import os
players_data_file = "players_data.csv"
competition_teams_file = "competition_teams.csv"
output_file = "players_match_stats.csv"

def load_data():
    players_df = pd.read_csv(players_data_file, header=None, names=["player_id", "data"])
    teams_df = pd.read_csv(competition_teams_file)
    return players_df, teams_df

def parse_player_data(row):
    try:
        data = json.loads(row["data"])
        player_info = data[0]["player"]
        matches = [match for match in data[1:] if "home_team" in match]
        return {
            "player_id": row["player_id"],
            "name": player_info["name"],
            "date_of_birth": player_info["date_of_birth"],
            "nationality": player_info["nationality"],
            "matches": matches
        }
    except (json.JSONDecodeError, IndexError, KeyError):
        return None

def get_player_team_info(player_name, teams_df):
    player_row = teams_df[teams_df["player_name"] == player_name]
    if not player_row.empty:
        return {
            "team_name": player_row.iloc[0]["team_name"],
            "position": player_row.iloc[0]["position"]
        }
    return {"team_name": "Unknown", "position": "Unknown"}

def compute_statistics(player_data):
    stats = {"wins": 0, "draws": 0, "losses": 0, "goals_scored": 0, "goals_conceded": 0}
    for match in player_data["matches"]:
        home_goals, away_goals = match["final_result"]["home"], match["final_result"]["away"]
        player_team = player_data["team_name"]
        if match["home_team"] == player_team:
            stats["goals_scored"] += home_goals
            stats["goals_conceded"] += away_goals
            if home_goals > away_goals:
                stats["wins"] += 1
            elif home_goals == away_goals:
                stats["draws"] += 1
            else:
                stats["losses"] += 1
        elif match["away_team"] == player_team:
            stats["goals_scored"] += away_goals
            stats["goals_conceded"] += home_goals
            if away_goals > home_goals:
                stats["wins"] += 1
            elif home_goals == home_goals:
                stats["draws"] += 1
            else:
                stats["losses"] += 1
    return stats

def save_players_data(players_stats):
    df = pd.DataFrame(players_stats)
    df.to_csv(output_file, index=False)

def generate_player_plot(player, df):
    player_stats = df[df['name'] == player]
    wins = player_stats['wins'].iloc[0]
    losses = player_stats['losses'].iloc[0]
    draws = player_stats['draws'].iloc[0]
    total_matches = wins + losses + draws
    win_percentage = (wins / total_matches) * 100 if total_matches > 0 else 0
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    results = [wins, losses, draws]
    labels = ['Wins', 'Losses', 'Draws']
    ax.bar(labels, results, color=['green', 'red', 'gray'], width=0.4)
    ax.set_title(f"Match Results for {player}")
    ax.set_xlabel("Result")
    ax.set_ylabel("Number of Matches")
    ax.set_ylim(0, total_matches)
    for i, value in enumerate(results):
        ax.text(i, value + 0.1, f'{value}', ha='center', va='bottom', fontsize=12) 
    ax.text(1.5, total_matches - 1, f'Win ratio: {win_percentage:.2f}%', ha='center', fontsize=12, color='blue')
    output_dir = 'player_plots'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    file_path = os.path.join(output_dir, f"{player}_stats.png")
    plt.savefig(file_path)
    plt.close(fig)

def save_data_for_plots():
    players_df, teams_df = load_data()
    selected_players = players_df[players_df["data"].str.contains("home_team")].head(50)
    players_stats = []
    for _, row in selected_players.iterrows():
        player_data = parse_player_data(row)
        if player_data:
            team_info = get_player_team_info(player_data["name"], teams_df)
            player_data.update(team_info)
            stats = compute_statistics(player_data)
            player_data.update(stats)
            players_stats.append(player_data)

def main():
    df = pd.read_csv('players_match_stats.csv')  
    for player in df['name'].unique():
        generate_player_plot(player, df)

if __name__ == "__main__":
    main()