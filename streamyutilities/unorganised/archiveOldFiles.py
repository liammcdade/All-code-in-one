#!/usr/bin/env python3

import os
import shutil
import argparse
from datetime import datetime, timedelta

def get_archive_destination_path(source_dir, custom_dest_dir=None):
    """Determines the final archive destination path."""
    timestamp_str = datetime.now().strftime("%Y%m%d")
    archive_subfolder_name = f"archive_{timestamp_str}"

    if custom_dest_dir:
        # User provided a specific destination directory
        return os.path.join(custom_dest_dir, archive_subfolder_name)
    else:
        # Default to 'archive_[YYYYMMDD]' within the source directory's parent, or source itself
        # For simplicity, let's try to create it within the source directory itself.
        # A more complex logic might place it in source_dir's parent or ~/Documents/ArchivedFiles

        proposed_dest = os.path.join(os.path.abspath(source_dir), archive_subfolder_name)
        # As a fallback, use user's Documents folder
        fallback_dest_base = os.path.join(os.path.expanduser("~"), "Documents", "ArchivedFiles")

        # Check if proposed_dest is reasonable. If source_dir is deep, this might be okay.
        # If source_dir is something like / (which is unlikely), this would be bad.
        # We'll assume source_dir is a typical user directory.
        try:
            # Attempt to create (or check writability for) the proposed_dest parent
            # For now, we'll just return it and let the move operation handle errors if not writable.
            # The actual directory will be created on demand.
            return proposed_dest
        except Exception: # Broad exception for cases like non-writable parent, etc.
            print(f"Warning: Default destination '{proposed_dest}' might not be usable.")
            final_fallback = os.path.join(fallback_dest_base, archive_subfolder_name)
            print(f"Using fallback archive destination: '{final_fallback}'")
            return final_fallback


def find_old_files(source_directory, days_old, recursive):
    """Finds files older than 'days_old' in the source directory."""
    old_files_map = {} # {source_abs_path: intended_dest_relative_to_archive_root}
    cutoff_time = datetime.now() - timedelta(days=days_old)
    abs_source_directory = os.path.abspath(source_directory)

    if not os.path.isdir(abs_source_directory):
        print(f"Error: Source directory '{abs_source_directory}' not found.")
        return None

    if recursive:
        for root, _, files in os.walk(abs_source_directory):
            # Avoid recursing into potential archive subdirectories we might create
            if "archive_" in os.path.basename(root) and os.path.dirname(root) == abs_source_directory: # simple check
                continue

            for filename in files:
                filepath = os.path.join(root, filename)
                try:
                    if os.path.isfile(filepath) and not os.path.islink(filepath):
                        file_mod_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                        if file_mod_time < cutoff_time:
                            # Relative path from source_directory to preserve structure
                            relative_path = os.path.relpath(filepath, abs_source_directory)
                            old_files_map[filepath] = relative_path
                except OSError as e:
                    print(f"Warning: Could not access or get info for '{filepath}': {e}")
    else: # Non-recursive
        for filename in os.listdir(abs_source_directory):
            filepath = os.path.join(abs_source_directory, filename)
            # Avoid archiving our own archive subdirectories if scan is run multiple times
            if os.path.isdir(filepath) and "archive_" in filename:
                 continue
            try:
                if os.path.isfile(filepath) and not os.path.islink(filepath):
                    file_mod_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                    if file_mod_time < cutoff_time:
                        # For non-recursive, relative path is just the filename
                        old_files_map[filepath] = filename
            except OSError as e:
                print(f"Warning: Could not access or get info for '{filepath}': {e}")

    return old_files_map


