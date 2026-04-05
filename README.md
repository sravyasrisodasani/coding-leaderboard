🏆 Coding Leaderboard Web App

A full-stack web application that tracks coding progress and displays a live leaderboard with an interactive UI.

---

🚀 Features

- 🔄 Fetches real-time coding stats using web scraping
- 📊 Interactive leaderboard with sorting options
- 🔍 Search functionality to filter users
- 🧮 Dynamic ranking based on performance
- 🌙 Dark mode UI for better user experience
- 📈 Visual representation using charts
- 🔁 Refresh button to update latest data

---

🧠 Tech Stack

🔹 Backend

- FastAPI
- Pandas
- BeautifulSoup (Web Scraping)
- Requests

🔹 Frontend

- Streamlit
- Pandas

🔹 Deployment

- Backend → Render
- Frontend → Streamlit Cloud

---

📂 Project Structure

leaderboard-project/
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── data/
│       └── users.csv
│
├── frontend/
│   └── app.py
│
└── README.md

---

⚙️ How It Works

1. User data (USERID + profile links) is stored in a CSV file
2. Backend fetches coding stats using web scraping
3. Data is processed and ranked based on solved problems
4. APIs expose leaderboard data
5. Frontend fetches and displays data in an interactive UI

---

▶️ Run Locally

🔹 Backend

cd backend
pip install -r requirements.txt
uvicorn main:app --reload

🔹 Frontend

cd frontend
streamlit run app.py

---

🌐 Live Demo

- 🔗 Streamlit link : https://coding-leaderboard.streamlit.app/
---

📌 Future Improvements

- Add user authentication
- Integrate LeetCode / CodeChef APIs
- Auto-refresh leaderboard
- Add profile avatars
- Improve UI/UX

---

🙌 Acknowledgements

This project helped me understand full-stack development by integrating backend APIs, web scraping, and frontend UI.

---

📬 Contact

Feel free to connect with me on LinkedIn for feedback or suggestions!
