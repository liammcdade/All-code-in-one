#!/usr/bin/env python3

import os
import re
import argparse
import glob


def collect_files_from_targets(targets, recursive_flag):
    """
    Collects all unique file paths from the given targets.
    Targets can be files, directories, or glob patterns.
    """
    collected_filepaths = set()
    for target_pattern in targets:
        # Check if the pattern is a directory directly
        if os.path.isdir(target_pattern) and not glob.has_magic(target_pattern):
            if recursive_flag:
                for root, _, files in os.walk(target_pattern):
                    for filename in files:
                        collected_filepaths.add(os.path.join(root, filename))
            else:  # Non-recursive: only files directly in the directory
                for item in os.listdir(target_pattern):
                    item_path = os.path.join(target_pattern, item)
                    if os.path.isfile(item_path):
                        collected_filepaths.add(item_path)
        else:  # It's a file or a glob pattern
            # Use glob to find files. recursive=True needed for '**'
            # If the pattern itself doesn't have recursive glob chars, but --recursive is set,
            # glob won't descend into subdirs unless the pattern explicitly allows it (e.g. dir/* or dir/**)
            # This part might need refinement if we want --recursive to force glob to be more recursive.
            # For now, rely on glob's own recursive nature if ** is in pattern.
            # If recursive_flag is true and target_pattern is a simple dir/*.txt, glob won't go deeper.
            # This is complex. Let's simplify: glob handles patterns. If it's a dir, os.walk handles recursion.

            # Simplified glob handling:
            # If glob.has_magic, it's a pattern. Let glob handle it.
            # If not, it's a specific file or dir.
            if glob.has_magic(target_pattern):
                # If recursive_flag is true, we should enable it for glob if possible (e.g. for patterns like my_dir/**/*.txt)
                # However, glob's recursive kwarg is for the '**' pattern.
                # A simple glob.glob(target_pattern) might be enough if pattern is specific.
                # For `project_dir/*.py`, recursive won't apply with simple glob.
                # This needs to be smarter or documented clearly.
                # Let's assume glob handles its patterns, and os.walk handles explicit dirs with --recursive.

                # If target_pattern could be like 'some_dir' that isn't caught by os.path.isdir first
                # (e.g. due to permissions temporarily), glob might still list it if it matches.
                # This part is tricky. For now, we'll glob everything that's not an explicit dir.
                found_items = glob.glob(
                    target_pattern, recursive=recursive_flag
                )  # Enable if user wants recursion
                for item_path in found_items:
                    if os.path.isfile(item_path):
                        collected_filepaths.add(item_path)
                    # If recursive_flag and item_path is a directory from glob, need to walk it
                    elif os.path.isdir(item_path) and recursive_flag:
                        for root, _, files in os.walk(item_path):
                            for filename in files:
                                collected_filepaths.add(os.path.join(root, filename))

            elif os.path.isfile(target_pattern):  # Specific file
                collected_filepaths.add(target_pattern)
            # else: it was a dir without magic, handled by os.path.isdir block. Or invalid path.

    return list(collected_filepaths)


