#!/usr/bin/env python3

import os
import argparse
from collections import Counter

def view_path_variable(check_duplicates=False, check_nondirs=False):
    """
    Retrieves, displays, and analyzes the system's PATH environment variable.
    """
    path_variable_str = os.getenv("PATH")

    if not path_variable_str:
        print("Error: PATH environment variable not found or is empty.")
        return

    # Split the PATH string by the OS-specific separator (e.g., ':' on Linux/macOS, ';' on Windows)
    original_paths = path_variable_str.split(os.pathsep)

    print("--- System PATH Entries ---")
    if not original_paths:
        print("(PATH is set but contains no entries after splitting)")
        return

    path_counts = None
    if check_duplicates:
        path_counts = Counter(original_paths)

    non_dir_paths_found = []

    for i, path_entry in enumerate(original_paths):
        if not path_entry: # Handle empty strings if PATH has consecutive separators like "::" or leading/trailing ":"
            status_marker = "[EMPTY STRING]"
            is_ok_dir = False
        elif os.path.exists(path_entry):
            if os.path.isdir(path_entry):
                status_marker = "[OK]"
                is_ok_dir = True
            else:
                status_marker = "[EXISTS - NOT A DIRECTORY]"
                is_ok_dir = False
                if check_nondirs: # Only add to list if we are actively checking for this
                    non_dir_paths_found.append(path_entry)
        else:
            status_marker = "[NOT FOUND]"
            is_ok_dir = False

        display_line = f"{i+1:3d}. {path_entry:<80} {status_marker}"

        # Add duplicate marker if applicable
        if check_duplicates and path_counts and path_counts[path_entry] > 1:
            display_line += f"  [DUPLICATE ({path_counts[path_entry]} times)]"

        # The check_nondirs highlighting is implicitly handled by "[EXISTS - NOT A DIRECTORY]"
        # but the flag `check_nondirs` ensures `non_dir_paths_found` is populated for a summary.

        print(display_line)

    # Summaries
    if check_duplicates:
        print("\n--- Duplicate Path Summary ---")
        duplicates_found_summary = False
        # Iterate through unique paths that were duplicated for a cleaner summary
        unique_duplicated_paths = {p: count for p, count in path_counts.items() if count > 1}
        if unique_duplicated_paths:
            duplicates_found_summary = True
            for path_val, count in sorted(unique_duplicated_paths.items()):
                print(f"  Path: '{path_val}' appears {count} times.")
        if not duplicates_found_summary:
            print("  No duplicate paths found in PATH.")

    if check_nondirs: # This summary relies on non_dir_paths_found being populated
        print("\n--- Non-Directory Path Summary ---")
        if non_dir_paths_found:
            print("  The following paths exist but are NOT directories:")
            # non_dir_paths_found might have duplicates if path itself was duplicated and also a non-dir.
            # Use set for unique summary.
            for path_val in sorted(list(set(non_dir_paths_found))):
                print(f"  - '{path_val}'")
        else:
            # This message also appears if all non-dirs were also not found (so not added to list)
            print("  No paths found that exist but are not directories (or all paths are valid directories or not found).")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="View and analyze the system's PATH environment variable.",
        epilog="Example: python pathViewer.py --check-duplicates --check-nondirs"
    )
    parser.add_argument(
        "--check-duplicates",
        action="store_true",
        help="Highlight and summarize duplicate paths in the PATH variable."
    )
    parser.add_argument(
        "--check-nondirs",
        action="store_true",
        help="Highlight and summarize paths in PATH that exist but are not directories."
    )

    args = parser.parse_args()

    view_path_variable(args.check_duplicates, args.check_nondirs)
    print("\nPATH analysis complete.")
