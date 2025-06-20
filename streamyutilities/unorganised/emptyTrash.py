#!/usr/bin/env python3

import os
import shutil
import argparse
import json
from datetime import datetime, timedelta

TRASH_BASE_DIR = os.path.expanduser("~/.local/share/streamyutilities_trash")
TRASH_FILES_DIR = os.path.join(TRASH_BASE_DIR, "files")
TRASH_LOG_FILE = os.path.join(TRASH_BASE_DIR, "trash.log")

def ensure_trash_structure_exists():
    """Checks if the basic trash directory exists."""
    if not os.path.isdir(TRASH_FILES_DIR) or not os.path.isfile(TRASH_LOG_FILE):
        print("Trash directory or log file not found. Looks like safeDelete hasn't been used or trash is clean.")
        return False
    return True

def load_trash_log():
    """Loads trash log entries. Returns a list of dictionaries."""
    if not os.path.exists(TRASH_LOG_FILE):
        return []
    entries = []
    try:
        with open(TRASH_LOG_FILE, 'r') as f:
            for line in f:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    print(f"Warning: Skipping corrupted log line: {line.strip()}")
    except IOError:
        print("Warning: Could not read trash log file.")
    return entries

def save_trash_log(log_entries):
    """Saves updated log entries back to the trash log file."""
    try:
        with open(TRASH_LOG_FILE, 'w') as f:
            for entry in log_entries:
                f.write(json.dumps(entry) + "\n")
    except IOError:
        print("Error: Could not write to trash log file. Log may be inconsistent.")

def get_item_display_info(log_entry):
    """Formats a log entry for display."""
    trashed_name = os.path.basename(log_entry.get("trash_path", "Unknown Trashed Path"))
    original_path = log_entry.get("original_path", "Unknown Original Path")
    deleted_at_str = log_entry.get("deleted_at", "Unknown Deletion Time")
    try:
        deleted_at_dt = datetime.fromisoformat(deleted_at_str)
        time_ago = datetime.now() - deleted_at_dt
        if time_ago.days > 0:
            ago_str = f"{time_ago.days} days ago"
        elif time_ago.seconds // 3600 > 0:
            ago_str = f"{time_ago.seconds // 3600} hours ago"
        else:
            ago_str = "recently"
        deleted_info = f"deleted {ago_str} ({deleted_at_dt.strftime('%Y-%m-%d %H:%M')})"
    except ValueError:
        deleted_info = f"deleted at {deleted_at_str}"

    return f"- '{trashed_name}' (Original: '{original_path}', Type: {log_entry.get('item_type', 'N/A')}, {deleted_info})"

def list_trash_items():
    if not ensure_trash_structure_exists():
        return

    log_entries = load_trash_log()
    actual_files_in_trash = set(os.listdir(TRASH_FILES_DIR))
    logged_trashed_basenames = set()

    if not log_entries and not actual_files_in_trash:
        print("Trash is empty.")
        return

    print("Items currently in trash (according to log):")
    if not log_entries:
        print("  Log is empty.")

    for entry in log_entries:
        print(f"  {get_item_display_info(entry)}")
        logged_trashed_basenames.add(os.path.basename(entry.get("trash_path")))

    # Check for discrepancies
    orphaned_files = actual_files_in_trash - logged_trashed_basenames
    if orphaned_files:
        print("\nOrphaned files in trash (present in files directory but not in log):")
        for fname in orphaned_files:
            print(f"  - '{fname}' (Full path: {os.path.join(TRASH_FILES_DIR, fname)})")

    missing_files = logged_trashed_basenames - actual_files_in_trash
    if missing_files:
        print("\nMissing files (in log but not in files directory - log may need cleaning):")
        for fname in missing_files:
            # Find original log entry for more info
            missing_entry_info = "Unknown original path"
            for entry in log_entries:
                if os.path.basename(entry.get("trash_path")) == fname:
                    missing_entry_info = entry.get("original_path", missing_entry_info)
                    break
            print(f"  - '{fname}' (Logged original: '{missing_entry_info}')")


def confirm_deletion(count):
    if count == 0:
        print("No items selected for deletion.")
        return False
    try:
        confirm = input(f"Permanently delete {count} item(s) from trash? (yes/no): ").strip().lower()
    except EOFError:
        print("\nConfirmation input not available. Aborting.")
        return False
    return confirm == 'yes'


