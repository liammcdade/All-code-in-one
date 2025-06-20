#!/usr/bin/env python3

import json
import csv
import argparse
import os


def convert_json_to_csv(input_filepath, output_filepath, delimiter=","):
    """
    Reads a JSON file (expected to be an array of objects) and converts
    its content to a CSV file.
    """
    try:
        print(f"Attempting to read JSON file: '{input_filepath}'")
        with open(input_filepath, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        print(f"Error: Input JSON file '{input_filepath}' not found.")
        return False
    except json.JSONDecodeError as e:
        print(
            f"Error decoding JSON from '{input_filepath}': {e.msg} (Line: {e.lineno}, Column: {e.colno})."
        )
        return False
    except IOError as e:
        print(f"Error reading input JSON file '{input_filepath}': {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while reading '{input_filepath}': {e}")
        return False

    if not isinstance(data, list):
        print("Error: JSON data is not an array (list). Expected an array of objects.")
        return False

    if not data:
        print(
            "Warning: JSON array is empty. Output CSV will only contain headers (if any derivable) or be empty."
        )
        # Create an empty CSV or one with headers if possible (e.g. if a schema was provided)
        # For now, if data is empty, we can't infer headers.
        try:
            with open(output_filepath, "w", newline="", encoding="utf-8") as csv_file:
                # No headers, no data. Just an empty file.
                pass
            print(
                f"Created an empty CSV file: '{output_filepath}' as JSON array was empty."
            )
            return True
        except IOError as e:
            print(f"Error writing empty CSV file '{output_filepath}': {e}")
            return False

    # Determine headers: union of all keys from all objects to handle variations
    # Using dict.fromkeys to get unique keys while preserving order of first appearance (Python 3.7+)
    # For older Python, collections.OrderedDict.fromkeys or a list and set combo would be needed for ordered headers.
    headers = []
    all_keys = set()  # To quickly check if a key was added to headers
    for item in data:
        if not isinstance(item, dict):
            print(
                f"Warning: Item '{item}' in JSON array is not an object (dictionary). Skipping this item."
            )
            continue
        for key in item.keys():
            if key not in all_keys:
                headers.append(key)
                all_keys.add(key)

    if not headers:
        print(
            "Error: Could not determine any headers from the JSON objects (e.g., all objects were empty or not dictionaries)."
        )
        # Similar to empty data, create an empty CSV.
        try:
            with open(output_filepath, "w", newline="", encoding="utf-8") as csv_file:
                pass
            print(
                f"Created an empty CSV file: '{output_filepath}' as no headers could be derived."
            )
            return True
        except IOError as e:
            print(f"Error writing empty CSV file '{output_filepath}': {e}")
            return False

    try:
        print(
            f"Attempting to write CSV data to: '{output_filepath}' with delimiter '{delimiter}'"
        )
        with open(output_filepath, mode="w", newline="", encoding="utf-8") as csv_file:
            # Using csv.DictWriter to handle rows as dictionaries
            # `extrasaction='ignore'` is the default, meaning keys in a dict not in fieldnames are ignored.
            # `restval=''` means if a dict is missing a key from fieldnames, an empty string is written.
            writer = csv.DictWriter(
                csv_file, fieldnames=headers, delimiter=delimiter, restval=""
            )

            writer.writeheader()  # Write the header row

            for item in data:
                if isinstance(item, dict):  # Process only if it's a dictionary
                    writer.writerow(item)

        print(f"Successfully converted '{input_filepath}' to '{output_filepath}'.")
        return True

    except IOError as e:
        print(f"Error writing output CSV file '{output_filepath}': {e}")
        return False
    except Exception as e:  # Catch other potential errors during CSV writing
        print(f"An unexpected error occurred during CSV writing: {e}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert a JSON file (array of objects) to a CSV file.",
        epilog='Example: python jsonToCsv.py input.json output.csv --delimiter ";"',
    )
    parser.add_argument("input_json_file", help="Path to the input JSON file.")
    parser.add_argument("output_csv_file", help="Path for the output CSV file.")
    parser.add_argument(
        "--delimiter",
        default=",",
        help="Delimiter to use in the output CSV file. Default is comma.",
    )

    args = parser.parse_args()

    delimiter_to_use = args.delimiter
    if delimiter_to_use == "\\t":  # For tab from command line
        delimiter_to_use = "\t"

    print(f"Input JSON: {args.input_json_file}")
    print(f"Output CSV: {args.output_csv_file}")
    print(
        f"Using delimiter for CSV: '{delimiter_to_use}' (raw arg: '{args.delimiter}')"
    )

    success = convert_json_to_csv(
        args.input_json_file, args.output_csv_file, delimiter_to_use
    )

    if success:
        print("Conversion process completed successfully.")
    else:
        print("Conversion process failed.")
