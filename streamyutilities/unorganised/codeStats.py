#!/usr/bin/env python3

import os
import argparse
import json
import re
from collections import defaultdict
import fnmatch # For glob-style ignore patterns

# --- Language Definitions (Extensions and Comment Styles) ---
# Simplified from countLines.py for direct inclusion
# Add more languages and their comment styles as needed
LANGUAGE_DEFINITIONS = {
    "Python": {
        "extensions": [".py", ".pyw"],
        "single_line_comment": re.compile(r'^\s*#'),
        "block_comment_start": None, # Python doesn't have block comments like /* ... */
        "block_comment_end": None,
    },
    "JavaScript": {
        "extensions": [".js"],
        "single_line_comment": re.compile(r'^\s*//'),
        "block_comment_start": re.compile(r'^\s*/\*'), # Simplified: line must start with /*
        "block_comment_end": re.compile(r'\*/\s*$'),   # Simplified: line must end with */
    },
    "Java": {
        "extensions": [".java"],
        "single_line_comment": re.compile(r'^\s*//'),
        "block_comment_start": re.compile(r'^\s*/\*'),
        "block_comment_end": re.compile(r'\*/\s*$'),
    },
    "C": {
        "extensions": [".c", ".h"],
        "single_line_comment": re.compile(r'^\s*//'), # C99+
        "block_comment_start": re.compile(r'^\s*/\*'),
        "block_comment_end": re.compile(r'\*/\s*$'),
    },
    "C++": {
        "extensions": [".cpp", ".hpp", ".cc", ".hh", ".cxx", ".hxx"],
        "single_line_comment": re.compile(r'^\s*//'),
        "block_comment_start": re.compile(r'^\s*/\*'),
        "block_comment_end": re.compile(r'\*/\s*$'),
    },
    "Shell": { # Bash, sh etc.
        "extensions": [".sh", ".bash"],
        "single_line_comment": re.compile(r'^\s*#'),
        "block_comment_start": None,
        "block_comment_end": None,
    },
    "HTML": { # HTML comments are <!-- ... -->, harder with line-based, treat as no line comments for simple LoC
        "extensions": [".html", ".htm"],
        "single_line_comment": None,
        "block_comment_start": re.compile(r'^\s*<!--'),
        "block_comment_end": re.compile(r'-->\s*$'),
    },
    "CSS": {
        "extensions": [".css"],
        "single_line_comment": None, # No standard single-line comment like //
        "block_comment_start": re.compile(r'^\s*/\*'),
        "block_comment_end": re.compile(r'\*/\s*$'),
    },
    # Add more languages here
}

# Reverse map for quick language lookup by extension
EXTENSION_TO_LANGUAGE = {}
for lang, details in LANGUAGE_DEFINITIONS.items():
    for ext in details["extensions"]:
        EXTENSION_TO_LANGUAGE[ext] = lang

# --- LoC Counting Function (Adapted from countLines.py logic) ---
def count_loc_in_file_content(content_lines, language_name):
    """Counts lines of code (non-empty, non-comment) in a list of content lines."""
    loc = 0
    lang_def = LANGUAGE_DEFINITIONS.get(language_name, {})
    single_line_re = lang_def.get("single_line_comment")
    block_start_re = lang_def.get("block_comment_start")
    block_end_re = lang_def.get("block_comment_end")

    in_block_comment = False
    for line in content_lines:
        stripped_line = line.strip()
        if not stripped_line: # Skip empty lines
            continue

        is_comment_line = False
        # Handle block comments (simplified logic)
        if block_start_re: # If language supports block comments
            if in_block_comment:
                if block_end_re and block_end_re.search(line): # End of block
                    in_block_comment = False
                is_comment_line = True # Line is part of a block comment
            elif block_start_re.search(line): # Start of a block
                in_block_comment = True
                is_comment_line = True # Line starting the block is a comment line
                if block_end_re and block_end_re.search(line): # Block ends on same line
                    in_block_comment = False

        # Handle single-line comments if not already in a block or if line isn't fully consumed by block
        if not is_comment_line and single_line_re:
            if single_line_re.match(stripped_line): # Check if line starts with comment (ignoring whitespace)
                is_comment_line = True

        if not is_comment_line:
            loc += 1
    return loc

