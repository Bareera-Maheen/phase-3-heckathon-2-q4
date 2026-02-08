from enum import Enum
from dataclasses import dataclass

class TaskStatus(Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"

@dataclass
class Task:
    id: int
    description: str
    status: TaskStatus = TaskStatus.PENDING

    def __post_init__(self):
        if not self.description or not self.description.strip():
            raise ValueError("Description cannot be empty.")
