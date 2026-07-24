
import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("FOOTBALL_API_TOKEN")
BASE_URL = "https://api.football-data.org/v4"
HEADERS = {"X-Auth-Token": API_TOKEN}
COMPETITION_CODE = "WC"


def extract_matches(competition_code: str) -> dict:
    """Trae todos los partidos de una competencia desde la API."""
    url = f"{BASE_URL}/competitions/{competition_code}/matches"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()  # lanza error si el status no es 200
    return response.json()


def save_raw_data(data: dict, competition_code: str) -> str:
    """Guarda el JSON crudo con timestamp, como respaldo antes de transformar."""
    os.makedirs("data/raw", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = f"data/raw/{competition_code}_{timestamp}.json"

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return filepath


if __name__ == "__main__":
    print(f"Extrayendo partidos de {COMPETITION_CODE}...")
    matches_data = extract_matches(COMPETITION_CODE)

    print(f"Partidos encontrados: {len(matches_data['matches'])}")

    filepath = save_raw_data(matches_data, COMPETITION_CODE)
    print(f"Datos guardados en: {filepath}")