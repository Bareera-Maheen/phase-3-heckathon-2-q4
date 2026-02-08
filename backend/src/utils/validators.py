def validate_description(description: str) -> str:
    """Validates that the description is not empty."""
    if not description or not description.strip():
        raise ValueError("Description cannot be empty.")
    return description.strip()

def validate_id(task_id: str) -> int:
    """Validates that the task_id is a positive integer."""
    try:
        id_val = int(task_id)
        if id_val <= 0:
            raise ValueError("Task ID must be a positive integer.")
        return id_val
    except ValueError:
        raise ValueError("Task ID must be a valid integer.")
