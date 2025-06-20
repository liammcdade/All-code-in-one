#!/usr/bin/env python3

import os
import shutil
import argparse
import json
from datetime import datetime

TRASH_BASE_DIR = os.path.expanduser("~/.local/share/streamyutilities_trash")
TRASH_FILES_DIR = os.path.join(TRASH_BASE_DIR, "files")
TRASH_LOG_FILE = os.path.join(TRASH_BASE_DIR, "trash.log")

def ensure_trash_exists():
    """Ensures the trash directory and log file structure exists."""
    os.makedirs(TRASH_FILES_DIR, exist_ok=True)
    if not os.path.exists(TRASH_LOG_FILE):
        # Create an empty log file if it doesn't exist, perhaps with a header if CSV
        # For JSON lines, just ensuring it can be appended to is fine.
        open(TRASH_LOG_FILE, 'a').close()

def log_deletion(original_path, trash_path, item_type):
    """Logs metadata about the deleted item."""
    log_entry = {
        "original_path": os.path.abspath(original_path),
        "trash_path": trash_path,
        "item_type": item_type,
        "deleted_at": datetime.now().isoformat()
    }
    try:
        with open(TRASH_LOG_FILE, 'a') as f:
            f.write(json.dumps(log_entry) + "\n")
    except IOError as e:
        print(f"Warning: Could not write to trash log: {e}")

def safe_delete_item(item_path):
    """Safely deletes a single item by moving it to the trash directory."""
    if not os.path.exists(item_path):
        print(f"Error: Source '{item_path}' does not exist. Skipping.")
        return False

    base_name = os.path.basename(item_path)
    target_trash_path = os.path.join(TRASH_FILES_DIR, base_name)

    # Handle name conflicts
    counter = 1
    original_name_part, original_ext_part = os.path.splitext(base_name)
    temp_base_name = base_name # Initialize with the original base name

    while os.path.exists(target_trash_path):
        # Construct new name: original_name_copyN.ext
        temp_base_name = f"{original_name_part}_copy{counter}{original_ext_part}"
        target_trash_path = os.path.join(TRASH_FILES_DIR, temp_base_name)
        counter += 1

        # Safety check for extremely long filenames
        if len(temp_base_name) > 250: # Max filename length is often around 255 chars
            # This is a fallback, ideally this situation is rare.
            # A more robust solution might involve hashing or a different naming scheme for extreme cases.
            print(f"Warning: Generated filename for '{base_name}' is getting very long. Trying timestamp.")
            timestamp_suffix = datetime.now().strftime("%Y%m%d%H%M%S%f") # added microsecs for more uniqueness
            temp_base_name = f"{original_name_part}_{timestamp_suffix}{original_ext_part}"
            target_trash_path = os.path.join(TRASH_FILES_DIR, temp_base_name)
            # If even this collides (extremely unlikely), it will error out or be caught by a re-loop.
            if os.path.exists(target_trash_path):
                 print(f"Error: Could not resolve filename conflict for '{base_name}' even with timestamp. Skipping.")
                 return False
            break # Exit loop after trying timestamp

    item_type = "directory" if os.path.isdir(item_path) else "file"
    try:
        shutil.move(item_path, target_trash_path)
        log_deletion(item_path, target_trash_path, item_type)
        print(f"Moved '{item_path}' to trash: '{target_trash_path}'")
        return True
    except Exception as e:
        print(f"Error moving '{item_path}' to trash: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Safely move files or directories to a designated trash location.",
        epilog="Example: python safeDelete.py /path/to/file.txt /path/to/folder"
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help="One or more file or directory paths to move to trash."
    )

    args = parser.parse_args()

    ensure_trash_exists()

    success_count = 0
    for item_path in args.paths:
        if safe_delete_item(item_path):
            success_count += 1

    print(f"\nSafely deleted {success_count} out of {len(args.paths)} item(s).")
