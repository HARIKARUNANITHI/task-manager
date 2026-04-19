# Task Manager API

## Features
- User Registration & Login (JWT)
- Create Task
- View All Tasks
- View Single Task
- Mark Task as Completed
- Delete Task

## Tech Stack
- FastAPI
- SQLite
- SQLAlchemy
- HTML, CSS, JavaScript

## How to Run

1. Install dependencies:
pip install -r requirements.txt

2. Run backend:
uvicorn app.main:app --reload

3. Run frontend:
cd frontend
python -m http.server 5500

4. Open browser:
http://localhost:5500

## API Docs
http://127.0.0.1:8000/docs