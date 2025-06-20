#!/usr/bin/env python3

import os
import argparse
import hashlib
from collections import defaultdict


def calculate_md5(filepath, chunk_size=8192):
    """Calculates the MD5 hash of a file."""
    try:
        with open(filepath, "rb") as f:
            return hashlib.md5(
                b"".join(chunk for chunk in iter(lambda: f.read(chunk_size), b""))
            ).hexdigest()
    except IOError:
        # Could log this error if needed
        return None


def find_duplicate_files(directory):
    """
    Finds duplicate files in the given directory and its subdirectories.
    Files are first grouped by size, then by MD5 hash.
    """
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' not found.")
        return []

    files_by_size = defaultdict(list)
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            if os.path.isfile(filepath) and not os.path.islink(
                filepath
            ):  # Ignore symlinks
                try:
                    size = os.path.getsize(filepath)
                    files_by_size[size].append(filepath)
                except OSError:
                    # File might be inaccessible or gone, skip
                    continue

    duplicates_found = []
    for size, files in files_by_size.items():
        if len(files) < 2:
            continue  # No potential duplicates for this size

        hashes_by_file = defaultdict(list)
        for filepath in files:
            md5_hash = calculate_md5(filepath)
            if md5_hash:
                hashes_by_file[md5_hash].append(filepath)

        for md5_hash, filepaths in hashes_by_file.items():
            if len(filepaths) > 1:
                duplicates_found.append(filepaths)

    return duplicates_found


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Find duplicate files in a directory and its subdirectories.",
        epilog="Example: python findDuplicates.py /path/to/your/directory",
    )
    parser.add_argument("directory", help="The directory to scan for duplicate files.")

    args = parser.parse_args()

    duplicate_groups = find_duplicate_files(args.directory)

    if duplicate_groups:
        print("Found duplicate files:")
        for group_num, group in enumerate(duplicate_groups, 1):
            print(f"\n--- Group {group_num} ---")
            for filepath in group:
                print(filepath)
    else:
        if os.path.isdir(args.directory):  # Check if directory was valid
            print(f"No duplicate files found in '{args.directory}'.")