def delete_selected_items(items_to_delete_basenames, all_log_entries):
    """
    Deletes specified items from file system and log.
    items_to_delete_basenames: set of basenames of files/dirs in TRASH_FILES_DIR.
    all_log_entries: list of all current log entries.
    Returns: count of successfully deleted items, updated log entries.
    """
    if not confirm_deletion(len(items_to_delete_basenames)):
        print("Deletion aborted by user.")
        return 0, all_log_entries

    updated_log_entries = []
    fs_deleted_successfully_basenames = set()

    for basename in items_to_delete_basenames:
        item_path_in_trash = os.path.join(TRASH_FILES_DIR, basename)
        try:
            if os.path.exists(item_path_in_trash): # Check if it exists before trying to delete
                if os.path.isfile(item_path_in_trash) or os.path.islink(item_path_in_trash):
                    os.remove(item_path_in_trash)
                elif os.path.isdir(item_path_in_trash):
                    shutil.rmtree(item_path_in_trash)
                else:
                    print(f"Warning: '{basename}' is not a file or directory. Skipping FS removal.")
                    continue # Not adding to fs_deleted_successfully_basenames
                print(f"Permanently deleted '{basename}' from trash files.")
            else:
                # File was already gone, but we intended to remove it. Consider it "successfully handled" for log cleanup.
                print(f"Note: '{basename}' was already gone from trash files directory.")

            fs_deleted_successfully_basenames.add(basename) # Add if FS deletion succeeded or file was already gone

        except OSError as e:
            print(f"Error deleting '{basename}' from trash files: {e}")
            # Do not add to fs_deleted_successfully_basenames if FS deletion failed

    # Filter log entries based on fs_deleted_successfully_basenames
    # Log entries are removed if their corresponding file system item was successfully deleted OR was already gone.
    for entry in all_log_entries:
        entry_basename = os.path.basename(entry.get("trash_path", ""))
        if entry_basename not in fs_deleted_successfully_basenames:
            updated_log_entries.append(entry)

    if fs_deleted_successfully_basenames: # If any FS operations were successful (or files confirmed gone)
         save_trash_log(updated_log_entries)
         print(f"Successfully processed {len(fs_deleted_successfully_basenames)} item(s): files removed/confirmed gone from filesystem and log updated.")

    return len(fs_deleted_successfully_basenames), updated_log_entries


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Manage and empty the streamyutilities trash.",
        epilog="Example: python emptyTrash.py --days 30"
    )
    group = parser.add_mutually_exclusive_group(required=True) # At least one action is required
    group.add_argument("--list", action="store_true", help="List items currently in trash.")
    group.add_argument("--all", action="store_true", help="Delete all items from trash.")
    group.add_argument("--name", metavar="TRASHED_NAME", help="Delete a specific item by its name in the trash files directory.")
    group.add_argument("--days", metavar="N", type=int, help="Delete items older than N days.")

    args = parser.parse_args()

    if not os.path.isdir(TRASH_BASE_DIR):
        print(f"Trash directory '{TRASH_BASE_DIR}' does not exist. Nothing to do.")
        exit(0)

    current_log_entries = load_trash_log()
    files_to_delete_basenames = set() # Basenames of items in TRASH_FILES_DIR

    if args.list:
        list_trash_items()
    elif args.all:
        print("Selected to delete ALL items from trash.")
        # Include orphaned files as well by listing all files in TRASH_FILES_DIR
        if os.path.isdir(TRASH_FILES_DIR):
             files_to_delete_basenames.update(os.listdir(TRASH_FILES_DIR))
        # No need to consult log for selection, but will use it for final reconciliation
        if not files_to_delete_basenames:
            print("Trash files directory is already empty.")
        delete_selected_items(files_to_delete_basenames, current_log_entries)

    elif args.name:
        print(f"Selected to delete item by name: '{args.name}'")
        item_full_path = os.path.join(TRASH_FILES_DIR, args.name)
        if os.path.exists(item_full_path):
            files_to_delete_basenames.add(args.name)
            delete_selected_items(files_to_delete_basenames, current_log_entries)
        else:
            print(f"Item '{args.name}' not found in trash files directory: '{TRASH_FILES_DIR}'.")
            # Check if it's only in the log (a discrepancy)
            is_in_log = any(os.path.basename(entry.get("trash_path", "")) == args.name for entry in current_log_entries)
            if is_in_log:
                print(f"Item '{args.name}' found in log, but not in file system. You may want to run with --all or clear specific log entries if this is frequent.")
                # Optionally, offer to remove just the log entry
                if confirm_deletion(1): # "1" because we are "deleting" one log entry
                    print(f"Removing log entry for '{args.name}'.")
                    # This is a special case of delete_selected_items where the item is already gone from FS
                    # We pass its basename so its log entry is removed.
                    delete_selected_items({args.name}, current_log_entries)


    elif args.days is not None:
        if args.days < 0:
            print("Error: Number of days must be non-negative.")
            exit(1)

        print(f"Selected to delete items older than {args.days} days.")
        cutoff_date = datetime.now() - timedelta(days=args.days)

        for entry in current_log_entries:
            try:
                deleted_at_dt = datetime.fromisoformat(entry.get("deleted_at"))
                if deleted_at_dt < cutoff_date:
                    basename = os.path.basename(entry.get("trash_path"))
                    # Check if file actually exists before adding to delete list
                    # This handles cases where log is out of sync
                    if os.path.exists(os.path.join(TRASH_FILES_DIR, basename)):
                         files_to_delete_basenames.add(basename)
                    else:
                        # File is in log, old enough, but not in TRASH_FILES_DIR.
                        # These log entries will be removed if user confirms general deletion.
                        # Add its basename to ensure its log entry is cleaned up if general deletion proceeds.
                        print(f"Note: Logged item '{basename}' (original: {entry.get('original_path')}) is older than {args.days} days but already missing from trash files. Will clean its log entry if deletion proceeds.")
                        files_to_delete_basenames.add(basename) # Add to ensure log cleanup
            except (ValueError, TypeError):
                print(f"Warning: Could not parse deletion date for log entry: {entry.get('trash_path')}. Skipping for age check.")

        if not files_to_delete_basenames:
            print(f"No items found older than {args.days} days or trash is empty.")
        else:
            delete_selected_items(files_to_delete_basenames, current_log_entries)
    else:
        parser.print_help()
