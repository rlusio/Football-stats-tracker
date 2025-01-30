import os
import logging
import requests
import pandas as pd
import gdown
from sqlalchemy import create_engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
DATA_DIR = "data"
PLOTS_DIR = "player_plots"
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PLOTS_DIR, exist_ok=True)
FILES = {
    "seasons.csv": "1t79cwhBgnfrze0Cn63SDlllGaKnv93p8",
    "playersData.csv": "10cNmxPZKnJxS5rfw1q3JFnFrZW8IUIff",
    "matchesData.csv": "1NU0KH0u7C4uwbX0acy6OP5Pc9tBEj_o1",
    "formatted_matches.csv": "1-bdOUi-Iy9-5CXtZuaNfgCyuVBbNqhCe",
    "competitions_ids.csv": "1kDgomYa2ojWPfVF15jlMLDC61AigZB4P",
    "competition_teams.csv": "15PWeNSQGRUM1HIM4hiaaMo62QFfEHITU",
    "competition_standings.csv": "1_q88PPK4PkU-PqgVlsgMAM2DQSrGPwpr",
}
PLOTS_FOLDER_ID = "1uEtR9gC9qbyA33nVR31He98jqTrZoA55"
def download_files():
    for filename, file_id in FILES.items():
        file_path = os.path.join(DATA_DIR, filename)
        if os.path.exists(file_path):
            logger.info(f"{filename} already exists")
            continue
        url = f"https://drive.google.com/uc?export=download&id={file_id}"
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(file_path, "wb") as f:
                f.write(response.content)
            logger.info(f"Downloaded {filename}")
        except requests.RequestException as e:
            logger.error(f"Downloading {filename} failed: {e}")

def download_player_plots():
    if os.listdir(PLOTS_DIR):
        logger.info(f"Folder {PLOTS_DIR} already contains files")
        return
    try:
        gdown.download_folder(
            id=PLOTS_FOLDER_ID, 
            output=PLOTS_DIR,
            quiet=False,
            use_cookies=False
        )
        logger.info("All plots have been downloaded successfully")
    except Exception as e:
        logger.error(f"Downloading plots failed: {e}", exc_info=True)

def load_csv_to_database(engine):
    for filename in os.listdir(DATA_DIR):
        file_path = os.path.join(DATA_DIR, filename)
        table_name = filename.split(".")[0]
        if filename.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif filename.endswith(".json"):
            with open(file_path, 'r') as file:
                data = file.read()
            df = pd.DataFrame([data])
        else:
            continue
        try:
            df.to_sql(table_name, engine, if_exists="replace", index=False)
            logger.info(f"{filename} loaded to database as a{table_name}`.")
        except Exception as e:
            logger.error(f"{filename} can't be saved: {e}")

if __name__ == "__main__":
    engine = create_engine("postgresql://football_stats_tracker_user:kF1QusNOQ9MKB5VdhMWLldIPs21oRhcV@dpg-cu98fmi3esus73b1lec0-a.oregon-postgres.render.com/football_stats_tracker")
    download_files()
    download_player_plots()
    load_csv_to_database(engine)