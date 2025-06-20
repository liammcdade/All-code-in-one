#!/usr/bin/env python3

import os
import argparse


def get_human_readable_size(size_bytes):
    """Converts size in bytes to a human-readable string (KB, MB, GB)."""
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = 0
    while size_bytes >= 1024 and i < len(size_name) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.2f}{size_name[i]}"


def get_dir_tree_size(path):
    """Calculates the total size of all files in a directory tree."""
    total_size = 0
    try:
        for dirpath, _, filenames in os.walk(path):
            for f_name in filenames:
                fp = os.path.join(dirpath, f_name)
                if not os.path.islink(fp):  # Exclude symlinks from size calculation
                    try:
                        total_size += os.path.getsize(fp)
                    except OSError:
                        # File might be inaccessible or gone during walk
                        print(f"Warning: Could not get size of '{fp}'. Skipping.")
                        pass
    except OSError as e:
        print(
            f"Warning: Could not walk directory '{path}': {e}. Skipping its size contribution here."
        )
    return total_size


def list_directory_sizes(base_dir, depth, sort_by, sort_order_asc):
    """
    Lists sizes of subdirectories at a specific depth or total size if depth is 0.
    """
    if not os.path.isdir(base_dir):
        print(f"Error: Directory '{base_dir}' not found or is not a directory.")
        return None, 0

    results = {}  # {path: size_in_bytes}

    if depth == 0:
        total_size_of_base_dir = get_dir_tree_size(base_dir)
        results[base_dir] = total_size_of_base_dir
        # The overall total is just this size for depth 0
        return results, total_size_of_base_dir

    # For depth > 0, we are interested in subdirectories at that specific depth
    # The "total size" reported at the end should be the total size of the base_dir.
    overall_total_size = get_dir_tree_size(base_dir)

    # Normalize base_dir to count path separators correctly
    # Use absolute paths for consistent depth calculation
    abs_base_dir = os.path.abspath(base_dir)
    base_depth_count = abs_base_dir.count(os.path.sep)

    for dirpath, dirnames, _ in os.walk(base_dir, topdown=True):
        abs_curr_dirpath = os.path.abspath(dirpath)  # Current dirpath in absolute form
        current_level = abs_curr_dirpath.count(os.path.sep) - base_depth_count

        # We want to list directories AT 'depth'. So, we need to find their parents at 'depth-1'.
        if current_level == depth - 1:
            for d_name in dirnames:
                # Construct the full path for the target directory
                # dirpath is relative to base_dir if base_dir was relative, or absolute if base_dir was absolute
                # os.path.join correctly handles this.
                target_dir_path = os.path.join(dirpath, d_name)
                results[target_dir_path] = get_dir_tree_size(target_dir_path)
            # After processing dirnames at this level, we don't need to go deeper from here
            # for the purpose of finding *target depth directories*.
            # So, clear dirnames to prevent os.walk from visiting them further for *this specific path*.
            dirnames[:] = []
        elif current_level >= depth:
            # If we are already deeper than or at target_depth, stop further recursion from this path
            dirnames[:] = []

    # Sort results
    if sort_by == "name":
        sorted_results = sorted(
            results.items(), key=lambda item: item[0], reverse=not sort_order_asc
        )
    else:  # Default sort by size
        sorted_results = sorted(
            results.items(), key=lambda item: item[1], reverse=not sort_order_asc
        )

    return sorted_results, overall_total_size


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Display sizes of subdirectories within a specified directory.",
        epilog="Example: python dirSize.py /my/folder --depth 2 --sort-by name",
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="The directory to scan (defaults to current directory).",
    )
    parser.add_argument(
        "--depth",
        type=int,
        default=1,
        help="Depth for scanning subdirectories (e.g., 1 for immediate children, 0 for total size of current dir). Default: 1.",
    )
    parser.add_argument(
        "--sort-by",
        choices=["size", "name"],
        default="size",
        help="Sort output by size or by name. Default: size.",
    )
    parser.add_argument(
        "--sort-order",
        choices=["asc", "desc"],
        help="Sort order: 'asc' (ascending) or 'desc' (descending). "
        "Defaults to 'desc' for --sort-by size, and 'asc' for --sort-by name.",
    )

    args = parser.parse_args()

    # Determine default sort order if not specified
    if args.sort_order is None:
        sort_asc = True if args.sort_by == "name" else False
    else:
        sort_asc = args.sort_order == "asc"

    if args.depth < 0:
        print("Error: Depth cannot be negative.")
        exit(1)

    print(
        f"Scanning directory: '{os.path.abspath(args.directory)}' at depth {args.depth}"
    )

    sorted_items, total_dir_size = list_directory_sizes(
        args.directory, args.depth, args.sort_by, sort_asc
    )

    if sorted_items is not None:
        if not sorted_items and args.depth > 0:
            print(f"No subdirectories found at depth {args.depth}.")
        elif (
            not sorted_items
            and args.depth == 0
            and args.directory not in dict(sorted_items)
        ):
            # This case should be handled by the "Error: Directory not found" or if it's empty
            print(f"Directory '{args.directory}' might be empty or inaccessible.")
        else:
            for item_path, size_bytes in sorted_items:
                relative_path = os.path.relpath(
                    item_path,
                    (
                        os.path.abspath(args.directory)
                        if args.directory != "."
                        else os.getcwd()
                    ),
                )
                if args.depth == 0:  # For depth 0, the item_path is the base_dir itself
                    relative_path = os.path.basename(os.path.abspath(item_path))

                print(f"  {get_human_readable_size(size_bytes):<10} {relative_path}")

        print("--------------------")
        print(
            f"Total size of '{os.path.abspath(args.directory)}': {get_human_readable_size(total_dir_size)}"
        )
