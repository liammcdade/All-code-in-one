"""
Searches for a pattern (text string or regular expression) in files.
Similar to a basic grep utility.

Usage:
    python search_in_files.py <pattern> <path_or_file1> [<path_or_file2>...] [options]

Arguments:
    pattern:            The text string or regular expression to search for.
    path_or_file:       One or more directory paths or file paths to search within.
                        If a directory is provided, it will be searched recursively.

Options:
    -i, --ignore-case:   Perform case-insensitive matching.
    -E, --regex:         Treat the pattern as a regular expression.
                         By default, the pattern is treated as a plain string.
    -n, --line-number:   Prefix each line of output with the 1-based line number
                         within its input file.
    -l, --files-with-matches:
                         Only print the names of files containing selected lines.
                         Do not print matching lines.
    -v, --invert-match:  Invert the sense of matching, to select non-matching lines.
    --skip-binary:       Attempt to skip binary files. Default is to try and read them.

Examples:
    Search for "error" in all .log files in the current directory and subdirectories:
    python search_in_files.py "error" . --include "*.log" (Note: --include not implemented yet, manual globbing or find would be needed for this specific example, or search all and filter by eye)
    For now, to search .log files, you might list them:
    python search_in_files.py "error" app.log server.log

    Search for "my_function" case-insensitively in a specific directory:
    python search_in_files.py "my_function" ./my_project -i

    List files containing "TODO" using regex for "TODO:" or "TODO[ ]":
    python search_in_files.py "TODO[: ]" ./src -E -l
"""

import argparse
import os
import re

# Simple binary detection (can be improved)
def is_likely_binary_file(filepath, block_size=512):
    """
    Tries to guess if a file is binary by checking for null bytes in the first block.
    This is a heuristic and might not be 100% accurate.
    """
    try:
        with open(filepath, 'rb') as f:
            block = f.read(block_size)
        if b'\0' in block:
            return True
    except IOError: # File couldn't be opened, might be special file
        return True # Treat as binary to be safe
    return False

def search_in_file(filepath, pattern, is_regex, ignore_case, line_numbers, files_with_matches, invert_match, skip_binary):
    """
    Searches for the pattern in a single file.
    Yields results or returns True if a match is found and files_with_matches is True.
    """
    if skip_binary and is_likely_binary_file(filepath):
        # print(f"Skipping binary file: {filepath}")
        return False # Indicate no match found / skipped

    try:
        # Try to open with UTF-8, then fallback to latin-1 which is less likely to error on decode
        # but might not render all characters correctly for all file types.
        encodings_to_try = ['utf-8', 'latin-1']
        file_content_lines = None

        for encoding in encodings_to_try:
            try:
                with open(filepath, 'r', encoding=encoding) as f:
                    file_content_lines = f.readlines()
                break # Successfully read
            except UnicodeDecodeError:
                continue # Try next encoding

        if file_content_lines is None: # If all encodings failed
            if not files_with_matches: # Only print error if not just listing files
                 print(f"Warning: Could not decode file {filepath} with tried encodings. Skipping.")
            return False


        flags = 0
        if ignore_case:
            flags |= re.IGNORECASE

        # Compile regex pattern once
        try:
            pattern_re = re.escape(pattern) if not is_regex else pattern
            compiled_pattern = re.compile(pattern_re, flags)
        except re.error as e:
            print(f"Error: Invalid regular expression '{pattern}': {e}")
            return False # Propagate error indicator

        file_matched = False
        for i, line in enumerate(file_content_lines):
            line = line.rstrip('\n\r') # Remove EOL characters for cleaner output

            match = bool(compiled_pattern.search(line))

            if invert_match:
                match = not match

            if match:
                if files_with_matches:
                    return True # Signal that file contains a match

                file_matched = True # For non -l mode, to track if file had any matches
                output = ""
                if filepath: # Prepend filename
                    output += f"{filepath}:"
                if line_numbers:
                    output += f"{i+1}:"
                output += line
                print(output)

        return file_matched # True if any line matched (for non -l mode), False otherwise

    except IOError as e:
        if not files_with_matches:
            print(f"Warning: Could not read file {filepath}: {e}")
        return False # Indicate no match / error
    except Exception as e:
        if not files_with_matches:
            print(f"An unexpected error occurred while processing {filepath}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Searches for a pattern in files, similar to grep.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("pattern", help="The text string or regular expression to search for.")
    parser.add_argument(
        "paths",
        nargs='+',
        help="One or more directory paths or file paths to search within. "
             "Directories are searched recursively."
    )
    parser.add_argument(
        "-i", "--ignore-case",
        action="store_true",
        help="Perform case-insensitive matching."
    )
    parser.add_argument(
        "-E", "--regex",
        action="store_true",
        help="Treat the pattern as a POSIX extended regular expression. "
             "By default, pattern is a plain string."
    )
    parser.add_argument(
        "-n", "--line-number",
        action="store_true",
        help="Prefix each line of output with the 1-based line number."
    )
    parser.add_argument(
        "-l", "--files-with-matches",
        action="store_true",
        help="Only print the names of files containing selected lines."
    )
    parser.add_argument(
        "-v", "--invert-match",
        action="store_true",
        help="Invert the sense of matching, to select non-matching lines."
    )
    parser.add_argument(
        "--skip-binary",
        action="store_true",
        help="Attempt to heuristically skip binary files. Default is to try reading them."
    )

    args = parser.parse_args()

    files_to_search = []
    for path_arg in args.paths:
        if os.path.isfile(path_arg):
            files_to_search.append(path_arg)
        elif os.path.isdir(path_arg):
            for dirpath, _, filenames in os.walk(path_arg):
                for filename in filenames:
                    files_to_search.append(os.path.join(dirpath, filename))
        else:
            print(f"Warning: Path '{path_arg}' is not a valid file or directory. Skipping.")

    if not files_to_search:
        print("No files found to search.")
        return

    # Pre-compile pattern if it's regex to catch errors early
    if args.regex:
        try:
            re.compile(args.pattern, re.IGNORECASE if args.ignore_case else 0)
        except re.error as e:
            print(f"Error: Invalid regular expression '{args.pattern}': {e}")
            return

    overall_match_found = False # To know if anything was printed, for exit status ideas

    for filepath in files_to_search:
        file_had_match = search_in_file(
            filepath,
            args.pattern,
            args.regex,
            args.ignore_case,
            args.line_number,
            args.files_with_matches,
            args.invert_match,
            args.skip_binary
        )
        if file_had_match:
            overall_match_found = True
            if args.files_with_matches:
                print(filepath) # Print filename if it matched and -l is on

    # Consider an exit code strategy if desired, e.g., 0 if match found, 1 if not.
    # For now, just rely on output.

if __name__ == "__main__":
    main()
