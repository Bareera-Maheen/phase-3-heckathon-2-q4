from typing import List, Optional
from sqlalchemy.orm import Session
from src.models.task import Task, TaskStatus
from src.models.sql_task import TaskDB
from src.utils.validators import validate_description

class TaskManager:
    """Manages the list of tasks using a Database Session."""
    
    def __init__(self, db: Session):
        self.db = db

    def add_task(self, description: str) -> Task:
        """Adds a new task with the given description."""
        valid_desc = validate_description(description)
        db_task = TaskDB(description=valid_desc, status=TaskStatus.PENDING)
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return self._to_pydantic(db_task)

    def get_all_tasks(self) -> List[Task]:
        """Returns all tasks."""
        db_tasks = self.db.query(TaskDB).all()
        return [self._to_pydantic(t) for t in db_tasks]

    def _find_task(self, task_id: int) -> TaskDB:
        """Helper to find a task by ID."""
        task = self.db.query(TaskDB).filter(TaskDB.id == task_id).first()
        if not task:
            raise ValueError(f"Task {task_id} not found.")
        return task

    def complete_task(self, task_id: int):
        """Marks a task as completed."""
        task = self._find_task(task_id)
        task.status = TaskStatus.COMPLETED
        self.db.commit()

    def reopen_task(self, task_id: int):
        """Marks a task as pending."""
        task = self._find_task(task_id)
        task.status = TaskStatus.PENDING
        self.db.commit()

    def update_task(self, task_id: int, new_description: str):
        """Updates the description of a task."""
        valid_desc = validate_description(new_description)
        task = self._find_task(task_id)
        task.description = valid_desc
        self.db.commit()

    def delete_task(self, task_id: int):
        """Deletes a task."""
        task = self._find_task(task_id)
        self.db.delete(task)
        self.db.commit()

    def _to_pydantic(self, db_task: TaskDB) -> Task:
        """Converts a DB model to a Pydantic model."""
        return Task(id=db_task.id, description=db_task.description, status=db_task.status)