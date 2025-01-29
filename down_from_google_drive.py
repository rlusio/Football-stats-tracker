import pandas as pd
import requests
from sqlalchemy import create_engine
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
def download_files_from_google_drive():
    files = {
        "seasons.csv": "1t79cwhBgnfrze0Cn63SDlllGaKnv93p8",
        "players_data.csv": "1Dpqte-NGhgHvm5xtzZkwHc2vJvur1DQW",
        "league_2021_matches.csv": "1D2efPuK8XU8OayjlDtd3ZgVOhrsbDQtg",
        "competitions_ids.csv": "1kDgomYa2ojWPfVF15jlMLDC61AigZB4P",
        "competition_teams.json": "158d7G5AWEPZ19vuto1WiKZPKM5n8n77h",
        "competition_standings.json": "1FVEX35PbUdVR3YkvXDyrasfuA3NpNA7O",
    }
    os.makedirs("data", exist_ok=True)
    for filename, file_id in files.items():
        url = f"https://drive.google.com/uc?export=download&id={file_id}"
        response = requests.get(url, stream=True)
        file_path = os.path.join("data", filename)
        with open(file_path, "wb") as f:
            f.write(response.content)
        logger.info(f"File {filename} has been downoladed and saved in {file_path}")
        
def load_csv_to_database(engine, folder="data"):
    for filename in os.listdir(folder):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder, filename)
            df = pd.read_csv(file_path)
            table_name = filename.split(".")[0]
            df.to_sql(table_name, engine, if_exists="replace", index=False)
            logger.info(f"File {filename} has been loaded to database as a {table_name}")

        elif filename.endswith(".json"):
            file_path = os.path.join(folder, filename)
            with open(file_path, 'r') as file:
                data = file.read()
            table_name = filename.split(".")[0]
            df = pd.DataFrame([data])
            df.to_sql(table_name, engine, if_exists="replace", index=False)
            logger.info(f"File {filename} has been loaded to database as a {table_name}")

def main():
    engine = create_engine("postgresql://football_stats_tracker_user:kF1QusNOQ9MKB5VdhMWLldIPs21oRhcV@dpg-cu98fmi3esus73b1lec0-a.oregon-postgres.render.com/football_stats_tracker")
    download_files_from_google_drive() 
    load_csv_to_database(engine)  

if __name__ == "__main__":
    main()