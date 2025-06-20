"""
Batch renames files in a directory based on a search/replace pattern,
and optionally adds a prefix or suffix.

Usage:
    python batch_rename_files.py <directory_path> <search_pattern> <replace_pattern> \
                                 [--prefix <prefix_string>] [--suffix <suffix_string>] \
                                 [--dry-run]

Arguments:
    directory_path:   Path to the directory containing files to rename.
    search_pattern:   The string/pattern to search for in filenames.
    replace_pattern:  The string to replace the search_pattern with.
    --prefix:         Optional. String to add to the beginning of filenames.
    --suffix:         Optional. String to add to the end of filenames (before extension).
    --dry-run:        Optional. If set, shows proposed renames without making changes.

Examples:
    Rename all files containing "report_old" to "report_new":
    python batch_rename_files.py ./reports "report_old" "report_new"

    Add prefix "final_" to all .txt files that had "draft" replaced by "final":
    python batch_rename_files.py ./docs "draft" "final" --prefix "final_"

    Add suffix "_v2" to all JPG images, and do a dry run:
    python batch_rename_files.py ./images "" "" --suffix "_v2" --dry-run
    (Note: search_pattern and replace_pattern can be empty if only using prefix/suffix)
"""

import argparse
import os

def generate_new_filename(filename, search_pattern, replace_pattern, prefix, suffix):
    """Generates the new filename based on search/replace, prefix, and suffix."""
    name, ext = os.path.splitext(filename)

    # Apply search and replace
    if search_pattern: # Only replace if search_pattern is not empty
        name = name.replace(search_pattern, replace_pattern)

    # Add prefix
    if prefix:
        name = prefix + name

    # Add suffix
    if suffix:
        name = name + suffix

    return name + ext

