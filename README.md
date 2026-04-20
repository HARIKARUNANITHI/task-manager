# Task Manager API

## 🚀 Project Overview

This is a full-stack Task Manager application built using FastAPI for the backend and a simple frontend using HTML, CSS, and JavaScript.

Users can register, login, and manage their personal tasks.

---

## ✨ Features

* User Registration & Login (JWT Authentication)
* Create Task
* View All Tasks
* View Single Task
* Mark Task as Completed
* Delete Task

---

## 🛠 Tech Stack

* Backend: FastAPI
* Database: SQLite
* ORM: SQLAlchemy
* Authentication: JWT + bcrypt
* Frontend: HTML, CSS, JavaScript
* Deployment: Render

---

## 🌐 Live Demo

🔗 Full Application:
https://task-manager-hzch.onrender.com

📄 API Docs:
https://task-manager-hzch.onrender.com/docs

---

## ⚙️ How to Run Locally

### 1. Clone repository

git clone https://github.com/HARIKARUNANITHI/task-manager.git

### 2. Install dependencies

pip install -r requirements.txt

### 3. Run backend

uvicorn app.main:app --reload

### 4. Open in browser

http://127.0.0.1:8000

---

## 🔐 Environment Variables

Create a `.env` file and add:

SECRET_KEY=your_secret_key_here

---

## 📁 Project Structure

task-manager/
│
├── app/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── database.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── requirements.txt
└── README.md

---

## 📌 Notes

* Users can only access their own tasks
* Passwords are securely hashed using bcrypt
* JWT is used for authentication
* Frontend and backend are served together using FastAPI

---

## 🙌 Author

Hari K
