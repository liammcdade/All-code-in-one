"""
Cleans up temporary files from a specified directory and its subdirectories.

Usage:
    python cleanup_temp_files.py <directory_path> [--delete]

Arguments:
    directory_path: The path to the directory to scan for temporary files.
    --delete: Optional flag. If provided, the script will delete found
              temporary files after confirmation.

Temporary file extensions/patterns checked:
    .tmp, .bak, .swp, .log, files ending with ~
"""

import argparse
import os

# Define common temporary file extensions and suffixes
TEMP_PATTERNS = ['.tmp', '.bak', '.swp', '.log', '~']

def find_temp_files(directory_path):
    """Finds temporary files in the given directory based on TEMP_PATTERNS."""
    temp_files_found = []
    for dirpath, _, filenames in os.walk(directory_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            # Check by extension or if filename ends with ~
            if os.path.isfile(filepath) and \
               (any(filename.lower().endswith(ext) for ext in TEMP_PATTERNS if ext != '~') or \
                filename.endswith('~')):
                temp_files_found.append(filepath)
    return temp_files_found

def main():
    parser = argparse.ArgumentParser(description="Cleans up temporary files from a directory.")
    parser.add_argument("directory_path", help="The directory to scan for temporary files.")
    parser.add_argument("--delete", action="store_true", help="Delete found temporary files.")

    args = parser.parse_args()

    if not os.path.isdir(args.directory_path):
        print(f"Error: Directory not found at {args.directory_path}")
        return

    print(f"Scanning for temporary files in: {args.directory_path}")
    print(f"Using patterns: {', '.join(TEMP_PATTERNS)}\n")

    try:
        temp_files = find_temp_files(args.directory_path)
    except Exception as e:
        print(f"Error during scanning: {e}")
        return

    if not temp_files:
        print("No temporary files found.")
        return

    print("Temporary files found:")
    for f_path in temp_files:
        print(f"  - {f_path}")

    if args.delete:
        print("\n-- Delete Mode --")
        try:
            confirm = input(f"Are you sure you want to delete {len(temp_files)} temporary file(s)? (yes/no): ").lower()
            if confirm == 'yes':
                deleted_count = 0
                error_count = 0
                for f_path in temp_files:
                    try:
                        os.remove(f_path)
                        print(f"Deleted: {f_path}")
                        deleted_count += 1
                    except OSError as e:
                        print(f"Error deleting {f_path}: {e}")
                        error_count += 1
                print(f"\nSuccessfully deleted {deleted_count} file(s).")
                if error_count > 0:
                    print(f"Failed to delete {error_count} file(s) due to errors.")
            else:
                print("Deletion cancelled by user.")
        except Exception as e:
            print(f"An error occurred during the deletion process: {e}")
    else:
        print("\nTo delete these files, run the script again with the --delete flag.")

if __name__ == "__main__":
    main()
