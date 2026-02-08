from sqlalchemy import Column, Integer, String, Enum as SQLEnum
from src.database import Base
from src.models.task import TaskStatus
import enum

class TaskDB(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.PENDING)
