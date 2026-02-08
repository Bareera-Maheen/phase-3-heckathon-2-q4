import sys
from typing import List
from src.models.task import Task, TaskStatus

def print_welcome():
    print("Welcome to Todo CLI!")

def print_menu():
    print("\n=== Todo Menu ===")
    print("1. Add Task")
    print("2. List Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Complete")
    print("6. Mark Incomplete")
    print("7. Exit")
    print("=================")

def get_menu_selection() -> str:
    return get_input("Select an option: ")

def print_error(message: str):
    print(f"Error: {message}")

def print_success(message: str):
    print(f"Success: {message}")

def get_input(prompt: str = "> ") -> str:
    try:
        return input(prompt).strip()
    except EOFError:
        return "7" # Default to exit on EOF

def format_task(task: Task) -> str:
    status_mark = "x" if task.status == TaskStatus.COMPLETED else " "
    return f"[{status_mark}] {task.id}: {task.description}"

def print_tasks(tasks: List[Task]):
    if not tasks:
        print("No tasks found.")
        return
    for task in tasks:
        print(format_task(task))