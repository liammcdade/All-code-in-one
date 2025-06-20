#!/usr/bin/env python3

import os
import json
import argparse


def validate_json_file(filepath):
    """
    Validates a single JSON file.
    Returns True if valid, False otherwise, along with a message.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Attempt to parse the JSON content
        json.loads(content)
        return True, f"'{filepath}': Valid JSON."

    except FileNotFoundError:
        return False, f"'{filepath}': Error - File not found."
    except IOError as e:
        return False, f"'{filepath}': Error reading file - {e}."
    except json.JSONDecodeError as e:
        error_message = (
            f"'{filepath}': Invalid JSON - {e.msg} "
            f"(Line: {e.lineno}, Column: {e.colno})."
        )
        return False, error_message
    except Exception as e:
        # Catch any other unexpected errors during the process for this file
        return False, f"'{filepath}': An unexpected error occurred - {e}."


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Validate one or more JSON files.",
        epilog="Example: python jsonValidator.py config.json data.json",
    )
    parser.add_argument(
        "filepaths", nargs="+", help="One or more paths to JSON files to validate."
    )

    args = parser.parse_args()

    print(f"Starting JSON validation for {len(args.filepaths)} file(s)...\n")

    valid_count = 0
    total_files = len(args.filepaths)

    for filepath_arg in args.filepaths:
        is_valid, message = validate_json_file(filepath_arg)
        print(message)
        if is_valid:
            valid_count += 1

    if total_files > 1:
        print(
            f"\nValidation summary: {valid_count} out of {total_files} file(s) are valid JSON."
        )
    elif total_files == 1 and valid_count == 1:
        pass  # Single file, already printed "Valid JSON."
    elif total_files == 1 and valid_count == 0:
        pass  # Single file, error message already printed.

    print("\nJSON validation process complete.")
