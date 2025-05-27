import json
import os

FILE_NAME = "tasks.json"
tasks = []

def load_tasks():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []

def save_tasks():
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4)

def add_task():
    task = input("Enter a new task: ").strip()
    if not task:
        print("Task cannot be empty.")
        return

    task_type = input("Is this a daily or project task? (daily/project): ").strip().lower()
    if task_type not in ["daily", "project"]:
        print("Invalid type. Defaulting to daily.")
        task_type = "daily"

    if task_type == "project":
        due_date = input("Enter due date (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Task not added.")
            return

        priority = input("Enter priority (Low, Medium, High): ").strip().capitalize()
        if priority not in ["Low", "Medium", "High"]:
            print("Invalid priority. Defaulting to 'Low'.")
            priority = "Low"
    else:
        due_date = ""
        priority = ""

    tasks.append({
        "task": task,
        "completed": False,
        "type": task_type,
        "due_date": due_date,
        "priority": priority
    })
    save_tasks()
    print(f"Added: {task} [{task_type}]")

from datetime import datetime

from datetime import datetime

def view_tasks():
    if not tasks:
        print("No tasks yet.")
        return

    # Step 1: Filter Prompt
    print("\nView which tasks?")
    print("1. All Tasks")
    print("2. Only Daily Tasks")
    print("3. Only Project Tasks")
    choice = input("Select (1/2/3): ").strip()

    if choice not in ["1", "2", "3"]:
        print("Invalid choice.")
        return

    # Step 2: Apply Filter
    filtered = []
    for t in tasks:
        t_type = t.get("type", "daily")
        if choice == '1':
            filtered.append(t)
        elif choice == '2' and t_type == "daily":
            filtered.append(t)
        elif choice == '3' and t_type == "project":
            filtered.append(t)

    if not filtered:
        print("No matching tasks found.")
        return

    # Step 3: Optional Sorting (only for project tasks)
    if choice == '3':
        print("\nSort tasks?")
        print("1. No Sorting")
        print("2. By Priority (High → Low)")
        print("3. By Due Date (Soonest First)")
        sort_choice = input("Choose sort option (1/2/3): ").strip()

        if sort_choice == '2':
            priority_order = {"High": 3, "Medium": 2, "Low": 1}
            filtered.sort(key=lambda t: priority_order.get(t.get("priority", "Low")), reverse=True)
        elif sort_choice == '3':
            def parse_due(t):
                try:
                    return datetime.strptime(t.get("due_date", ""), "%Y-%m-%d")
                except:
                    return datetime.max
            filtered.sort(key=parse_due)

    # Step 4: Display
    print("\nYour Tasks:")
    for i, t in enumerate(filtered):
        status = "✓" if t["completed"] else " "
        t_type = t.get("type", "daily")
        if t_type == "project":
            due = t.get("due_date", "N/A")
            prio = t.get("priority", "Low")
            print(f"{i + 1}. [{status}] {t['task']} (Project - Due: {due}, Priority: {prio})")
        else:
            print(f"{i + 1}. [{status}] {t['task']} (Daily)")
    print()

def get_filtered_tasks():
    filtered = []
    for t in tasks:
        t_type = t.get("type", "daily")
        filtered.append(t)
    return filtered


def complete_task():
    view_tasks()
    try:
        num = int(input("Enter task number to mark complete: "))
        tasks[num - 1]["completed"] = True
        save_tasks()
        print("Task marked as complete.")
    except (ValueError, IndexError):
        print("Invalid task number.")

def delete_task():
    filtered = get_filtered_tasks()

    if not filtered:
        print("No tasks to delete.")
        return

    print("\nYour Tasks:")
    for i, t in enumerate(filtered):
        status = "✓" if t["completed"] else " "
        t_type = t.get("type", "daily")
        if t_type == "project":
            due = t.get("due_date", "N/A")
            prio = t.get("priority", "Low")
            print(f"{i + 1}. [{status}] {t['task']} (Project - Due: {due}, Priority: {prio})")
        else:
            print(f"{i + 1}. [{status}] {t['task']} (Daily)")

    try:
        num = int(input("Enter task number to delete: "))
        if num < 1 or num > len(filtered):
            raise IndexError
        removed = tasks.pop(tasks.index(filtered[num - 1]))
        save_tasks()
        print(f"Deleted: {removed['task']}")
    except (ValueError, IndexError):
        print("Invalid task number.")


def menu():
    global tasks
    tasks = load_tasks()

    while True:
        print("------ To-Do List ------")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task Complete")
        print("4. Delete Task")
        print("5. Exit")

        choice = input("Choose an option (1-5): ").strip()

        if choice == '1':
            add_task()
        elif choice == '2':
            view_tasks()
        elif choice == '3':
            complete_task()
        elif choice == '4':
            delete_task()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    menu()
