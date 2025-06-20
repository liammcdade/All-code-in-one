"""
Analyzes and displays the sizes of subdirectories within a given directory.

Usage:
    python analyze_directory_sizes.py [directory_path] [--depth D] [--top N]

Arguments:
    directory_path:   Optional. Path to the directory to analyze.
                      Defaults to the current working directory.
Options:
    --depth D, -d D:  Maximum depth of subdirectories to scan.
                      A depth of 0 means only files in the root of directory_path.
                      A depth of 1 means files in root + immediate subdirectories.
                      Defaults to full recursion (e.g., a large number like 999).
    --top N, -t N:    Display only the top N largest subdirectories.
                      If not specified, all scanned subdirectories are shown.
"""

import argparse
import os

def bytes_to_human_readable(n_bytes):
    return next((f"{n_bytes / (1 << (i + 1) * 10):.2f} {s}B" for i, s in reversed(list(enumerate(('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')))) if n_bytes >= 1 << (i + 1) * 10), f"{n_bytes} B")

def get_directory_sizes(root_dir, max_depth):
    """
    Calculates the total size of each subdirectory up to max_depth.
    Returns a dictionary: {path: size_in_bytes}
    """
    dir_sizes = {}
    root_dir = os.path.abspath(root_dir)
    initial_depth = root_dir.count(os.sep)

    for current_dirpath, dirnames, filenames in os.walk(root_dir, topdown=True):
        current_depth = current_dirpath.count(os.sep) - initial_depth

        if current_depth > max_depth:
            # Stop recursing into this branch by clearing dirnames
            dirnames[:] = []
            continue

        dir_size = 0
        # Size of files directly in current_dirpath
        for filename in filenames:
            filepath = os.path.join(current_dirpath, filename)
            try:
                if not os.path.islink(filepath): # Avoid double counting symlinks if they point within tree
                    dir_size += os.path.getsize(filepath)
            except OSError as e:
                print(f"Warning: Could not access file {filepath}: {e}")

        # Add this size to current_dirpath and all its parents up to root_dir
        # This is a bit tricky because os.walk gives children sizes later.
        # A simpler approach for this script's goal (sizes of *subdirectories* of root_dir)
        # is to calculate size for each directory seen and store it.
        # We are interested in the size of 'current_dirpath' itself.

        # To get total size of 'current_dirpath' including its children:
        # we need to sum sizes from deeper levels first.
        # The current loop structure is top-down.
        # Let's rethink: calculate total size for each directory encountered.

    # Alternative: Post-order traversal or summing up after full walk
    # For simplicity, let's stick to calculating total size for each visited dir
    # then sum up for parent directories if needed, or focus on what this script needs:
    # "total size of each subdirectory *within* it (the root_dir)"
    # This means we want sizes of root_dir/subdir1, root_dir/subdir2, etc.

    # Let's use a dictionary to store sizes and accumulate from bottom up.
    path_sizes = {} # Stores total size of all files within this path and its children

    for current_dirpath, _, filenames in os.walk(root_dir, topdown=False): # topdown=False for bottom-up
        current_depth = current_dirpath.count(os.sep) - initial_depth
        if current_depth > max_depth: # Should not be strictly necessary with topdown=False if handled right
            continue

        current_total_size = 0
        # Add size of files directly in this directory
        for filename in filenames:
            filepath = os.path.join(current_dirpath, filename)
            try:
                if not os.path.islink(filepath):
                    current_total_size += os.path.getsize(filepath)
            except OSError as e:
                print(f"Warning: Could not access file {filepath}: {e}")

        # Add sizes of direct children directories already processed (due to topdown=False)
        for dirname in dirnames:  # Use dirnames from os.walk, which contains only directories
            child_dir_path = os.path.join(current_dirpath, dirname)
            if child_dir_path in path_sizes:
                # Ensure it's a direct child and its size has been computed
                if child_dir_path.count(os.sep) == current_dirpath.count(os.sep) + 1:
                    current_total_size += path_sizes[child_dir_path]

        path_sizes[current_dirpath] = current_total_size

    # Now, filter for the subdirectories of the *original* root_dir at depth 1 relative to it.
    # Or, if depth is 0, just the files in root_dir.
    # The request is "total size of each subdirectory *within* it"
    # If depth=0, it's files in root. If depth=1, it's root/subdirA, root/subdirB.

    # The path_sizes dictionary now contains the total size for *every* directory scanned.
    # We need to extract the ones that are direct children of root_dir, or deeper based on requested depth.
    # The current `max_depth` in `os.walk` limits how deep `path_sizes` goes.

    # If we want to show sizes of subdirectories at a certain depth relative to root_dir:
    # For depth 0: total size of files in root_dir (not its subdirs)
    # For depth 1: total size of root_dir/subdirA, root_dir/subdirB (incl their content)

    # Let's refine dir_sizes to be specifically what the user wants to see:
    # A list of (directory_name, total_size) for directories at the requested conceptual depth.

    # The current path_sizes has full tree sizes.
    # If user asks for --depth 1, they want to see sizes of root/d1, root/d2, etc.
    # where size of root/d1 includes everything under root/d1.

    # So, path_sizes is actually what we need. We just need to filter it.
    # We are interested in directories that are `max_depth` levels down from `root_dir`.
    # Or, if we list all subdirs, then `max_depth` limits how far their own sizes are aggregated.

    # Let's redefine: the script shows sizes of immediate children of `root_dir`.
    # The `max_depth` will control how deep the calculation for *those children's* sizes goes.
    # No, the prompt implies `max_depth` is about *which* subdirectories are listed.
    # "limit the depth of subdirectory scanning (e.g., --depth 1 to only show sizes of immediate children)"

    # So, if root is /A, and --depth 1, we show /A/B, /A/C.
    # If root is /A, and --depth 0, we show /A (total size).
    # If root is /A, and --depth 2, we show /A/B, /A/C, /A/B/D, /A/B/E, /A/C/F.

    # The `path_sizes` from bottom-up walk is correct. Now filter what to display.
    display_sizes = {}
    for path, size in path_sizes.items():
        # Only consider paths that are at the specified depth relative to root_dir
        # or shallower, if we want to display a tree-like structure up to depth.
        # "Display a list of subdirectories and their total sizes"
        # This usually means immediate subdirectories, or those up to a certain depth.

        path_depth_from_root = path.count(os.sep) - initial_depth

        # We want to list directories that are themselves subdirectories of root_dir,
        # and their depth should not exceed `max_depth`.
        if path_depth_from_root <= max_depth and path_depth_from_root >= 0 : # >=0 for root itself
            if path == root_dir and max_depth < 0 : # Special case: if depth is -1 (or 0 in prompt), show root only.
                                                # Let's say depth 0 means root dir itself.
                pass # handled later

            # We want to display each directory at the specified depth, or if max_depth is large, all of them.
            # The key in display_sizes should probably be relative to root_dir for clarity.
            relative_path = os.path.relpath(path, start=os.path.dirname(root_dir)) # Gives "root_dir/subdir" or "root_dir"
            if path == root_dir :
                 relative_path = os.path.basename(root_dir) + " (root itself)"


            # We only want to show directories that are *exactly* at `max_depth` if `max_depth` is restrictive?
            # Or all dirs *up to* `max_depth`? "limit the depth of subdirectory scanning"
            # "display a list of subdirectories" -> implies multiple.
            # Let's assume it means show all directories found up to that 'max_depth'.
            display_sizes[relative_path] = size

    # If depth 0 was requested, it means only files in the root.
    # The current path_sizes[root_dir] contains total size of root_dir and all children.
    # This needs to be clearer.
    # Let's redefine:
    #   - `max_depth` controls how deep `os.walk` goes to calculate sizes.
    #   - The output should be a list of immediate subdirectories of `root_dir` and their *total* sizes calculated up to `max_depth`.
    # This seems more standard for a "du -sh *" like behavior.

    # So, we need total size of root_dir/subdir1, root_dir/subdir2.
    # path_sizes has this. We just need to select root_dir/subdir1, root_dir/subdir2.

    final_display_data = {}
    # Add total size of files directly in root_dir, if depth allows (e.g. depth 0 or more)
    if max_depth >= 0:
        files_in_root_size = 0
        root_dir_listing = os.listdir(root_dir)
        for item in root_dir_listing:
            item_path = os.path.join(root_dir, item)
            if os.path.isfile(item_path) and not os.path.islink(item_path):
                try:
                    files_in_root_size += os.path.getsize(item_path)
                except OSError as e:
                    print(f"Warning: Could not access file {item_path}: {e}")
        if files_in_root_size > 0:
            final_display_data[os.path.join(os.path.basename(root_dir), "[Files_In_Root]")] = files_in_root_size


    # Add sizes of immediate subdirectories of root_dir
    # Their sizes in `path_sizes` are comprehensive (sum of all their children)
    # The `max_depth` for `os.walk` should be effectively infinite if we want full sizes of immediate children.
    # The `max_depth` argument for the script should be about *which* directories to list.

    # Let's simplify the definition of --depth for the user:
    # --depth 0: Show total size of root_dir itself.
    # --depth 1: Show total size of root_dir, and then immediate children of root_dir.
    # --depth N: Show all directories up to N levels from root_dir.

    # The `path_sizes` dictionary is good. It contains {abs_path: total_recursive_size}.
    # We just need to select which entries from `path_sizes` to display based on user's `max_depth` choice.

    output_data = {}
    for path, size in path_sizes.items():
        # Calculate depth of 'path' relative to 'root_dir'
        # To do this, compare common path. root_dir must be prefix of path.
        if not path.startswith(root_dir): continue # Should not happen if os.walk is on root_dir

        path_rel_to_root = os.path.relpath(path, root_dir)
        depth = path_rel_to_root.count(os.sep) if path_rel_to_root != '.' else 0

        if depth <= max_depth:
            display_name = os.path.join(os.path.basename(root_dir), path_rel_to_root) if path_rel_to_root != '.' else os.path.basename(root_dir)
            output_data[display_name] = size

    return output_data


