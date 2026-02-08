from sqlmodel import Session, select
from src.database import engine
from src.models.entities import Task, TaskStatus, Priority
from src.mcp.utils import tool
from uuid import UUID
from datetime import datetime
from typing import Optional

@tool()
def add_task(user_id: str, title: str, description: Optional[str] = None, priority: Priority = Priority.MEDIUM, deadline: Optional[str] = None):
    """Add a new todo task.
    
    Args:
        title: The title of the task
        description: A detailed description of the task
        priority: The priority of the task (low, medium, high)
        deadline: ISO format deadline string (YYYY-MM-DDTHH:MM:SS)
    """
    with Session(engine) as session:
        task = Task(
            title=title,
            description=description,
            priority=priority,
            deadline=datetime.fromisoformat(deadline) if deadline else None,
            user_id=user_id
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return (True, task.dict())

@tool()
def update_task(user_id: str, task_id: str, title: Optional[str] = None, description: Optional[str] = None, priority: Optional[Priority] = None):
    """Update an existing task.
    
    Args:
        task_id: The UUID of the task to update
        title: New title for the task
        description: New description for the task
        priority: New priority for the task
    """
    with Session(engine) as session:
        statement = select(Task).where(Task.id == UUID(task_id), Task.user_id == user_id)
        task = session.exec(statement).first()
        if not task:
            return (False, "Task not found")
        
        if title: task.title = title
        if description: task.description = description
        if priority: task.priority = priority
        
        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)
        return (True, task.dict())

@tool()
def complete_task(user_id: str, task_id: str):
    """Mark a task as completed.
    
    Args:
        task_id: The UUID of the task to complete
    """
    with Session(engine) as session:
        statement = select(Task).where(Task.id == UUID(task_id), Task.user_id == user_id)
        task = session.exec(statement).first()
        if not task:
            return (False, "Task not found")
        
        task.status = TaskStatus.COMPLETED
        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        return (True, f"Task {task_id} marked as completed")

@tool()
def delete_task(user_id: str, task_id: str):
    """Delete a task.
    
    Args:
        task_id: The UUID of the task to delete
    """
    with Session(engine) as session:
        statement = select(Task).where(Task.id == UUID(task_id), Task.user_id == user_id)
        task = session.exec(statement).first()
        if not task:
            return (False, "Task not found")
        
        session.delete(task)
        session.commit()
        return (True, f"Task {task_id} deleted")

@tool()
def list_tasks(user_id: str, status: Optional[TaskStatus] = None, priority: Optional[Priority] = None):
    """List and filter tasks.
    
    Args:
        status: Filter by status (pending, completed)
        priority: Filter by priority (low, medium, high)
    """
    with Session(engine) as session:
        statement = select(Task).where(Task.user_id == user_id)
        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = statement.where(Task.priority == priority)
        
        tasks = session.exec(statement).all()
        return (True, [t.dict() for t in tasks])