def search_replace_in_file(
    filepath, search_pattern, replacement_string, is_regex, dry_run, interactive_mode
):
    """
    Performs search and replace in a single file.
    Returns (num_replacements_made, file_content_changed_flag, error_occurred_flag).
    """
    try:
        # Attempt to read with UTF-8, then fallback with warning
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            print(
                f"Warning: Could not decode '{filepath}' as UTF-8. Trying with 'latin-1'."
            )
            with open(filepath, "r", encoding="latin-1") as f:  # Common fallback
                content = f.read()

        original_content = content
        num_replacements = 0

        if is_regex:
            try:
                new_content, num_replacements = re.subn(
                    search_pattern, replacement_string, content
                )
            except re.error as e:
                print(
                    f"Regex error for pattern '{search_pattern}' in '{filepath}': {e}. Skipping file."
                )
                return 0, False, True
        else:  # Plain string replacement
            num_replacements = content.count(search_pattern)
            if num_replacements > 0:
                new_content = content.replace(search_pattern, replacement_string)
            else:
                new_content = content

        if num_replacements == 0:
            return 0, False, False  # No changes needed

        print(
            f"\n--- Potential changes for '{filepath}' ({num_replacements} occurrence(s)) ---"
        )
        # For simplicity in dry-run/interactive, just show if changes would occur.
        # A more advanced version would show diffs.
        # print("Old content snippet / New content snippet here...")

        file_actually_changed = False
        if dry_run:
            print(f"  [Dry Run] Would replace {num_replacements} instance(s).")
            # To show what would change more clearly, one could compare lines:
            # old_lines = original_content.splitlines()
            # new_lines = new_content.splitlines()
            # for i, (old, new) in enumerate(zip(old_lines, new_lines)):
            # if old != new: print(f"Line {i+1}:\n  OLD: {old}\n  NEW: {new}")
            # This is too verbose for now.
            return (
                num_replacements,
                False,
                False,
            )  # Report potential changes, but file not actually changed

        if interactive_mode:
            # Per-file confirmation for now. Per-occurrence is more complex.
            user_confirm = (
                input(
                    f"Apply {num_replacements} change(s) to '{filepath}'? (yes/no/all_remaining): "
                )
                .strip()
                .lower()
            )
            if user_confirm == "yes":
                pass  # Proceed with this file
            elif user_confirm == "all_remaining":
                # This implies a global state to stop asking, not implemented here simply.
                # For now, treat 'all_remaining' as 'yes' for this file and continue asking for next.
                # Or, this could set a global flag to auto-confirm subsequent files.
                # Let's make it simpler: interactive is per file.
                print(
                    "Treating 'all_remaining' as 'yes' for this file. Future files will still ask if in interactive mode."
                )
                pass
            else:  # 'no' or anything else
                print(f"Skipped changes for '{filepath}'.")
                return 0, False, False  # User skipped

        # Write back the changes
        try:
            with open(
                filepath,
                "w",
                encoding="utf-8" if "UnicodeDecodeError" not in locals() else "latin-1",
            ) as f:
                f.write(new_content)
            file_actually_changed = True
            print(f"  Applied {num_replacements} replacement(s) to '{filepath}'.")
        except IOError as e:
            print(f"Error writing changes to '{filepath}': {e}")
            return num_replacements, False, True  # Had changes, but failed to write

        return num_replacements, file_actually_changed, False

    except FileNotFoundError:  # Should be caught by collect_files, but as safety
        print(f"Error: File '{filepath}' not found during processing.")
        return 0, False, True
    except Exception as e:
        print(f"An unexpected error occurred while processing '{filepath}': {e}")
        return 0, False, True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Search and replace text in files. Use with caution.",
        epilog='Example: python textSearchReplace.py "old" "new" ./*.txt --dry-run',
    )
    parser.add_argument(
        "search_pattern", help="The string or regex pattern to search for."
    )
    parser.add_argument(
        "replacement_string", help="The string to replace occurrences with."
    )
    parser.add_argument(
        "input_targets",
        nargs="+",
        help="One or more file paths, directory paths, or glob patterns (e.g., 'src/*.py', 'docs/').",
    )
    parser.add_argument(
        "--is-regex",
        action="store_true",
        help="Treat the search_pattern as a regular expression.",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="If an input target is a directory, search recursively within it. "
        "Note: Glob patterns like 'dir/**/*.txt' are inherently recursive.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what changes would be made without actually modifying files.",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Confirm each file before making replacements. (Currently per-file, not per-occurrence).",
    )

    args = parser.parse_args()

    print("Collecting files...")
    # Refined file collection based on --recursive for directories
    # Glob patterns handle their own recursion e.g. dir/**/file.txt
    # For explicit directory targets, --recursive controls os.walk

    # This file collection needs to be robust.
    # If target is dir, and --recursive, walk.
    # If target is dir, and no --recursive, listdir for files.
    # If target is glob, glob.glob.
    # The current collect_files_from_targets is a bit convoluted. Let's simplify.

    files_to_process = []
    for target in args.input_targets:
        if os.path.isdir(target):
            if args.recursive:
                for root, dirs, files_in_dir in os.walk(target):
                    for fname in files_in_dir:
                        files_to_process.append(os.path.join(root, fname))
            else:  # only files in top level of this directory
                for fname in os.listdir(target):
                    fpath = os.path.join(target, fname)
                    if os.path.isfile(fpath):
                        files_to_process.append(fpath)
        elif os.path.isfile(target):  # Explicit file
            files_to_process.append(target)
        else:  # Assume glob pattern
            # For glob, if user wants recursive on a pattern like `somedir/*`, they should use `somedir/**`
            # The recursive flag for glob.glob is specifically for `**`
            # So, we pass args.recursive to glob, it will only matter if `**` is in the pattern.
            expanded_glob = glob.glob(target, recursive=args.recursive)
            for g_item in expanded_glob:
                if os.path.isfile(g_item):
                    files_to_process.append(g_item)
                elif (
                    os.path.isdir(g_item) and args.recursive
                ):  # If glob matched a dir and we are recursive
                    for root, dirs, files_in_dir in os.walk(g_item):
                        for fname in files_in_dir:
                            files_to_process.append(os.path.join(root, fname))

    files_to_process = sorted(list(set(files_to_process)))  # Unique and sorted

    if not files_to_process:
        print("No files found to process based on input targets.")
        exit(0)

    print(f"Found {len(files_to_process)} file(s) to process.")
    if args.dry_run:
        print("Dry run mode enabled. No files will be changed.")

    total_files_modified = 0
    total_replacements_made_overall = 0
    total_files_with_potential_changes = 0  # For dry_run summary
    total_potential_replacements = 0  # For dry_run summary

    for filepath in files_to_process:
        # Pass the original args.interactive, not a global state for 'all_remaining' for now
        replacements_in_file, modified_this_file, error = search_replace_in_file(
            filepath,
            args.search_pattern,
            args.replacement_string,
            args.is_regex,
            args.dry_run,
            args.interactive,
        )
        if error:
            print(f"Skipping '{filepath}' due to error during processing.")
            continue

        if args.dry_run:
            if replacements_in_file > 0:
                total_files_with_potential_changes += 1
                total_potential_replacements += replacements_in_file
        else:  # Not dry_run
            if modified_this_file:  # This means file was successfully written to
                total_files_modified += 1
                # replacements_in_file counts actual changes if not dry_run and user confirmed
                total_replacements_made_overall += replacements_in_file

    print("\n--- Summary ---")
    if args.dry_run:
        print("Dry run mode. No files were actually changed.")
        print(f"Potential files to be modified: {total_files_with_potential_changes}")
        print(f"Potential total replacements: {total_potential_replacements}")
    else:
        print(f"Total files modified: {total_files_modified}")
        print(f"Total replacements made: {total_replacements_made_overall}")

    print("\nText search and replace process complete.")
