import sys
from src.services.task_manager import TaskManager
from src.ui.cli import (
    print_welcome, print_menu, get_menu_selection, 
    print_error, print_success, get_input, print_tasks
)
from src.utils.validators import validate_id
from src.database import SessionLocal, engine
from src.models import sql_task

# Init DB
sql_task.Base.metadata.create_all(bind=engine)

def main():
    """Entry point for the Todo CLI application."""
    print_welcome()
    
    # DB Session management
    db = SessionLocal()
    manager = TaskManager(db)

    try:
        while True:
            print_menu()
            selection = get_menu_selection()
            
            try:
                if selection == "1": # Add
                    desc = get_input("Enter task description: ")
                    if not desc:
                        print_error("Description cannot be empty.")
                    else:
                        task = manager.add_task(desc)
                        print_success(f"Task {task.id} added.")
                
                elif selection == "2": # List
                    tasks = manager.get_all_tasks()
                    print_tasks(tasks)
                
                elif selection == "3": # Update
                    id_str = get_input("Enter task ID: ")
                    task_id = validate_id(id_str)
                    new_desc = get_input("Enter new description: ")
                    if not new_desc:
                        print_error("Description cannot be empty.")
                    else:
                        manager.update_task(task_id, new_desc)
                        print_success(f"Task {task_id} updated.")

                elif selection == "4": # Delete
                    id_str = get_input("Enter task ID: ")
                    task_id = validate_id(id_str)
                    manager.delete_task(task_id)
                    print_success(f"Task {task_id} deleted.")

                elif selection == "5": # Complete
                    id_str = get_input("Enter task ID: ")
                    task_id = validate_id(id_str)
                    manager.complete_task(task_id)
                    print_success(f"Task {task_id} marked as completed.")

                elif selection == "6": # Incomplete
                    id_str = get_input("Enter task ID: ")
                    task_id = validate_id(id_str)
                    manager.reopen_task(task_id)
                    print_success(f"Task {task_id} marked as pending.")

                elif selection == "7": # Exit
                    print("Goodbye!")
                    print("Final Task List:")
                    print_tasks(manager.get_all_tasks())
                    sys.exit(0)
                
                else:
                    print_error("Invalid selection. Please try again.")

            except ValueError as e:
                print_error(str(e))
            except Exception as e:
                print_error(f"Unexpected error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
