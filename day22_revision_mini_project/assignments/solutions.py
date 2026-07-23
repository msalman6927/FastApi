# solutions.py  (Day 22 - COMPLETE Task Manager in a SINGLE runnable file)
# -----------------------------------------------------------
# A single-file version of the whole app (auth + DB + per-user CRUD),
# handy as a reference. The taskmanager/ package is the structured version.
#
# SETUP: pip install "fastapi[standard]" sqlmodel pyjwt "passlib[bcrypt]"
# RUN:   fastapi dev solutions.py  ->  http://127.0.0.1:8000/docs
# -----------------------------------------------------------

from datetime import datetime, timedelta, timezone
import jwt
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlmodel import SQLModel, Field, create_engine, Session, select

# --- config (would live in .env) ---
SECRET, ALGO, MINUTES = "dev-secret-change-me", "HS256", 30
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2 = OAuth2PasswordBearer(tokenUrl="/login")
engine = create_engine("sqlite:///tasks.db",
                       connect_args={"check_same_thread": False})


# --- models ---
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    done: bool = False
    priority: int = 3
    user_id: int = Field(foreign_key="user.id")

class RegisterIn(SQLModel):
    username: str
    password: str

class TaskCreate(SQLModel):
    title: str
    done: bool = False
    priority: int = Field(default=3, ge=1, le=5)

class TaskUpdate(SQLModel):
    title: str | None = None
    done: bool | None = None
    priority: int | None = Field(default=None, ge=1, le=5)

class TaskPublic(SQLModel):
    id: int
    title: str
    done: bool
    priority: int


# --- helpers ---
def get_session():
    with Session(engine) as session:
        yield session

def create_token(username: str) -> str:
    return jwt.encode(
        {"sub": username, "exp": datetime.now(timezone.utc) + timedelta(minutes=MINUTES)},
        SECRET, algorithm=ALGO)

def current_user(token: str = Depends(oauth2),
                 session: Session = Depends(get_session)) -> User:
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGO])["sub"]
    except jwt.PyJWTError:
        raise HTTPException(401, "Invalid or expired token")
    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(401, "User not found")
    return user


app = FastAPI(title="Task Manager (single-file)")

@app.on_event("startup")
def startup():
    SQLModel.metadata.create_all(engine)


# --- auth routes ---
@app.post("/register", status_code=201)
def register(data: RegisterIn, session: Session = Depends(get_session)):
    if session.exec(select(User).where(User.username == data.username)).first():
        raise HTTPException(409, "Username taken")
    session.add(User(username=data.username, hashed_password=pwd.hash(data.password)))
    session.commit()
    return {"registered": data.username}

@app.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(),
          session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == form.username)).first()
    if not user or not pwd.verify(form.password, user.hashed_password):
        raise HTTPException(401, "Incorrect username or password")
    return {"access_token": create_token(user.username), "token_type": "bearer"}


# --- task routes (per-user) ---
@app.post("/tasks", response_model=TaskPublic, status_code=201)
def create_task(data: TaskCreate, user: User = Depends(current_user),
                session: Session = Depends(get_session)):
    task = Task(**data.model_dump(), user_id=user.id)
    session.add(task); session.commit(); session.refresh(task)
    return task

# Task 3: filtering + search; Task 4: stats before dynamic route
@app.get("/tasks/stats")
def stats(user: User = Depends(current_user), session: Session = Depends(get_session)):
    tasks = session.exec(select(Task).where(Task.user_id == user.id)).all()
    done = sum(1 for t in tasks if t.done)
    return {"total": len(tasks), "done": done, "pending": len(tasks) - done}

@app.get("/tasks", response_model=list[TaskPublic])
def list_tasks(done: bool | None = None, q: str | None = None,
               user: User = Depends(current_user), session: Session = Depends(get_session)):
    query = select(Task).where(Task.user_id == user.id)
    if done is not None:
        query = query.where(Task.done == done)
    tasks = session.exec(query).all()
    if q:
        tasks = [t for t in tasks if q.lower() in t.title.lower()]
    return tasks

def owned(task_id, user, session) -> Task:
    task = session.get(Task, task_id)
    if not task or task.user_id != user.id:
        raise HTTPException(404, f"Task {task_id} not found")
    return task

@app.get("/tasks/{task_id}", response_model=TaskPublic)
def get_task(task_id: int, user: User = Depends(current_user),
             session: Session = Depends(get_session)):
    return owned(task_id, user, session)

@app.patch("/tasks/{task_id}", response_model=TaskPublic)
def update_task(task_id: int, changes: TaskUpdate, user: User = Depends(current_user),
                session: Session = Depends(get_session)):
    task = owned(task_id, user, session)
    for k, v in changes.model_dump(exclude_unset=True).items():
        setattr(task, k, v)
    session.add(task); session.commit(); session.refresh(task)
    return task

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, user: User = Depends(current_user),
                session: Session = Depends(get_session)):
    session.delete(owned(task_id, user, session)); session.commit()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