# --- Main Script ---
def analyze_project(target_dir, ignore_patterns_str, output_format):
    abs_target_dir = os.path.abspath(target_dir)
    if not os.path.isdir(abs_target_dir):
        print(f"Error: Target directory '{abs_target_dir}' not found or is not a directory.", file=sys.stderr)
        return

    # Process ignore patterns
    # Simple split by comma. Users should be careful with spaces.
    raw_ignore_patterns = [p.strip() for p in ignore_patterns_str.split(',') if p.strip()]
    # Separate dir patterns from file patterns for os.walk optimization
    ignore_dir_names = {p for p in raw_ignore_patterns if not any(c in p for c in ['*', '?', '[']) and p.endswith('/')}
    ignore_file_patterns = [p for p in raw_ignore_patterns if p not in ignore_dir_names]
    # Normalize dir patterns by removing trailing slash for comparison with os.path.basename
    ignore_dir_names = {p.rstrip('/') for p in ignore_dir_names}


    language_stats = defaultdict(lambda: {"files": 0, "loc": 0})
    unknown_extensions = defaultdict(int)

    print(f"Scanning directory: {abs_target_dir}")
    if raw_ignore_patterns:
        print(f"Ignoring patterns: {', '.join(raw_ignore_patterns)}")


    for root, dirs, files in os.walk(abs_target_dir, topdown=True):
        # Filter directories to ignore (modifying dirs list in place for os.walk)
        dirs[:] = [d for d in dirs if d not in ignore_dir_names and not any(fnmatch.fnmatch(d, pat.rstrip('/')) for pat in ignore_file_patterns if pat.endswith('/'))]


        for filename in files:
            # Filter files by ignore patterns
            if any(fnmatch.fnmatch(filename, file_pat) for file_pat in ignore_file_patterns if not file_pat.endswith('/')):
                continue

            filepath = os.path.join(root, filename)
            _, extension = os.path.splitext(filename)
            extension = extension.lower()

            language = EXTENSION_TO_LANGUAGE.get(extension)
            if language:
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()

                    loc = count_loc_in_file_content(lines, language)
                    language_stats[language]["files"] += 1
                    language_stats[language]["loc"] += loc
                except Exception as e:
                    print(f"Warning: Could not process file '{filepath}': {e}", file=sys.stderr)
            elif extension: # Has an extension but not mapped
                unknown_extensions[extension] += 1

    # Calculate total LoC for percentage calculation
    total_loc_all_langs = sum(stats["loc"] for stats in language_stats.values())

    # Prepare results for output
    output_data = {
        "languages": [],
        "summary": {
            "total_files": sum(s["files"] for s in language_stats.values()),
            "total_loc": total_loc_all_langs,
        },
        "unknown_extensions_count": sum(unknown_extensions.values()),
        "unknown_extensions_details": dict(unknown_extensions) if unknown_extensions else {}
    }

    for lang, stats in sorted(language_stats.items(), key=lambda item: item[1]["loc"], reverse=True):
        percentage = (stats["loc"] / total_loc_all_langs * 100) if total_loc_all_langs > 0 else 0
        output_data["languages"].append({
            "language": lang,
            "files": stats["files"],
            "loc": stats["loc"],
            "percentage": round(percentage, 2)
        })

    # Display results
    if output_format == 'json':
        print(json.dumps(output_data, indent=4))
    else: # Text format
        print("\n--- Code Statistics ---")
        if not output_data["languages"]:
            print("No source code files found or processed.")
        else:
            header = "{:<15} | {:>8} | {:>12} | {:>10}".format("Language", "Files", "Lines of Code", "Percentage")
            print(header)
            print("-" * len(header))
            for lang_data in output_data["languages"]:
                print("{:<15} | {:>8} | {:>12} | {:>9.2f}%".format(
                    lang_data["language"],
                    lang_data["files"],
                    lang_data["loc"],
                    lang_data["percentage"]
                ))
            print("-" * len(header))
            print("{:<15} | {:>8} | {:>12} | {:>9.2f}%".format(
                "Total",
                output_data["summary"]["total_files"],
                output_data["summary"]["total_loc"],
                100.00 if total_loc_all_langs > 0 else 0.00
            ))

        if output_data["unknown_extensions_count"] > 0:
            print(f"\nFound {output_data['unknown_extensions_count']} file(s) with unmapped extensions.")
            # Optionally list them: print(output_data["unknown_extensions_details"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Scan a directory for source code files and generate language statistics.",
        epilog="Example: python codeStats.py /path/to/project --ignore \"*.log,build/,dist/,.git/\""
    )
    parser.add_argument(
        "target_directory",
        nargs="?", # Optional, defaults to current dir
        default=".",
        help="The target directory to scan. Defaults to the current directory."
    )
    parser.add_argument(
        "--ignore",
        type=str,
        default=".git/,.vscode/,__pycache__/,node_modules/,venv/,build/,dist/,*.pyc,*.log,*.tmp,*.swp",
        help="Comma-separated list of directory names or file patterns to ignore (e.g., \"*.log,build/,dist/\"). "
             "Directory patterns should end with '/' (e.g., 'node_modules/'). Default ignores common ones."
    )
    parser.add_argument(
        "--format",
        choices=['text', 'json'],
        default='text',
        help="Output format for the statistics. Default: 'text'."
    )

    args = parser.parse_args()

    analyze_project(args.target_directory, args.ignore, args.format)
    print("\nCode statistics process complete.")
