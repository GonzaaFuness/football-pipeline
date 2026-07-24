import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("FOOTBALL_DB_HOST"),
    "port": os.getenv("FOOTBALL_DB_PORT"),
    "dbname": os.getenv("FOOTBALL_DB_NAME"),
    "user": os.getenv("FOOTBALL_DB_USER"),
    "password": os.getenv("FOOTBALL_DB_PASSWORD"),
}

CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS matches (
    match_id INTEGER PRIMARY KEY,
    utc_date TIMESTAMP,
    status VARCHAR(20),
    matchday INTEGER,
    stage VARCHAR(50),
    "group" VARCHAR(50),
    home_team VARCHAR(100),
    away_team VARCHAR(100),
    home_score INTEGER,
    away_score INTEGER,
    winner VARCHAR(20)
);
"""

UPSERT_QUERY = """
INSERT INTO matches (match_id, utc_date, status, matchday, stage, "group",
                      home_team, away_team, home_score, away_score, winner)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (match_id) DO UPDATE SET
    status = EXCLUDED.status,
    home_score = EXCLUDED.home_score,
    away_score = EXCLUDED.away_score,
    winner = EXCLUDED.winner;
"""


def load_to_postgres(csv_path: str):
    df = pd.read_csv(csv_path)

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute(CREATE_TABLE_QUERY)
    conn.commit()

    rows_inserted = 0
    for _, row in df.iterrows():
        cur.execute(UPSERT_QUERY, (
            row["match_id"],
            row["utc_date"],
            row["status"],
            int(row["matchday"]) if pd.notna(row["matchday"]) else None,
            row["stage"],
            row["group"] if pd.notna(row["group"]) else None,
            row["home_team"], row["away_team"],
            int(row["home_score"]) if pd.notna(row["home_score"]) else None,
            int(row["away_score"]) if pd.notna(row["away_score"]) else None,
            row["winner"],
        ))
        rows_inserted += 1

    conn.commit()
    cur.close()
    conn.close()

    print(f"Carga completa: {rows_inserted} filas procesadas (insertadas/actualizadas)")


if __name__ == "__main__":
    load_to_postgres("data/processed/wc_matches.csv")