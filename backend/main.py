# backend/main.py
from fastapi import FastAPI
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import threading

app = FastAPI()

# ---------- PATH ----------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "data", "users.csv")

# ---------- CONSTANT ----------
TOTAL_PROBLEMS = 210

# ---------- CACHE ----------
leaderboard_cache = []

# ---------- LOAD USERS ----------
def load_users():
    df = pd.read_csv(CSV_PATH)
    df = df.drop_duplicates(subset=["USERID"])
    return df

# ---------- SCRAPER ----------
def get_codingbat_data(profile_link):
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(profile_link, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()
        lines = text.split("\n")

        solved = 0

        for line in lines:
            if "Count:" in line:
                try:
                    solved = int(line.strip().split(":")[1])
                except:
                    solved = 0
                break

        unsolved = TOTAL_PROBLEMS - solved

        return {"solved": solved, "unsolved": unsolved}

    except Exception as e:
        print("❌ Error:", profile_link, e)
        return {"solved": 0, "unsolved": TOTAL_PROBLEMS}

# ---------- FETCH ----------
def fetch_leaderboard():
    global leaderboard_cache

    print("🚀 Fetching leaderboard...")

    df = load_users()
    temp = []

    for _, row in df.iterrows():
        print(f"Processing: {row['USERID']}")
        data = get_codingbat_data(row["PROFILELINK"])

        temp.append({
            "userid": row["USERID"],
            "solved": data["solved"],
            "unsolved": data["unsolved"]
        })

    temp.sort(key=lambda x: x["solved"], reverse=True)

    leaderboard_cache = temp
    print("✅ Leaderboard ready!")

# ---------- STARTUP ----------
@app.on_event("startup")
def startup():
    threading.Thread(target=fetch_leaderboard, daemon=True).start()

# ---------- HOME ----------
@app.get("/")
def home():
    return {"message": "Leaderboard API Running 🚀"}

# ---------- REFRESH ----------
@app.post("/refresh")
def refresh():
    threading.Thread(target=fetch_leaderboard, daemon=True).start()
    return {"status": "Refreshing..."}

# ---------- GET ----------
@app.get("/leaderboard")
def leaderboard():
    global leaderboard_cache

    # 🔥 AUTO-FETCH if empty
    if not leaderboard_cache:
        fetch_leaderboard()

    return leaderboard_cache