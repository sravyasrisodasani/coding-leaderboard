from fastapi import FastAPI
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import threading

app = FastAPI()   # ✅ THIS LINE IS MUST

CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "users.csv")
TOTAL_PROBLEMS = 210

leaderboard_cache = []

def load_users():
    try:
        df = pd.read_csv(CSV_PATH)
        df = df.drop_duplicates(subset=["USERID"])
        return df
    except:
        return pd.DataFrame(columns=["USERID", "PROFILELINK"])

def get_codingbat_data(profile_link):
    try:
        response = requests.get(profile_link, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()

        solved = 0
        for line in text.split("\n"):
            if "Count:" in line:
                try:
                    solved = int(line.split(":")[1])
                except:
                    solved = 0
                break

        return {"solved": solved, "unsolved": TOTAL_PROBLEMS - solved}
    except:
        return {"solved": 0, "unsolved": TOTAL_PROBLEMS}

def fetch_leaderboard():
    global leaderboard_cache

    df = load_users()
    temp = []

    for _, row in df.iterrows():
        data = get_codingbat_data(row["PROFILELINK"])
        temp.append({
            "userid": row["USERID"],
            "solved": data["solved"],
            "unsolved": data["unsolved"]
        })

    temp.sort(key=lambda x: x["solved"], reverse=True)
    leaderboard_cache = temp

@app.on_event("startup")
def startup():
    threading.Thread(target=fetch_leaderboard, daemon=True).start()

@app.get("/")
def home():
    return {"message": "Working ✅"}

@app.get("/leaderboard")
def leaderboard():
    return leaderboard_cache

@app.post("/refresh")
def refresh():
    threading.Thread(target=fetch_leaderboard, daemon=True).start()
    return {"status": "Refreshing"}