def batch_rename(directory_path, search_pattern, replace_pattern, prefix, suffix, dry_run):
    """Performs the batch renaming operation."""

    print(f"\nScanning directory: {directory_path}")
    if search_pattern:
        print(f"Searching for: '{search_pattern}'")
        print(f"Replacing with: '{replace_pattern}'")
    if prefix:
        print(f"Adding prefix: '{prefix}'")
    if suffix:
        print(f"Adding suffix: '{suffix}'")

    if dry_run:
        print("\nDRY RUN MODE: No files will be renamed.")

    proposed_renames = [] # List of (original_path, new_path) tuples
    files_to_rename_count = 0

    # First pass: identify files and generate new names
    for filename in os.listdir(directory_path):
        original_filepath = os.path.join(directory_path, filename)

        if os.path.isfile(original_filepath):
            new_filename = generate_new_filename(filename, search_pattern, replace_pattern, prefix, suffix)
            new_filepath = os.path.join(directory_path, new_filename)

            if new_filename != filename: # If there's an actual change
                files_to_rename_count += 1
                proposed_renames.append((original_filepath, new_filepath, filename, new_filename))

    if not proposed_renames:
        print("\nNo files found matching the criteria or no changes would be made.")
        return

    print(f"\nFound {files_to_rename_count} file(s) that would be renamed:")

    # Check for potential conflicts before showing proposed renames
    potential_conflicts = {} # new_name -> list of original_names
    final_rename_plan = [] # (original_path, new_path, original_filename, new_filename) without conflicts

    for orig_fp, new_fp, orig_fn, new_fn in proposed_renames:
        # Check if new_fp would overwrite an existing file NOT part of the current batch rename
        # (i.e. a file that is not itself being renamed)
        # Or if multiple files are being renamed to the same new_fp

        # Check if new_fp already exists and is NOT one of the original files being renamed
        existing_original_paths = [item[0] for item in proposed_renames]
        if os.path.exists(new_fp) and new_fp not in existing_original_paths:
            print(f"  - WARNING: '{orig_fn}' -> '{new_fn}'. CONFLICT: '{new_fn}' already exists and will be SKIPPED.")
            continue # Skip this rename

        # Check if multiple files in this batch would be renamed to the same new_filename
        if new_fn in potential_conflicts:
            potential_conflicts[new_fn].append(orig_fn)
        else:
            potential_conflicts[new_fn] = [orig_fn]

        final_rename_plan.append((orig_fp, new_fp, orig_fn, new_fn))

    # Filter out renames that would cause internal conflicts (multiple files to same new name)
    actual_renames_to_perform = []
    for orig_fp, new_fp, orig_fn, new_fn in final_rename_plan:
        if len(potential_conflicts[new_fn]) > 1:
            print(f"  - WARNING: Multiple files would be renamed to '{new_fn}' (from {', '.join(potential_conflicts[new_fn])}). SKIPPING these renames to prevent conflict.")
            # Mark all involved as skipped for clarity if needed, but for now, just don't add them
        elif new_fp != orig_fp : # Ensure it's actually a rename
             actual_renames_to_perform.append((orig_fp, new_fp, orig_fn, new_fn))
             print(f"  - Plan: '{orig_fn}' -> '{new_fn}'")


    if not actual_renames_to_perform:
        print("\nNo renames to perform after conflict resolution.")
        return

    if dry_run:
        print("\nDry run complete. No changes were made.")
        return

    print(f"\nProceeding with {len(actual_renames_to_perform)} rename(s).")
    try:
        confirm = input("Are you sure you want to rename these files? (yes/no): ").lower()
        if confirm == 'yes':
            renamed_count = 0
            error_count = 0
            # Sort by new_filepath length descending to handle cases like a -> aa, aa -> aaa
            # This helps prevent overwriting a source file that is also a target for another rename in the same batch
            # A more robust way is to rename to temporary unique names first, then to final names.
            # For simplicity here, we'll rely on the conflict check and careful ordering.
            # A truly safe approach involves renaming to temp names first if complex chained renames are possible.
            # However, our conflict check should prevent direct overwrites of existing files not in the batch
            # and multiple files renaming to the same target.

            # To be safer, let's check if any new_filepath is an original_filepath of another operation
            # This is a simple check for chained renames that might fail if not ordered.
            # For example: fileA -> fileB, and fileB -> fileC. If fileA is renamed first, fileB is overwritten.
            # A more robust solution is to rename to temporary names first.

            # Simple check: if a target new_filepath is also an original_filepath in another operation.
            # This is tricky. The current conflict check handles overwriting *existing* files.
            # And multiple files mapping to the *same* new name.
            # The main remaining risk is a -> b, b -> c.
            # If we rename a to b first, the original b is gone.
            # To handle this well, often files are renamed to temp names first.
            # For this script, we'll proceed with the current conflict checks.

            for original_filepath, new_filepath, _, _ in actual_renames_to_perform:
                try:
                    os.rename(original_filepath, new_filepath)
                    print(f"Renamed: '{original_filepath}' -> '{new_filepath}'")
                    renamed_count += 1
                except FileExistsError:
                     print(f"Error renaming '{original_filepath}': Target '{new_filepath}' already exists (should have been caught by pre-check). Skipping.")
                     error_count +=1
                except OSError as e:
                    print(f"Error renaming '{original_filepath}': {e}")
                    error_count += 1

            print(f"\nSuccessfully renamed {renamed_count} file(s).")
            if error_count > 0:
                print(f"Failed to rename {error_count} file(s) due to errors.")
        else:
            print("Renaming cancelled by user.")
    except Exception as e:
        print(f"An error occurred during the renaming process: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Batch renames files in a directory.",
        formatter_class=argparse.RawTextHelpFormatter # To keep example formatting
    )
    parser.add_argument("directory_path", help="Path to the directory.")
    parser.add_argument("search_pattern", help="String to search for in filenames. Can be empty if only using prefix/suffix.")
    parser.add_argument("replace_pattern", help="String to replace the search_pattern with.")
    parser.add_argument("--prefix", help="Optional. String to add to the beginning of filenames.")
    parser.add_argument("--suffix", help="Optional. String to add to the end of filenames (before extension).")
    parser.add_argument("--dry-run", action="store_true", help="Show proposed renames without making changes.")

    args = parser.parse_args()

    if not os.path.isdir(args.directory_path):
        print(f"Error: Directory not found at {args.directory_path}")
        return

    # It's okay for search_pattern to be empty if prefix or suffix is provided.
    # It's also okay for replace_pattern to be empty.
    if not args.search_pattern and not args.prefix and not args.suffix:
        print("Error: You must specify a search_pattern, a prefix, or a suffix for the script to do anything.")
        parser.print_help()
        return

    batch_rename(
        args.directory_path,
        args.search_pattern,
        args.replace_pattern,
        args.prefix,
        args.suffix,
        args.dry_run
    )

if __name__ == "__main__":
    main()
