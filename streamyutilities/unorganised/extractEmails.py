#!/usr/bin/env python3

import os
import re
import argparse

# Regex for finding email addresses (common practical version)
# Handles most typical email addresses.
# Does not aim for full RFC 5322 compliance as that is extremely complex.
EMAIL_REGEX = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")


def extract_emails_from_content(content):
    """Extracts email addresses from a string content using regex."""
    return EMAIL_REGEX.findall(content)


def process_files(filepaths):
    """
    Reads content from multiple files and extracts unique email addresses.
    Returns a set of unique email addresses found.
    """
    unique_emails = set()

    for filepath in filepaths:
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            emails_in_file = extract_emails_from_content(content)
            if emails_in_file:
                unique_emails.update(emails_in_file)
            print(f"Processed '{filepath}', found {len(emails_in_file)} email(s).")
        except FileNotFoundError:
            print(f"Error: File '{filepath}' not found. Skipping.")
        except IOError as e:
            print(f"Error reading file '{filepath}': {e}. Skipping.")
        except Exception as e:
            print(
                f"An unexpected error occurred with file '{filepath}': {e}. Skipping."
            )

    return unique_emails


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract email addresses from one or more files.",
        epilog="Example: python extractEmails.py doc.txt --output emails.txt",
    )
    parser.add_argument(
        "filepaths",
        nargs="+",
        help="One or more paths to files to process for email extraction.",
    )
    parser.add_argument(
        "--output",
        metavar="OUTPUT_FILE",
        help="Optional: File to save the extracted unique email addresses to (one email per line).",
    )

    args = parser.parse_args()

    print(f"Starting email extraction from {len(args.filepaths)} file(s)...")
    extracted_emails_set = process_files(args.filepaths)

    if not extracted_emails_set:
        print("\nNo email addresses found in the processed files.")
    else:
        print(
            f"\nFound a total of {len(extracted_emails_set)} unique email address(es)."
        )
        if args.output:
            try:
                with open(args.output, "w", encoding="utf-8") as outfile:
                    for email in sorted(
                        list(extracted_emails_set)
                    ):  # Sort for consistent output
                        outfile.write(email + "\n")
                print(f"Successfully saved extracted emails to '{args.output}'.")
            except IOError as e:
                print(f"Error writing emails to output file '{args.output}': {e}")
                print("Printing emails to console instead:")
                for email in sorted(list(extracted_emails_set)):
                    print(email)
        else:
            print("Extracted unique email addresses:")
            for email in sorted(
                list(extracted_emails_set)
            ):  # Sort for consistent output
                print(email)

    print("\nExtraction process complete.")
