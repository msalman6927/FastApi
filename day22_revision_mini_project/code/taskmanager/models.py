# taskmanager/models.py  -- SQLModel tables + Pydantic API models (Days 12,16,18)
from sqlmodel import SQLModel, Field


# ---- Database tables ----
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str


class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    done: bool = False
    user_id: int = Field(foreign_key="user.id")   # which user owns this task


# ---- API models (input/output separation) ----
class RegisterIn(SQLModel):
    username: str
    password: str


class TaskCreate(SQLModel):
    title: str
    done: bool = False


class TaskUpdate(SQLModel):
    title: str | None = None
    done: bool | None = None


class TaskPublic(SQLModel):
    id: int
    title: str
    done: bool