def main():
    parser = argparse.ArgumentParser(
        description="Analyzes and displays sizes of subdirectories.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "directory_path",
        nargs='?',
        default=os.getcwd(),
        help="Path to the directory to analyze. Defaults to current directory."
    )
    parser.add_argument(
        "--depth", "-d",
        type=int,
        default=0, # Defaulting to depth 0 (immediate children and files in root)
                   # Let's clarify: depth 0 = root, depth 1 = root + immediate children, etc.
                   # The prompt: "--depth 1 to only show sizes of immediate children"
                   # This implies depth 0 would be files in root_dir.
                   # Let's make --depth 0 mean content of target dir (files + total for each subdir)
                   # and --depth 1 mean content of target dir's children (files + total for each grandchild)
                   # This is like `du -d <depth>`. So depth 0 is common.
        help="Maximum depth of subdirectories to show. "
             "Depth 0: Show total size of items (files/dirs) directly in directory_path. "
             "Depth 1: Also show items in immediate subdirectories, etc. "
             "Default: 0."
    )
    parser.add_argument(
        "--top", "-t",
        type=int,
        default=None,
        help="Display only the top N largest subdirectories/files. Shows all by default."
    )

    args = parser.parse_args()

    if not os.path.isdir(args.directory_path):
        print(f"Error: Directory '{args.directory_path}' not found or is not a directory.")
        return

    if args.depth < 0:
        print("Error: Depth must be a non-negative integer.")
        return

    print(f"Analyzing directory: {os.path.abspath(args.directory_path)}")
    print(f"Listing items up to depth: {args.depth}\n")

    try:
        # The get_directory_sizes needs to be aligned with the --depth definition.
        # If depth is 0, we want to see sizes of items *within* directory_path.
        # These items are files and immediate subdirectories.
        # The size of an immediate subdirectory should be its *total* recursive size.

        # So, os.walk should always go full depth to calculate total sizes.
        # The `max_depth` argument in `get_directory_sizes` should reflect the display depth.

        # Let's refine `get_directory_sizes` for `du -d <depth>` behavior.
        # It should return sizes of all items up to `args.depth` from the target directory.

        # path_sizes will store {absolute_path: total_size_of_that_path_recursively}
        path_sizes = {}
        abs_root_dir = os.path.abspath(args.directory_path)

        for current_dirpath, dirnames, filenames in os.walk(abs_root_dir, topdown=False, onerror=lambda e: print(f"Warning: Cannot access {e.filename}: {e.strerror}")):
            dir_total_size = 0
            # Add size of files directly in this directory
            for filename in filenames:
                filepath = os.path.join(current_dirpath, filename)
                try:
                    if not os.path.islink(filepath):
                        dir_total_size += os.path.getsize(filepath)
                except OSError as e:
                    print(f"Warning: Could not get size of file {filepath}: {e}")

            # Add sizes of direct children directories (already processed due to topdown=False)
            for dirname in dirnames: # dirnames are from current_dirpath
                child_dir_abs_path = os.path.join(current_dirpath, dirname)
                if child_dir_abs_path in path_sizes:
                    dir_total_size += path_sizes[child_dir_abs_path]

            path_sizes[current_dirpath] = dir_total_size

        # Now filter what to display based on args.depth
        # We want to list items (files and dirs) that are at `args.depth` levels
        # *below* abs_root_dir.
        # Or, more like `du`, items *within* abs_root_dir, then items *within* its children if depth > 0.

        results_to_display = {} # {display_name: size}
        root_basename = os.path.basename(abs_root_dir)

        # Add files directly in abs_root_dir
        for item_name in os.listdir(abs_root_dir):
            item_abs_path = os.path.join(abs_root_dir, item_name)
            if os.path.isfile(item_abs_path):
                try:
                    if not os.path.islink(item_abs_path):
                         results_to_display[os.path.join(root_basename, item_name)] = os.path.getsize(item_abs_path)
                except OSError as e:
                    print(f"Warning: Could not get size of file {item_abs_path}: {e}")
            elif os.path.isdir(item_abs_path):
                # This is a subdirectory. Its total size is in path_sizes.
                results_to_display[os.path.join(root_basename, item_name)] = path_sizes.get(item_abs_path, 0)

        # If depth > 0, we need to go deeper.
        # The current `results_to_display` is effectively for depth 0.
        # This is getting complicated. Let's use the `du -d <depth>` model more strictly.
        # `du -d 0 path` shows total for `path`.
        # `du -d 1 path` shows total for `path`, and for `path/child1`, `path/child2`.
        # This is not what the prompt "depth 1 to only show sizes of immediate children" implies.
        # Prompt implies: depth 0 = files in root, depth 1 = immediate subdirs.

        # Back to: `path_sizes` has recursive sizes of ALL dirs.
        # We need to select which ones to show.
        # If depth D, show dirs that are D levels below `directory_path`.

        display_items = {} # {relative_path_to_show: size}
        initial_depth_count = abs_root_dir.count(os.sep)

        # Add files in the root directory if depth is 0
        if args.depth == 0:
            for item_name in os.listdir(abs_root_dir):
                item_abs_path = os.path.join(abs_root_dir, item_name)
                if os.path.isfile(item_abs_path):
                    try:
                        if not os.path.islink(item_abs_path):
                            display_items[item_name] = os.path.getsize(item_abs_path)
                    except OSError as e:
                        print(f"Warning: File access error {item_abs_path}: {e}")


        # Add directories at the specified depth
        for path, size in path_sizes.items():
            if path.startswith(abs_root_dir):
                # path_depth = number of components in path relative to abs_root_dir
                relative_path = os.path.relpath(path, abs_root_dir)
                if relative_path == ".": # The root directory itself
                    current_path_script_depth = 0
                else:
                    current_path_script_depth = relative_path.count(os.sep) + 1

                if current_path_script_depth == args.depth: # Only show items at this exact depth
                    # For depth 0, this means the root dir itself.
                    # For depth 1, this means immediate children of root.
                    if relative_path == ".": # Special case for root itself if depth is 0
                        display_items[os.path.basename(abs_root_dir) + " (Total)"] = size
                    else:
                        display_items[relative_path] = size

        # Sort by size
        sorted_items = sorted(display_items.items(), key=lambda item: item[1], reverse=True)

        if not sorted_items:
            print("No subdirectories or files found at the specified depth to display, or error in size calculation.")
            return

        print(f"\nSizes for items at depth {args.depth} relative to {abs_root_dir}:")

        items_to_show = sorted_items
        if args.top is not None and args.top > 0:
            items_to_show = sorted_items[:args.top]
            if not items_to_show and sorted_items : # If top N is 0 but there are items
                 print(f"(Top {args.top} requested, but no items to show or N is too small)")

        if not items_to_show and sorted_items: # If top was applied and resulted in empty list
             print(f"(Top {args.top} filter resulted in no items to display from {len(sorted_items)} total at this depth)")


        for name, size_in_bytes in items_to_show:
            print(f"  {bytes_to_human_readable(size_in_bytes):>10}  {name}")

        if args.top is not None and args.top > 0 and len(sorted_items) > args.top:
            print(f"\n(Showing top {args.top} of {len(sorted_items)} items at this depth)")


    except (OSError, ValueError) as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
