import streamlit as st
import pandas as pd
import requests

API_URL = "https://coding-leaderboard-1.onrender.com/leaderboard"
REFRESH_URL = "https://coding-leaderboard-1.onrender.com/refresh"

# ---------- PAGE ----------
st.set_page_config(page_title="Coding Leaderboard", layout="wide")

# ---------- DARK MODE CSS ----------
st.markdown("""
<style>
body {
    background-color: #0E1117;
    color: white;
}
.stApp {
    background-color: #0E1117;
}
</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.markdown(
    "<h1 style='text-align:center;color:#00ADB5;'>🏆 Coding Leaderboard</h1>",
    unsafe_allow_html=True
)

# ---------- REFRESH ----------
if st.button("🔄 Refresh Leaderboard"):
    try:
        requests.post(REFRESH_URL)
        st.success("Refreshing... wait 10–20 sec ⏳")
    except:
        st.error("Backend not reachable!")

# ---------- FETCH ----------
with st.spinner("Fetching leaderboard... ⏳"):
    try:
        response = requests.get(API_URL)
        data = response.json()
    except:
        st.error("Backend not reachable!")
        st.stop()

# ---------- CHECK ----------
if not isinstance(data, list) or len(data) == 0:
    st.warning("No data yet 😴 Click refresh and wait...")
    st.stop()

# ---------- DATAFRAME ----------
df = pd.DataFrame(data)

# ---------- CLEAN ----------
df["solved"] = df["solved"].astype(int)
df["unsolved"] = df["unsolved"].astype(int)

# ---------- SCORE ----------
df["score"] = df["solved"] * 2 - df["unsolved"]

# ---------- SEARCH ----------
st.subheader("🔍 Search User")
search = st.text_input("Enter userid...")

if search:
    df = df[df["userid"].str.contains(search, case=False)]

# ---------- SORT ----------
sort_option = st.selectbox(
    "Sort by:",
    ["solved", "unsolved", "score", "rank"]
)

if sort_option != "rank":
    df = df.sort_values(by=sort_option, ascending=False)

df = df.reset_index(drop=True)

# ---------- RANK ----------
df["rank"] = df.index + 1

# ---------- MEDALS ----------
def medal(r):
    return "🥇" if r == 1 else "🥈" if r == 2 else "🥉" if r == 3 else ""

df["🏅"] = df["rank"].apply(medal)

# ---------- SERIAL ----------
df["#"] = df.index + 1

# ---------- ORDER ----------
df = df[["#", "🏅", "userid", "solved", "unsolved", "score", "rank"]]

# ---------- STYLING ----------

# Top 3 highlight (dark friendly)
def highlight_top3(row):
    if row["rank"] == 1:
        return ['background-color: #3B1C32; color: #00FFAB; font-weight:bold'] * len(row)
    elif row["rank"] == 2:
        return ['background-color: #6A1E55; color: #B0BEC5; font-weight:bold'] * len(row)
    elif row["rank"] == 3:
        return ['background-color: #A64D79; color: #FFAB91; font-weight:bold'] * len(row)
    return [''] * len(row)

# Zebra rows (dark)
def zebra(row):
    return ['background-color: #161A21'] * len(row) if row.name % 2 == 0 else ['background-color: #1E232B'] * len(row)

# Top 10 green / Bottom 10 red
def color_top_bottom(row):
    styles = [''] * len(row)
    s_idx = row.index.get_loc("solved")
    u_idx = row.index.get_loc("unsolved")

    if row.name < 10:
        styles[s_idx] = 'color: #00FFAB; font-weight:bold'
        styles[u_idx] = 'color: #00FFAB; font-weight:bold'
    elif row.name >= len(df) - 10:
        styles[s_idx] = 'color: #FF4C4C; font-weight:bold'
        styles[u_idx] = 'color: #FF4C4C; font-weight:bold'

    return styles

# ---------- APPLY STYLE ----------
styled_df = df.style \
    .apply(zebra, axis=1) \
    .apply(highlight_top3, axis=1) \
    .apply(color_top_bottom, axis=1) \
    .set_table_styles([
        {
            'selector': 'th',
            'props': [
                ('background-color', '#0D47A1'),
                ('color', 'white'),
                ('font-weight', 'bold'),
                ('text-align', 'center'),
                ('font-size', '15px')
            ]
        },
        {
            'selector': 'td',
            'props': [
                ('text-align', 'center'),
                ('font-size', '14px'),
                ('color', 'white')
            ]
        }
    ])

# ---------- DISPLAY ----------
st.dataframe(styled_df, use_container_width=True, height=600)

# ---------- GRAPH ----------
st.subheader("📊 Solved Problems Graph")
st.bar_chart(df.set_index("userid")["solved"])