#!/usr/bin/env python3

import argparse
import json
from datetime import datetime, timezone
import os
import sys

TODO_FILE_PATH = os.path.expanduser("~/.streamyutilities_todos.json")
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z" # ISO 8601 with timezone

# --- Data Handling Functions ---
def load_tasks():
    """Loads tasks from the JSON file. Returns an empty list if file not found or invalid."""
    if not os.path.exists(TODO_FILE_PATH):
        return []
    try:
        with open(TODO_FILE_PATH, 'r', encoding='utf-8') as f:
            tasks = json.load(f)
        # Validate basic structure (list of dicts) - can be more thorough
        if not isinstance(tasks, list) or not all(isinstance(t, dict) for t in tasks):
            print(f"Warning: Data in '{TODO_FILE_PATH}' is not in the expected format (list of tasks). Starting fresh if modified.", file=sys.stderr)
            return [] # Or raise an error / attempt recovery
        return tasks
    except json.JSONDecodeError:
        print(f"Warning: Could not decode JSON from '{TODO_FILE_PATH}'. File might be corrupted.", file=sys.stderr)
        return [] # Or raise
    except IOError as e:
        print(f"Error reading todo file '{TODO_FILE_PATH}': {e}", file=sys.stderr)
        return [] # Or raise

def save_tasks(tasks_list):
    """Saves the list of tasks to the JSON file."""
    try:
        with open(TODO_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(tasks_list, f, indent=4)
        return True
    except IOError as e:
        print(f"Error writing to todo file '{TODO_FILE_PATH}': {e}", file=sys.stderr)
        return False

def generate_new_task_id(tasks_list):
    """Generates a new unique ID for a task."""
    if not tasks_list:
        return 1
    return max(task.get('id', 0) for task in tasks_list) + 1

# --- Action Functions ---
def add_task(description):
    tasks = load_tasks()
    new_id = generate_new_task_id(tasks)
    task = {
        "id": new_id,
        "description": description,
        "status": "pending", # "pending" or "completed"
        "created_at": datetime.now(timezone.utc).strftime(DATE_FORMAT),
        "completed_at": None
    }
    tasks.append(task)
    if save_tasks(tasks):
        print(f"Added task {new_id}: \"{description}\"")
    else:
        print("Failed to save new task.")

def list_tasks(status_filter=None, show_ids=True): # Default show_ids to True as per example
    tasks = load_tasks()
    if not tasks:
        print("No tasks in the list.")
        return

    filtered_tasks = tasks
    if status_filter and status_filter != "all":
        filtered_tasks = [task for task in tasks if task.get('status') == status_filter]
        if not filtered_tasks:
            print(f"No tasks found with status '{status_filter}'.")
            return

    print(f"\n--- TODO List ({status_filter or 'all'}) ---")
    for task in filtered_tasks:
        status_marker = "[x]" if task.get('status') == "completed" else "[ ]"
        id_prefix = f"{task.get('id', '?'):>3d}. " if show_ids else ""
        desc = task.get('description', 'No description')
        created_str = task.get('created_at', '')
        created_display = ""
        if created_str:
            try:
                # Attempt to parse and reformat for friendlier display if needed, or show as is
                # dt_created = datetime.strptime(created_str, DATE_FORMAT)
                # created_display = f"(Created: {dt_created.strftime('%Y-%m-%d %H:%M')})"
                created_display = f"(Created: {created_str.split('T')[0]})" # Just date part for brevity
            except ValueError:
                created_display = f"(Created: {created_str})" # Show raw if parse fails

        completed_str = task.get('completed_at')
        completed_display = ""
        if completed_str:
             try:
                completed_display = f"(Completed: {completed_str.split('T')[0]})"
             except Exception:
                completed_display = f"(Completed: {completed_str})"


        print(f"{id_prefix}{status_marker} {desc} {created_display} {completed_display}".strip())
    if not filtered_tasks and (status_filter and status_filter != "all"): # Redundant due to check above
        pass


def mark_task_done(task_id):
    tasks = load_tasks()
    task_found = False
    for task in tasks:
        if task.get('id') == task_id:
            task_found = True
            if task['status'] == "completed":
                print(f"Task {task_id} \"{task['description']}\" is already marked as completed.")
            else:
                task['status'] = "completed"
                task['completed_at'] = datetime.now(timezone.utc).strftime(DATE_FORMAT)
                if save_tasks(tasks):
                    print(f"Marked task {task_id} \"{task['description']}\" as completed.")
                else:
                    print(f"Failed to update task {task_id}.")
            break
    if not task_found:
        print(f"Error: Task with ID {task_id} not found.")

def remove_task(task_id):
    tasks = load_tasks()
    original_len = len(tasks)
    tasks = [task for task in tasks if task.get('id') != task_id]

    if len(tasks) < original_len:
        if save_tasks(tasks):
            print(f"Removed task {task_id}.")
        else:
            print(f"Failed to save changes after removing task {task_id}.")
    else:
        print(f"Error: Task with ID {task_id} not found.")

def edit_task(task_id, new_description):
    tasks = load_tasks()
    task_found = False
    for task in tasks:
        if task.get('id') == task_id:
            task_found = True
            old_description = task['description']
            task['description'] = new_description
            # Optionally update a 'modified_at' timestamp here
            if save_tasks(tasks):
                print(f"Edited task {task_id}: from \"{old_description}\" to \"{new_description}\"")
            else:
                print(f"Failed to save changes for task {task_id}.")
            break
    if not task_found:
        print(f"Error: Task with ID {task_id} not found.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple command-line to-do list manager.")
    subparsers = parser.add_subparsers(dest="action", title="Actions", help="Available actions", required=True)

    # Add command
    parser_add = subparsers.add_parser("add", help="Add a new task.")
    parser_add.add_argument("description", type=str, help="The description of the task.")

    # List command
    parser_list = subparsers.add_parser("list", help="List tasks.")
    parser_list.add_argument(
        "--status",
        choices=["pending", "completed", "all"],
        default="all", # Or 'pending' if preferred as default
        help="Filter tasks by status. Default: 'all'."
    )
    parser_list.add_argument(
        "--no-ids", # Changed from --ids to --no-ids to make IDs default
        action="store_false",
        dest="show_ids", # store result in show_ids
        help="Hide task IDs in the list."
    )
    parser_list.set_defaults(show_ids=True)


    # Done command
    parser_done = subparsers.add_parser("done", help="Mark a task as completed.")
    parser_done.add_argument("task_id", type=int, help="The ID of the task to mark as completed.")

    # Remove command
    parser_remove = subparsers.add_parser("remove", help="Remove a task.")
    parser_remove.add_argument("task_id", type=int, help="The ID of the task to remove.")

    # Edit command
    parser_edit = subparsers.add_parser("edit", help="Edit an existing task's description.")
    parser_edit.add_argument("task_id", type=int, help="The ID of the task to edit.")
    parser_edit.add_argument("new_description", type=str, help="The new description for the task.")

    args = parser.parse_args()

    if args.action == "add":
        add_task(args.description)
    elif args.action == "list":
        list_tasks(args.status, args.show_ids)
    elif args.action == "done":
        mark_task_done(args.task_id)
    elif args.action == "remove":
        remove_task(args.task_id)
    elif args.action == "edit":
        edit_task(args.task_id, args.new_description)
    else:
        parser.print_help() # Should not be reached due to 'required=True' for subparsers

    sys.exit(0)
