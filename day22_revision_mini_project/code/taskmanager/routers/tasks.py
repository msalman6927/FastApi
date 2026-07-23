# taskmanager/routers/tasks.py  -- per-user task CRUD (protected)
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from ..database import get_session
from ..models import Task, TaskCreate, TaskUpdate, TaskPublic, User
from ..auth import get_current_user

# Every route here requires a logged-in user (the get_current_user dependency).
router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskPublic, status_code=201)
def create_task(data: TaskCreate,
                user: User = Depends(get_current_user),
                session: Session = Depends(get_session)):
    task = Task(title=data.title, done=data.done, user_id=user.id)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.get("/", response_model=list[TaskPublic])
def list_tasks(user: User = Depends(get_current_user),
               session: Session = Depends(get_session)):
    # Only THIS user's tasks (per-user isolation = authorization by identity).
    return session.exec(select(Task).where(Task.user_id == user.id)).all()


def _get_owned_task(task_id: int, user: User, session: Session) -> Task:
    task = session.get(Task, task_id)
    if not task or task.user_id != user.id:      # not found OR not yours -> 404
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Task {task_id} not found")
    return task


@router.get("/{task_id}", response_model=TaskPublic)
def get_task(task_id: int, user: User = Depends(get_current_user),
             session: Session = Depends(get_session)):
    return _get_owned_task(task_id, user, session)


@router.patch("/{task_id}", response_model=TaskPublic)
def update_task(task_id: int, changes: TaskUpdate,
                user: User = Depends(get_current_user),
                session: Session = Depends(get_session)):
    task = _get_owned_task(task_id, user, session)
    for key, value in changes.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, user: User = Depends(get_current_user),
                session: Session = Depends(get_session)):
    task = _get_owned_task(task_id, user, session)
    session.delete(task)
    session.commit()
