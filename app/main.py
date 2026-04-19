
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.database import engine, Base, SessionLocal
from app import models, schemas
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi import Header
from fastapi import Request


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password: str):
    return pwd_context.hash(password)

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# DB connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Home route
@app.get("/")
def home():
    return {"message": "Task Manager API running"}

# Register route
@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = models.User(
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.query(models.User).filter(models.User.email == email).first()

        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not db_user:
        return {"error": "User not found"}

    if not verify_password(user.password, db_user.password):
        return {"error": "Invalid password"}

    token = create_access_token({"sub": db_user.email})

    return {"access_token": token, "token_type": "bearer"}

@app.post("/tasks")
def create_task(title: str, description: str, token: str,
                db: Session = Depends(get_db)):

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email = payload.get("sub")

    user = db.query(models.User).filter(models.User.email == email).first()

    new_task = models.Task(
        title=title,
        description=description,
        user_id=user.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

@app.get("/tasks")
def get_tasks(token: str, db: Session = Depends(get_db)):

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email = payload.get("sub")

    user = db.query(models.User).filter(models.User.email == email).first()

    tasks = db.query(models.Task).filter(models.Task.user_id == user.id).all()

    return tasks

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, token: str, db: Session = Depends(get_db)):

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email = payload.get("sub")

    user = db.query(models.User).filter(models.User.email == email).first()

    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.user_id == user.id
    ).first()

    if not task:
        return {"error": "Task not found"}

    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully"}

@app.put("/tasks/{task_id}")
def update_task(task_id: int, completed: bool, token: str,
                db: Session = Depends(get_db)):

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email = payload.get("sub")

    user = db.query(models.User).filter(models.User.email == email).first()

    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.user_id == user.id
    ).first()

    if not task:
        return {"error": "Task not found"}

    task.completed = completed
    db.commit()

    return {"message": "Task updated"}

@app.get("/tasks/{task_id}")
def get_task(task_id: int, token: str, db: Session = Depends(get_db)):

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email = payload.get("sub")

    user = db.query(models.User).filter(models.User.email == email).first()

    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.user_id == user.id
    ).first()

    if not task:
        return {"error": "Task not found"}

    return task    