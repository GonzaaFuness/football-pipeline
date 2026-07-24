import json
import pandas as pd
from pathlib import Path


def load_latest_raw_file(competition_code: str) -> dict:
    """Busca y carga el archivo JSON crudo más reciente de una competencia."""
    raw_dir = Path("data/raw")
    files = sorted(raw_dir.glob(f"{competition_code}_*.json"))

    if not files:
        raise FileNotFoundError(f"No hay archivos crudos para {competition_code}")

    latest_file = files[-1]
    print(f"Cargando: {latest_file}")

    with open(latest_file, "r", encoding="utf-8") as f:
        return json.load(f)


def transform_matches(raw_data: dict) -> pd.DataFrame:
    """Convierte el JSON crudo de partidos en un DataFrame limpio."""
    matches = raw_data["matches"]

    rows = []
    for match in matches:
        rows.append({
            "match_id": match["id"],
            "utc_date": match["utcDate"],
            "status": match["status"],
            "matchday": match["matchday"],
            "stage": match["stage"],
            "group": match.get("group"),
            "home_team": match["homeTeam"]["name"],
            "away_team": match["awayTeam"]["name"],
            "home_score": match["score"]["fullTime"]["home"],
            "away_score": match["score"]["fullTime"]["away"],
            "winner": match["score"].get("winner"),
        })

    df = pd.DataFrame(rows)

    # Conversión de tipos
    df["utc_date"] = pd.to_datetime(df["utc_date"])
    df["home_score"] = df["home_score"].astype("Int64")  # Int64 permite NaN (partidos no jugados)
    df["away_score"] = df["away_score"].astype("Int64")

    return df


if __name__ == "__main__":
    raw_data = load_latest_raw_file("WC")
    df = transform_matches(raw_data)

    print(df.info())
    print(df.head())

    # Guardamos también una versión procesada en CSV, útil para inspeccionar
    Path("data/processed").mkdir(parents=True, exist_ok=True)
    df.to_csv("data/processed/wc_matches.csv", index=False)
    print("\nGuardado en: data/processed/wc_matches.csv")