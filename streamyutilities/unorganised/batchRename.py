#!/usr/bin/env python3

import os
import argparse


def batch_rename_files(
    directory, search_pattern, replace_pattern, extension=None, dry_run=False
):
    """
    Renames files in a directory based on search and replace patterns.
    """
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' not found.")
        return

    rename_operations = []  # List to store (original_path, new_path) tuples

    for filename in os.listdir(directory):
        original_filepath = os.path.join(directory, filename)

        if not os.path.isfile(original_filepath):
            continue  # Skip directories or other non-file entries

        # Filter by extension if provided
        if extension:
            if not filename.endswith(extension):
                continue

        # Check if search pattern is in the filename
        if search_pattern in filename:
            new_filename = filename.replace(search_pattern, replace_pattern)
            new_filepath = os.path.join(directory, new_filename)

            # Avoid renaming to an existing filename (simple check)
            if new_filepath == original_filepath:
                continue  # No actual change

            rename_operations.append((original_filepath, new_filepath))

    if not rename_operations:
        print("No files found matching the criteria or no renames needed.")
        return

    print("\nProposed renames:")
    for old, new in rename_operations:
        print(f"  '{os.path.basename(old)}'  ->  '{os.path.basename(new)}'")

    if dry_run:
        print("\nDry run complete. No files were changed.")
        return

    # Confirmation step
    # Ensure input is handled correctly in various environments
    try:
        confirm = input("\nProceed with these renames? (yes/no): ").strip().lower()
    except EOFError:  # Handle cases where stdin is not available (e.g. piped input)
        print("\nConfirmation input not available. Aborting.")
        confirm = "no"

    if confirm == "yes":
        renamed_count = 0
        skipped_because_exists = []
        for old_path, new_path in rename_operations:
            if os.path.exists(new_path):
                print(
                    f"Skipping rename of '{os.path.basename(old_path)}' to '{os.path.basename(new_path)}' as target already exists."
                )
                skipped_because_exists.append(
                    (os.path.basename(old_path), os.path.basename(new_path))
                )
                continue
            try:
                os.rename(old_path, new_path)
                renamed_count += 1
            except OSError as e:
                print(f"Error renaming '{os.path.basename(old_path)}': {e}")

        print(f"\nSuccessfully renamed {renamed_count} file(s).")
        if skipped_because_exists:
            print("\nSkipped renames due to target file already existing:")
            for old, new in skipped_because_exists:
                print(f"  '{old}'  ->  '{new}'")
    else:
        print("\nRenaming aborted by user.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Batch rename files in a directory.",
        epilog='Example: python batchRename.py /path/to/pics "IMG_" "Vacation2024_" --extension .jpg',
    )
    parser.add_argument("directory", help="The directory containing files to rename.")
    parser.add_argument("search_pattern", help="The text to find in filenames.")
    parser.add_argument(
        "replace_pattern", help="The text to replace the search pattern with."
    )
    parser.add_argument(
        "--extension",
        help="Optional: Process only files with this extension (e.g., '.txt').",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what renames would occur without actually performing them.",
    )

    args = parser.parse_args()

    batch_rename_files(
        args.directory,
        args.search_pattern,
        args.replace_pattern,
        args.extension,
        args.dry_run,
    )
