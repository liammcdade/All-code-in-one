#!/usr/bin/env python3

import os
import shutil
import argparse
import tarfile
import zipfile
from datetime import datetime

def create_backup(source_path, destination_dir=None, archive_format="zip"):
    """
    Creates a backup of a source file or directory.
    """
    if not os.path.exists(source_path):
        print(f"Error: Source path '{source_path}' does not exist.")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = os.path.basename(source_path)

    # Determine backup destination directory
    if destination_dir:
        backup_dest_dir = destination_dir
    else:
        # Try to create a 'backups' subdirectory in the source's parent directory
        parent_dir_of_source = os.path.dirname(os.path.abspath(source_path))
        proposed_backup_dir = os.path.join(parent_dir_of_source, "backups")

        # Fallback to ~/.backups if parent_dir_of_source is not writable or not preferred
        # For simplicity, we'll try to create it. If it fails, we'll use ~/.backups
        # A more robust check would involve os.access(parent_dir_of_source, os.W_OK)
        # but creating it and catching error is also a way.
        try:
            if not os.path.exists(proposed_backup_dir):
                 os.makedirs(proposed_backup_dir, exist_ok=True)
            backup_dest_dir = proposed_backup_dir
        except OSError:
            print(f"Warning: Could not create or access '{proposed_backup_dir}'.")
            user_home_backups = os.path.expanduser("~/.backups")
            print(f"Defaulting to user backup directory: '{user_home_backups}'")
            backup_dest_dir = user_home_backups

    # Ensure the final backup destination directory exists
    try:
        if not os.path.exists(backup_dest_dir):
            os.makedirs(backup_dest_dir, exist_ok=True)
            print(f"Created backup directory: '{backup_dest_dir}'")
    except OSError as e:
        print(f"Error: Could not create destination directory '{backup_dest_dir}': {e}")
        return

    # Construct backup filename
    if os.path.isfile(source_path):
        name, ext = os.path.splitext(base_name)
        backup_filename = f"{name}_backup_{timestamp}{ext if ext else '.bak'}"
        backup_filepath = os.path.join(backup_dest_dir, backup_filename)
        try:
            shutil.copy2(source_path, backup_filepath)
            print(f"Successfully backed up file '{source_path}' to '{backup_filepath}'")
        except Exception as e:
            print(f"Error backing up file '{source_path}': {e}")

    elif os.path.isdir(source_path):
        backup_filename_base = f"{base_name}_backup_{timestamp}"

        if archive_format == "zip":
            backup_filepath = os.path.join(backup_dest_dir, f"{backup_filename_base}.zip")
            try:
                with zipfile.ZipFile(backup_filepath, 'w', zipfile.ZIP_DEFLATED) as zf:
                    for root, _, files in os.walk(source_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            # Add file to zip, preserving structure relative to source_path
                            arcname = os.path.relpath(file_path, source_path)
                            zf.write(file_path, arcname)
                print(f"Successfully backed up directory '{source_path}' to '{backup_filepath}'")
            except Exception as e:
                print(f"Error creating zip archive for '{source_path}': {e}")

        elif archive_format == "tar.gz":
            backup_filepath = os.path.join(backup_dest_dir, f"{backup_filename_base}.tar.gz")
            try:
                with tarfile.open(backup_filepath, "w:gz") as tar:
                    # The arcname parameter sets the name of the top-level directory in the archive
                    tar.add(source_path, arcname=base_name)
                print(f"Successfully backed up directory '{source_path}' to '{backup_filepath}'")
            except Exception as e:
                print(f"Error creating tar.gz archive for '{source_path}': {e}")
        else:
            print(f"Error: Unsupported archive format '{archive_format}'. Use 'zip' or 'tar.gz'.")
    else:
        print(f"Error: Source path '{source_path}' is neither a file nor a directory.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create a backup of a specified file or directory.",
        epilog="Example: python createBackup.py /path/to/file.txt --destination /my/backups --format zip"
    )
    parser.add_argument("source_path", help="The source file or directory to back up.")
    parser.add_argument(
        "--destination",
        help="Optional: The directory where the backup should be stored. "
             "Defaults to a 'backups' subfolder in the source's parent directory, "
             "or ~/.backups if that's not accessible."
    )
    parser.add_argument(
        "--format",
        choices=["zip", "tar.gz"],
        default="zip",
        help="Optional: The archive format for directory backups. Default: 'zip'."
    )

    args = parser.parse_args()

    create_backup(args.source_path, args.destination, args.format)