def archive_files(source_dir_path, days, dest_dir_path=None, recursive_scan=False, dry_run_mode=False):

    archive_root_dest = get_archive_destination_path(source_dir_path, dest_dir_path)

    print(f"Scanning for files older than {days} days in '{os.path.abspath(source_dir_path)}'.")
    if recursive_scan:
        print("Recursive scan enabled.")

    # Prevent archiving from within its own target archive directory if default location is used
    abs_source_dir = os.path.abspath(source_dir_path)
    if archive_root_dest.startswith(abs_source_dir) and abs_source_dir != os.path.dirname(archive_root_dest):
         # e.g. source is /foo, archive is /foo/archive_date. This is fine.
         # But if source is /foo/archive_date and archive is /foo/archive_date/archive_date2, bad.
         # A simple check: if archive_root_dest is inside abs_source_dir AND is not an immediate child like "archive_XYZ"
         # This is tricky. The find_old_files has a basic check.
         pass


    files_to_archive_map = find_old_files(abs_source_dir, days, recursive_scan)

    if files_to_archive_map is None: # Source directory not found
        return

    if not files_to_archive_map:
        print("No files found matching the age criteria.")
        return

    print(f"\nFound {len(files_to_archive_map)} file(s) to archive to '{archive_root_dest}':")
    for src_abs, dest_rel in files_to_archive_map.items():
        print(f"  - '{src_abs}'  ->  '{os.path.join(archive_root_dest, dest_rel)}'")

    if dry_run_mode:
        print("\nDry run complete. No files were moved.")
        return

    try:
        confirm = input("\nProceed with archiving these files? (yes/no): ").strip().lower()
    except EOFError:
        print("\nConfirmation input not available. Aborting.")
        confirm = "no"

    if confirm == 'yes':
        moved_count = 0
        print(f"\nArchiving files to '{archive_root_dest}'...")
        # Ensure the main archive root destination exists
        try:
            if not os.path.exists(archive_root_dest):
                 os.makedirs(archive_root_dest, exist_ok=True)
                 print(f"Created archive base directory: '{archive_root_dest}'")
        except OSError as e:
            print(f"Error: Could not create archive base directory '{archive_root_dest}': {e}. Aborting.")
            return

        for src_abs_path, dest_rel_path in files_to_archive_map.items():
            final_dest_path = os.path.join(archive_root_dest, dest_rel_path)
            final_dest_subdir = os.path.dirname(final_dest_path)

            try:
                if not os.path.exists(final_dest_subdir):
                    os.makedirs(final_dest_subdir, exist_ok=True)

                if os.path.exists(final_dest_path):
                    # Basic conflict handling: append timestamp to filename if target exists
                    name, ext = os.path.splitext(os.path.basename(final_dest_path))
                    conflict_suffix = datetime.now().strftime("_%H%M%S%f")
                    final_dest_path = os.path.join(final_dest_subdir, f"{name}{conflict_suffix}{ext}")
                    print(f"Warning: Target '{os.path.join(archive_root_dest, dest_rel_path)}' existed. Saving as '{final_dest_path}'.")

                shutil.move(src_abs_path, final_dest_path)
                moved_count += 1
            except Exception as e:
                print(f"Error moving '{src_abs_path}' to '{final_dest_path}': {e}")

        print(f"\nSuccessfully archived {moved_count} file(s).")
    else:
        print("\nArchiving aborted by user.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Archive old files from a source directory.",
        epilog="Example: python archiveOldFiles.py /docs --days 365 --dest /backups/docs_archive --recursive"
    )
    parser.add_argument("source_directory", help="The directory to scan for old files.")
    parser.add_argument("--days", type=int, required=True, help="Files older than this number of days will be archived.")
    parser.add_argument("--destination", help="Optional: Directory where archives will be stored. Defaults to 'archive_[YYYYMMDD]' in source_dir or ~/Documents/ArchivedFiles.")
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Scan recursively into subdirectories. Default: only top-level files."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List files that would be archived without actually moving them."
    )

    args = parser.parse_args()

    if args.days < 0:
        print("Error: Number of days must be non-negative.")
        exit(1)

    archive_files(
        args.source_directory,
        args.days,
        args.destination,
        args.recursive,
        args.dry_run
    )
