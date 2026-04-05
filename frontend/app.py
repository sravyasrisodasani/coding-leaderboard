import streamlit as st
import pandas as pd
import requests

API_URL_LEADERBOARD = "http://127.0.0.1:8000/leaderboard"
API_URL_REFRESH = "http://127.0.0.1:8000/refresh"

# ---------- PAGE ----------
st.set_page_config(page_title="Coding Leaderboard", layout="wide")

# ---------- TITLE ----------
st.markdown(
    "<h1 style='text-align:center;color:#1F4E79;'>🏆 Coding Leaderboard</h1>",
    unsafe_allow_html=True
)

# ---------- REFRESH ----------
if st.button("🔄 Refresh Leaderboard"):
    try:
        requests.post(API_URL_REFRESH)
        st.success("Refreshing... ⏳")
        st.rerun()
    except:
        st.error("Backend not reachable!")

# ---------- FETCH ----------
with st.spinner("Fetching leaderboard... ⏳"):
    try:
        response = requests.get(API_URL_LEADERBOARD)
        data = response.json()
    except:
        st.error("Backend not running!")
        st.stop()

df = pd.DataFrame(data)

# ---------- CLEAN ----------
df["solved"] = df["solved"].astype(int)
df["unsolved"] = df["unsolved"].astype(int)

# ---------- SORT ----------
sort_option = st.selectbox("Sort by:", ["solved", "unsolved", "rank"])
df = df.sort_values(by=sort_option, ascending=False).reset_index(drop=True)

# ---------- RANK ----------
df["rank"] = df.index + 1

# ---------- MEDALS ----------
def medal(r):
    return "🥇" if r == 1 else "🥈" if r == 2 else "🥉" if r == 3 else ""

df["🏅"] = df["rank"].apply(medal)

# ---------- SERIAL ----------
df["#"] = df.index + 1

# ---------- REORDER COLUMNS ----------
df = df[["#", "🏅", "userid", "solved", "unsolved", "rank"]]

# ---------- STYLING ----------
def highlight_rows(row):
    if row["rank"] == 1:
        return ['background-color: #FFD700; color: black; font-weight:bold']*len(row)   # Gold
    elif row["rank"] == 2:
        return ['background-color: #C0C0C0; color: black; font-weight:bold']*len(row)   # Silver
    elif row["rank"] == 3:
        return ['background-color: #CD7F32; color: white; font-weight:bold']*len(row)   # Bronze
    return ['']*len(row)

def zebra(row):
    return ['background-color: #FFFDEB']*len(row) if row.name % 2 == 0 else ['background-color: #F3E3D0']*len(row)

# ---------- COLOR SOLVED DIGIT ----------
def solved_digit_color(row):
    styles = ['']*len(row)
    solved_idx = row.index.get_loc('solved')
    # Top 10 users → green text
    if row.name <= 9:
        styles[solved_idx] = 'color: green; font-weight:bold'
    # Bottom 10 users → red text
    elif row.name >= len(df)-10:
        styles[solved_idx] = 'color: red; font-weight:bold'
    return styles

styled_df = df.style \
    .apply(zebra, axis=1) \
    .apply(highlight_rows, axis=1) \
    .apply(solved_digit_color, axis=1) \
    .set_table_styles([
        {'selector': 'th',
         'props': [('background-color', '#4B8BBE'),
                   ('color', 'white'),
                   ('font-weight', 'bold'),
                   ('text-align', 'center'),
                   ('font-size', '16px')]},
        {'selector': 'td',
         'props': [('text-align', 'center'),
                   ('font-size', '14px')]}
    ]) \
    .set_properties(**{
        'border-color': "#E9B90C",
        'border-width': '0.5px',
        'border-style': 'solid'
    })

# ---------- DISPLAY ----------
st.dataframe(styled_df, height=600, use_container_width=True)