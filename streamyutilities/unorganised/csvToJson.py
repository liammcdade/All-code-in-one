#!/usr/bin/env python3

import csv
import json
import argparse
import os

def convert_csv_to_json(input_filepath, output_filepath, delimiter=','):
    """
    Reads a CSV file and converts its content to a JSON array of objects.
    Uses CSV headers as keys for the JSON objects.
    """
    data_list = []

    try:
        print(f"Attempting to read CSV file: '{input_filepath}' with delimiter '{delimiter}'")
        with open(input_filepath, mode='r', newline='', encoding='utf-8') as csv_file:
            # Using csv.DictReader to automatically use the first row as keys
            csv_reader = csv.DictReader(csv_file, delimiter=delimiter)

            # csv.DictReader might raise Error if delimiter is not found or other issues
            # We'll catch generic Exception for CSV parsing for now.
            # More specific error handling (e.g., csv.Error) can be added if needed.

            line_count = 0
            for row in csv_reader:
                data_list.append(row)
                line_count += 1

            if line_count == 0 and csv_reader.fieldnames is None:
                print(f"Warning: CSV file '{input_filepath}' might be empty or headers not found with delimiter '{delimiter}'.")
                # If headers are not found with the given delimiter, fieldnames will be None
                # or DictReader might consume the first line as data if it can't parse headers.
            elif not data_list:
                 print(f"Warning: CSV file '{input_filepath}' read successfully but contained no data rows after headers.")


    except FileNotFoundError:
        print(f"Error: Input CSV file '{input_filepath}' not found.")
        return False
    except IOError as e:
        print(f"Error reading input CSV file '{input_filepath}': {e}")
        return False
    except Exception as e: # Catching broader CSV parsing issues
        print(f"Error parsing CSV file '{input_filepath}': {e}. Check delimiter and file format.")
        return False

    if not data_list and not csv_reader.fieldnames: # Double check if anything was really processed
        # This condition might indicate a serious issue with delimiter or file structure
        # such that DictReader couldn't even establish fieldnames.
        print(f"No data processed from CSV. Output JSON will likely be empty or just '[]'.")


    try:
        print(f"Attempting to write JSON data to: '{output_filepath}'")
        with open(output_filepath, mode='w', encoding='utf-8') as json_file:
            # Write the list of dictionaries as a JSON array, pretty-printed
            json.dump(data_list, json_file, indent=4)
        print(f"Successfully converted '{input_filepath}' to '{output_filepath}'.")
        return True

    except IOError as e:
        print(f"Error writing output JSON file '{output_filepath}': {e}")
        return False
    except TypeError as e: # Handles issues if data_list contains non-serializable types
        print(f"Error during JSON serialization: {e}. Ensure CSV data is compatible.")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert a CSV file to a JSON file.",
        epilog="Example: python csvToJson.py input.csv output.json --delimiter \";\""
    )
    parser.add_argument("input_csv_file", help="Path to the input CSV file.")
    parser.add_argument("output_json_file", help="Path for the output JSON file.")
    parser.add_argument(
        "--delimiter",
        default=",",
        help="Delimiter used in the CSV file (e.g., ',', ';', '\\t'). Default is comma."
    )

    args = parser.parse_args()

    # For tab delimiter, argparse might pass it as "\\t" string. We need actual tab.
    delimiter_to_use = args.delimiter
    if delimiter_to_use == '\\t':
        delimiter_to_use = '\t'

    print(f"Input CSV: {args.input_csv_file}")
    print(f"Output JSON: {args.output_json_file}")
    print(f"Using delimiter: '{delimiter_to_use}' (raw arg: '{args.delimiter}')")

    success = convert_csv_to_json(args.input_csv_file, args.output_json_file, delimiter_to_use)

    if success:
        print("Conversion process completed successfully.")
    else:
        print("Conversion process failed.")
