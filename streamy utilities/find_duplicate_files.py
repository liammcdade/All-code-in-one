"""
Finds and optionally deletes duplicate files in a directory.

Usage:
    python find_duplicate_files.py <directory_path> [--delete]

Arguments:
    directory_path: The path to the directory to scan for duplicate files.
    --delete: Optional flag. If provided, the script will prompt the user
              to delete duplicate files.
"""

import argparse
import hashlib
import os

def calculate_hash(filepath, block_size=65536):
    """Calculates the SHA256 hash of a file."""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        buf = f.read(block_size)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(block_size)
    return hasher.hexdigest()

def find_duplicates(directory_path):
    """Finds duplicate files in the given directory."""
    hashes = {}
    duplicates = {}

    for dirpath, _, filenames in os.walk(directory_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.isfile(filepath):
                file_hash = calculate_hash(filepath)
                if file_hash in hashes:
                    if file_hash not in duplicates:
                        duplicates[file_hash] = [hashes[file_hash]]
                    duplicates[file_hash].append(filepath)
                else:
                    hashes[file_hash] = filepath
    return duplicates

def main():
    parser = argparse.ArgumentParser(description="Finds and optionally deletes duplicate files.")
    parser.add_argument("directory_path", help="The directory to scan.")
    parser.add_argument("--delete", action="store_true", help="Prompt to delete duplicates.")

    args = parser.parse_args()

    if not os.path.isdir(args.directory_path):
        print(f"Error: Directory not found at {args.directory_path}")
        return

    duplicate_files = find_duplicates(args.directory_path)

    if not duplicate_files:
        print("No duplicate files found.")
        return

    print("\nDuplicate files found:")
    for file_hash, files in duplicate_files.items():
        print(f"\nHash: {file_hash}")
        for f in files:
            print(f"  - {f}")

    if args.delete:
        print("\n-- Delete Mode --")
        for file_hash, files in duplicate_files.items():
            print(f"\nDuplicate set (Hash: {file_hash}):")
            for idx, f_path in enumerate(files):
                print(f"  {idx + 1}. {f_path}")

            while True:
                try:
                    # Prompt user to select files to keep
                    keep_indices_str = input("Enter numbers of files to KEEP (comma-separated, e.g., 1,2), or 'none' to delete all, or 'skip' to keep all: ")

                    if keep_indices_str.lower() == 'skip':
                        print(f"Skipping deletion for this set.")
                        break

                    files_to_delete = list(files) # Assume all are to be deleted initially

                    if keep_indices_str.lower() != 'none':
                        keep_indices = [int(i.strip()) -1 for i in keep_indices_str.split(',')]

                        # Validate input indices
                        if not all(0 <= idx < len(files) for idx in keep_indices):
                            print("Invalid selection. Please enter valid numbers.")
                            continue

                        # Determine files to delete
                        files_to_keep_paths = [files[i] for i in keep_indices]
                        files_to_delete = [f for f in files if f not in files_to_keep_paths]


                    if not files_to_delete:
                        print("No files selected for deletion in this set.")
                        break

                    print("\nFiles to be DELETED:")
                    for f_del in files_to_delete:
                        print(f"  - {f_del}")

                    confirm = input("Confirm deletion? (yes/no): ").lower()
                    if confirm == 'yes':
                        for f_del in files_to_delete:
                            try:
                                os.remove(f_del)
                                print(f"Deleted: {f_del}")
                            except OSError as e:
                                print(f"Error deleting {f_del}: {e}")
                        break
                    elif confirm == 'no':
                        print("Deletion cancelled for this set.")
                        break
                    else:
                        print("Invalid input. Please type 'yes' or 'no'.")

                except ValueError:
                    print("Invalid input. Please enter numbers separated by commas, 'none', or 'skip'.")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
