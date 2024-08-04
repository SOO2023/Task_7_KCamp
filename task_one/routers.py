from fastapi import APIRouter, status, Depends
from .schemas import TaskIn, TaskOut, TaskUpdate
from .util import (
    get_all_items,
    get_item_by_id,
    create_new_item,
    delete_item,
    update_item,
)
from .models import Tasks
from sqlalchemy.orm import Session
from .database import db_session

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/{task_id}", response_model=TaskOut, description="Get task using task id")
def get_task(task_id: int, db: Session = Depends(db_session)):
    task = get_item_by_id(task_id, db, Tasks, "task")
    return task


@router.get("/", response_model=list[TaskOut], description="Get all tasks")
def get_all_tasks(db: Session = Depends(db_session)):
    tasks = get_all_items(db, Tasks)
    return tasks


@router.post(
    "/",
    response_model=TaskOut,
    status_code=status.HTTP_201_CREATED,
    description="Create a new task",
)
def create_task(task: TaskIn, db: Session = Depends(db_session)):
    task = create_new_item(task.model_dump(), db, Tasks)
    return task


@router.put(
    "/{task_id}",
    response_model=TaskOut,
    status_code=status.HTTP_201_CREATED,
    description="Update task",
)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(db_session)):
    task = update_item(task_id, task.model_dump(), db, Tasks, "task")
    return task


@router.delete(
    "/{task_id}", status_code=status.HTTP_204_NO_CONTENT, description="Delete task"
)
def delete_task(task_id: int, db: Session = Depends(db_session)):
    delete_item(task_id, db, Tasks, "task")
