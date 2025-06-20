#!/usr/bin/env python3

import os
import shutil
import argparse
import json
from collections import defaultdict

DEFAULT_MAPPINGS = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp"],
    "Documents": [
        ".pdf",
        ".docx",
        ".doc",
        ".txt",
        ".odt",
        ".rtf",
        ".csv",
        ".xls",
        ".xlsx",
        ".ppt",
        ".pptx",
    ],
    "Archives": [".zip", ".tar", ".gz", ".rar", ".7z"],
    "Music": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm"],
    "Scripts": [".py", ".sh", ".js", ".pl", ".rb"],
    "Executables": [".exe", ".msi", ".dmg", ".deb", ".rpm"],
}


def load_mappings(custom_mapping_file):
    import json

    return (
        {**DEFAULT_MAPPINGS, **json.load(open(custom_mapping_file))}
        if custom_mapping_file
        else DEFAULT_MAPPINGS.copy()
    )


def organize_downloads(
    downloads_dir, custom_mapping_file, unknown_action="other", dry_run=False
):
    if not os.path.isdir(downloads_dir):
        print(f"Error: Downloads directory '{downloads_dir}' not found.")
        return

    ext_to_category_map = load_mappings(custom_mapping_file)

    proposed_moves = []  # List of (src_path, dest_path, category_folder_name)
    folders_to_create = set()

    for filename in os.listdir(downloads_dir):
        src_path = os.path.join(downloads_dir, filename)
        if not os.path.isfile(src_path):  # Only process files
            continue

        _, file_extension = os.path.splitext(filename)
        file_extension = file_extension.lower()

        category_folder_name = ext_to_category_map.get(file_extension)

        if not category_folder_name:
            if unknown_action == "leave":
                continue  # Leave the file as is
            else:  # Default is "other"
                category_folder_name = "Other"

        dest_folder_path = os.path.join(downloads_dir, category_folder_name)
        dest_path = os.path.join(dest_folder_path, filename)

        if (
            src_path == dest_path
        ):  # Already in the correct place (e.g. in "Other" and unknown)
            continue

        proposed_moves.append((src_path, dest_path, category_folder_name))
        if not os.path.exists(dest_folder_path):
            folders_to_create.add(
                category_folder_name
            )  # Store just name, relative to downloads_dir

    if not proposed_moves:
        print("No files to organize or all files are already organized.")
        return

    print("\nProposed actions:")
    if folders_to_create:
        print("  Folders to be created:")
        for folder_name in sorted(list(folders_to_create)):
            print(f"    - {os.path.join(downloads_dir, folder_name)}")

    print("  Files to be moved:")
    for src, dest, _ in proposed_moves:
        print(
            f"    - Move '{os.path.basename(src)}' to '{os.path.relpath(dest, downloads_dir)}'"
        )

    if dry_run:
        print("\nDry run complete. No files were moved or folders created.")
        return

    try:
        confirm = input("\nProceed with these actions? (yes/no): ").strip().lower()
    except EOFError:
        print("\nConfirmation input not available. Aborting.")
        confirm = "no"

    if confirm == "yes":
        moved_count = 0
        # Create folders first
        for folder_name in sorted(list(folders_to_create)):
            full_folder_path = os.path.join(downloads_dir, folder_name)
            try:
                os.makedirs(full_folder_path, exist_ok=True)
                print(f"Created folder: '{full_folder_path}'")
            except OSError as e:
                print(f"Error creating folder '{full_folder_path}': {e}")
                # Potentially abort if critical folder creation fails, or try to continue

        # Move files
        for src_path, dest_path, _ in proposed_moves:
            try:
                # Ensure destination directory exists (it should have been created)
                dest_dir = os.path.dirname(dest_path)
                if not os.path.exists(dest_dir):
                    # This case should ideally be caught by folder creation logic
                    print(
                        f"Warning: Destination directory '{dest_dir}' for '{os.path.basename(src_path)}' does not exist. Skipping."
                    )
                    continue

                if os.path.exists(dest_path):
                    print(
                        f"Warning: File '{dest_path}' already exists. Skipping '{os.path.basename(src_path)}'."
                    )
                    continue

                shutil.move(src_path, dest_path)
                moved_count += 1
            except Exception as e:
                print(
                    f"Error moving '{os.path.basename(src_path)}' to '{dest_path}': {e}"
                )

        print(f"\nSuccessfully moved {moved_count} file(s).")
    else:
        print("\nOrganization aborted by user.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Organize files in a directory into category subfolders based on extension.",
        epilog="Example: python organizeDownloads.py /path/to/Downloads --custom-mapping mapping.json",
    )
    parser.add_argument(
        "downloads_dir", help="The directory whose files need to be organized."
    )
    parser.add_argument(
        "--custom-mapping",
        help="Optional: Path to a JSON file with custom extension mappings "
        '(e.g., {"Videos": [".mkv", ".mp4"]}). These merge with/override defaults.',
    )
    parser.add_argument(
        "--unknown-action",
        choices=["other", "leave"],
        default="other",
        help="Action for files with unknown extensions: 'other' (move to 'Other' folder) "
        "or 'leave' (leave them in place). Default: 'other'.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what actions would be taken without actually moving files or creating folders.",
    )

    args = parser.parse_args()

    organize_downloads(
        args.downloads_dir, args.custom_mapping, args.unknown_action, args.dry_run
    )
