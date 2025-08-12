# 🚨 Project Discontinued 🚨

This project was a **learning experiment** to explore Flet + FastAPI + PostgreSQL.  
It is now **archived** due to limitations in the Flet framework, such as limited widget customization and performance constraints on mobile.  

Development continues in a **new Flutter-based version** for better scalability, performance, and cross-platform support.  

➡️ **See the new repository here:** [LogBook (Flutter Version)](https://github.com/Fakhrul-Hakimy/LogBook-Flutter)  

---

# 📓 LogBook

LogBook is a learning project — an Android application built with Flet for logging daily activities. It features a Python-based frontend with a FastAPI backend, connected to a PostgreSQL database. The backend is securely exposed to the internet via Cloudflare Tunnel to simulate production-level deployment.

---

## 🚀 Features

- **🔐 User Authentication**  
  Secure login with username and password.

- **📝 Daily Log Entry**  
  Users can create logs with:
  - Date
  - Time-in and Time-out
  - Comment
  - Image upload

- **💾 Database Integration**  
  Uses PostgreSQL with:
  - `users` table (username, hashed password)
  - `logs` table (date, time_in, time_out, comment, image_path)

- **📤 File Uploads**  
  Image files are saved with timestamped names in the `uploads/` directory. File paths are stored in the database.

- **📡 REST API Endpoints**
  - `POST /users`: Create a new user
  - `POST /login`: Authenticate a user
  - `POST /logs`: Create a new log entry (with optional image)
  - `GET /logs`: Retrieve all log entries

---

## 🧰 Tech Stack

| Layer     | Technology      |
|-----------|-----------------|
| Frontend  | Python, Flet    |
| Backend   | Python, FastAPI |
| Database  | PostgreSQL      |

### 🧩 Libraries Used

- `flet~=0.28.3`
- `requests~=2.32.4`
- `bcrypt`
- `SQLAlchemy`

---

## ⚙️ Getting Started

### ✅ Prerequisites

- Python 3.x
- PostgreSQL
- (Optional) Cloudflare Tunnel

---

### 📦 Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/LogBook.git
cd LogBook

cd api
python -m venv .venv
```

# macOS/Linux
```
source .venv/bin/activate

```
# Windows
```bash
.\.venv\Scripts\activate

pip install -r requirements.txt
```
⚠️ Update the PostgreSQL connection string in database.py

Run the backend:

```bash
uvicorn main:app --reload
```
3. Set Up the Frontend
```bash

cd ../app
python -m venv .venv
```
# macOS/Linux

```bash
source .venv/bin/activate
```
# Windows
```bash
.\.venv\Scripts\activate

pip install -r requirements.txt
```
Run the Flet app:

```bash
flet run main.py
```
🗂️ Project Structure

```bash
Copy
Edit
LogBook/
│
├── api/                    # FastAPI backend
│   ├── main.py             # API routes
│   ├── models.py           # SQLAlchemy models
│   ├── database.py         # DB connection
│   └── uploads/            # Uploaded images
│
├── app/                    # Flet frontend
│   ├── main.py             # UI logic
│   └── logo.png            # App logo
│
├── .gitignore              # Git ignore rules
├── LICENSE                 # MIT License
└── README.md               # Project info
```
📄 License
This project is licensed under the MIT License.

The software is provided "as is", without warranty of any kind. See the LICENSE file for more details.

📬 Contact
For questions or feedback, please contact the repository owner: Fakhrul Hakimy.

