import logging

from auth import AuthCheckDep
from db import DBSessionDep
from db.models import Task, TaskCreate, TaskPublic, TaskUpdate
from fastapi import APIRouter, HTTPException
from pydantic import UUID4
from sqlmodel import select

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/")
def create_task(
    task_details: TaskCreate, session: DBSessionDep, user: AuthCheckDep
) -> UUID4:
    task = Task(created_by=user.id, **task_details.model_dump(exclude_unset=True))
    session.add(task)
    session.commit()
    session.refresh(task)
    logger.info(f"Task {task.title!r} created with ID {task.id}")
    return task.id


@router.get("/{task_id}")
def read_task(task_id: UUID4, session: DBSessionDep) -> TaskPublic:
    task = session.get(Task, task_id)
    if not task:
        logger.warning(f"Task with ID {task_id} not found")
        raise HTTPException(status_code=404, detail="Task not found")
    logger.info(f"Task {task.title!r} retrieved with ID {task.id}")
    return task


@router.get("/")
def read_all_tasks(session: DBSessionDep) -> list[TaskPublic]:
    tasks = session.exec(select(Task)).all()
    logger.info(f"Retrieved {len(tasks)} tasks")
    return tasks


@router.delete("/{task_id}")
def delete_task(task_id: UUID4, session: DBSessionDep, user: AuthCheckDep) -> None:
    task = session.get(Task, task_id)
    if not task:
        logger.warning(f"Task with ID {task_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    if task.created_by != user.id and (
        task.assigned_to and task.assigned_to != user.id
    ):
        logger.warning(
            f"User {user.username} not authorized to delete task {task.title!r}"
        )
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this task"
        )

    session.delete(task)
    session.commit()
    logger.info(f"Task {task.title!r} deleted with ID {task.id}")


@router.patch("/{task_id}")
def update_task(
    task_id: UUID4, task_details: TaskUpdate, session: DBSessionDep, user: AuthCheckDep
) -> TaskPublic:
    task = session.get(Task, task_id)
    if not task:
        logger.warning(f"Task with ID {task_id} not found")
        raise HTTPException(status_code=404, detail="User not found")

    if task.created_by != user.id and (
        task.assigned_to and task.assigned_to != user.id
    ):
        logger.warning(
            f"User {user.username} not authorized to update task {task.title!r}"
        )
        raise HTTPException(
            status_code=403, detail="Not authorized to update this task"
        )

    for key, value in task_details.model_dump(exclude_unset=True).items():
        setattr(task, key, value)

    session.commit()
    session.refresh(task)
    logger.info(f"Task {task.title!r} updated with ID {task.id}")
    return task
