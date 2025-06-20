#!/usr/bin/env python3

import os
import argparse
import re

# Common single-line comment starters
# For simplicity, does not handle cases like string literals containing comment markers
SINGLE_LINE_COMMENT_PATTERNS = {
    ".py": re.compile(r"^\s*#"),
    ".sh": re.compile(r"^\s*#"),
    ".js": re.compile(r"^\s*//"),
    ".c": re.compile(r"^\s*//"),
    ".cpp": re.compile(r"^\s*//"),
    ".java": re.compile(r"^\s*//"),
    ".go": re.compile(r"^\s*//"),
    ".rs": re.compile(r"^\s*//"),
    ".rb": re.compile(r"^\s*#"),
    ".pl": re.compile(r"^\s*#"),
    ".php": re.compile(r"^\s*(#|//)"),  # PHP uses # and //
}
# Basic block comment patterns (start and end)
# This is a simplified handling and won't be perfect for all edge cases
BLOCK_COMMENT_PATTERNS = {
    ".c": (re.compile(r"^\s*/\*"), re.compile(r"\*/\s*$")),
    ".cpp": (re.compile(r"^\s*/\*"), re.compile(r"\*/\s*$")),
    ".java": (re.compile(r"^\s*/\*"), re.compile(r"\*/\s*$")),
    ".js": (re.compile(r"^\s*/\*"), re.compile(r"\*/\s*$")),
    ".php": (re.compile(r"^\s*/\*"), re.compile(r"\*/\s*$")),
    # Add more as needed
}


def get_file_extension(filepath):
    return os.path.splitext(filepath)[1].lower()


def count_lines_in_file(filepath, ignore_comments, ignore_blank_lines):
    """
    Counts total lines, non-empty lines, and lines of code (LoC) in a single file.
    LoC is heuristically determined.
    """
    stats = {"total": 0, "non_empty": 0, "loc": 0, "file": filepath}
    file_ext = get_file_extension(filepath)

    single_line_comment_re = SINGLE_LINE_COMMENT_PATTERNS.get(file_ext)
    block_comment_start_re, block_comment_end_re = BLOCK_COMMENT_PATTERNS.get(
        file_ext, (None, None)
    )

    in_block_comment = False

    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for line_content in f:
                stats["total"] += 1
                stripped_line = line_content.strip()

                if not stripped_line:  # It's a blank line
                    if not ignore_blank_lines:
                        # Non-empty count doesn't care about ignore_blank_lines flag
                        # LoC count does care
                        pass  # It's blank, don't count as non_empty or LoC if ignoring
                    # else: continue to count it as non-empty if not ignoring blanks for LoC
                else:
                    stats["non_empty"] += 1

                # LoC counting logic
                current_line_is_loc = True

                if not stripped_line:  # Is a blank line
                    if ignore_blank_lines:
                        current_line_is_loc = False
                    # `non_empty` already handled: blank lines are not non-empty

                if (
                    current_line_is_loc and ignore_comments
                ):  # Only check for comments if it's not already disqualified
                    line_is_comment = False
                    # Test for block comments first
                    if block_comment_start_re and block_comment_end_re:
                        # Case 1: Already in a block comment
                        if in_block_comment:
                            if block_comment_end_re.search(
                                line_content
                            ):  # End of block comment?
                                # Check if anything non-whitespace exists AFTER '*/'
                                # For simplicity, if '*/' is on the line, we assume the useful part of the line ends with it or before it.
                                # A more complex check: line_content.split(block_comment_end_re.pattern)[-1].strip()
                                # For now, assume if */ is found, the "comment part" is dominant for this line.
                                line_is_comment = True  # The line ending the block is considered a comment line
                                in_block_comment = False
                            else:  # Still inside block comment, no end marker on this line
                                line_is_comment = True
                        # Case 2: Not in a block comment, check for start
                        elif block_comment_start_re.search(line_content):
                            # Check if anything non-whitespace exists BEFORE '/*'
                            # For simplicity, if '/*' is on the line, we assume the useful part starts after it or is consumed by it.
                            # A more complex check: line_content.split(block_comment_start_re.pattern)[0].strip()
                            line_is_comment = True  # The line starting the block is considered a comment line
                            in_block_comment = True
                            if block_comment_end_re.search(
                                line_content
                            ):  # Ends on the same line
                                in_block_comment = False
                                # line_is_comment remains true, as it's a '/* ... */' line

                    # Test for single-line comments if not already classified by block comments
                    # This means a line like `code(); // comment` is LoC, but `// comment` is not.
                    # And `code(); /* comment */` would be LoC, but `/* comment */` is not.
                    if not line_is_comment and single_line_comment_re:
                        # Check if the line *starts* with a single-line comment marker (ignoring leading whitespace)
                        if single_line_comment_re.match(stripped_line):
                            line_is_comment = True

                    if line_is_comment:
                        current_line_is_loc = False

                if current_line_is_loc:
                    stats["loc"] += 1

    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        return None
    except Exception as e:
        print(f"Error reading file '{filepath}': {e}")
        return None

    # If ignore_blank_lines is true, an empty file or file with only blank lines should have loc = 0.
    # If ignore_comments is true, a file with only comments (and maybe blank lines) should have loc = 0.
    # The current logic for non_empty is simply any line with non-whitespace characters.
    # The loc count is refined by the flags.

    return stats


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Count lines in files: total, non-empty, and lines of code (LoC).",
        epilog="Example: python countLines.py my_script.py --ignore-comments",
    )
    parser.add_argument(
        "filepaths", nargs="+", help="One or more file paths to analyze."
    )
    parser.add_argument(
        "--ignore-comments",
        action="store_true",
        help="Exclude comment lines from Lines of Code (LoC) count. Also affects non-empty if line is only comment.",
    )
    parser.add_argument(
        "--ignore-blank-lines",
        action="store_true",
        help="Exclude blank lines from Lines of Code (LoC) count.",
    )

    args = parser.parse_args()

    grand_totals = {"total": 0, "non_empty": 0, "loc": 0}
    num_files_processed = 0

    for filepath in args.filepaths:
        print(f"\nProcessing file: {filepath}")
        file_stats = count_lines_in_file(
            filepath, args.ignore_comments, args.ignore_blank_lines
        )

        if file_stats:
            num_files_processed += 1
            print(f"  Total lines: {file_stats['total']}")
            print(f"  Non-empty lines: {file_stats['non_empty']}")
            print(f"  Lines of Code (LoC): {file_stats['loc']}")
            grand_totals["total"] += file_stats["total"]
            grand_totals["non_empty"] += file_stats["non_empty"]
            grand_totals["loc"] += file_stats["loc"]
        else:
            print("  Skipped due to errors.")

    if num_files_processed > 1:
        print("\n-----------------------------------")
        print("Grand Totals for Processed Files:")
        print(f"  Total lines: {grand_totals['total']}")
        print(f"  Non-empty lines: {grand_totals['non_empty']}")
        print(f"  Lines of Code (LoC): {grand_totals['loc']}")
        print("-----------------------------------")

    if num_files_processed == 0 and args.filepaths:
        print("\nNo files were processed successfully.")
