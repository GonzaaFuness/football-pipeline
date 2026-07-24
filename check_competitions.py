import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("FOOTBALL_API_TOKEN")
BASE_URL = "https://api.football-data.org/v4"
headers = {"X-Auth-Token": API_TOKEN}

response = requests.get(f"{BASE_URL}/competitions", headers=headers)
data = response.json()

for comp in data["competitions"]:
    print(comp["code"], "-", comp["name"])