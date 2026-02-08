import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.services.task_manager import TaskManager
from src.models.task import TaskStatus
from src.database import Base
from src.models import sql_task

# Setup in-memory DB for tests
engine = create_engine("sqlite:///:memory:")
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_add_task(db_session):
    manager = TaskManager(db_session)
    task = manager.add_task("Buy milk")
    assert task.id == 1
    assert task.description == "Buy milk"
    assert task.status == TaskStatus.PENDING
    assert len(manager.get_all_tasks()) == 1
    
    task2 = manager.add_task("Walk dog")
    assert task2.id == 2
    assert len(manager.get_all_tasks()) == 2

def test_get_all_tasks(db_session):
    manager = TaskManager(db_session)
    manager.add_task("Task 1")
    manager.add_task("Task 2")
    tasks = manager.get_all_tasks()
    assert len(tasks) == 2
    assert tasks[0].description == "Task 1"
    assert tasks[1].description == "Task 2"

def test_complete_task(db_session):
    manager = TaskManager(db_session)
    task = manager.add_task("Buy milk")
    manager.complete_task(task.id)
    # Refresh logic inside manager handles DB update, we check via find or get_all
    updated_task = manager._find_task(task.id)
    assert updated_task.status == TaskStatus.COMPLETED

def test_reopen_task(db_session):
    manager = TaskManager(db_session)
    task = manager.add_task("Buy milk")
    manager.complete_task(task.id)
    manager.reopen_task(task.id)
    updated_task = manager._find_task(task.id)
    assert updated_task.status == TaskStatus.PENDING

def test_complete_task_not_found(db_session):
    manager = TaskManager(db_session)
    with pytest.raises(ValueError, match="Task 999 not found"):
        manager.complete_task(999)

def test_update_task(db_session):
    manager = TaskManager(db_session)
    task = manager.add_task("Buy milk")
    manager.update_task(task.id, "Buy almond milk")
    updated_task = manager._find_task(task.id)
    assert updated_task.description == "Buy almond milk"

def test_delete_task(db_session):
    manager = TaskManager(db_session)
    task = manager.add_task("Buy milk")
    manager.delete_task(task.id)
    assert len(manager.get_all_tasks()) == 0
    with pytest.raises(ValueError):
        manager.complete_task(task.id)
