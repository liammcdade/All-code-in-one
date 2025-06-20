#!/usr/bin/env python3

import os
import argparse


def list_files_by_type(directory, extension):
    """
    Lists all files within the given directory (and its subdirectories)
    that match the specified file extension.
    """
    matched_files = []
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' not found.")
        return matched_files

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                matched_files.append(os.path.join(root, file))

    return matched_files


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="List files by type in a directory.",
        epilog="Example: python listFilesByType.py /path/to/directory .py",
    )
    parser.add_argument("directory", help="The directory to search in.")
    parser.add_argument(
        "extension", help="The file extension to filter by (e.g., '.txt')."
    )

    args = parser.parse_args()

    found_files = list_files_by_type(args.directory, args.extension)

    if found_files:
        print("Found matching files:")
        for f_path in found_files:
            print(f_path)
    else:
        # Check if directory exists to differentiate between no files found and bad directory
        if os.path.isdir(args.directory):
            print(
                f"No files found with extension '{args.extension}' in directory '{args.directory}'."
            )
