#!/usr/bin/env python3

import os
import argparse
import re
import glob
from datetime import datetime
import sys

# --- Language Definitions for Comment Styles ---
# style: 'line' for single-line prefix, 'block_c' for C-style /* ... */ on each line,
# 'block_hash' for # on each line (like Python docstrings often treated for headers)
# 'block_xml' for XML/HTML style comments
LANGUAGE_COMMENT_STYLES = {
    "Python": {"extensions": [".py", ".pyw"], "style": "line", "prefix": "# "},
    "JavaScript": {"extensions": [".js"], "style": "line", "prefix": "// "}, # Or block_c
    "Java": {"extensions": [".java", ".scala", ".kt", ".groovy"], "style": "line", "prefix": "// "}, # Or block_c
    "C": {"extensions": [".c", ".h"], "style": "block_c_ SPDX"}, # SPDX often first
    "C++": {"extensions": [".cpp", ".hpp", ".cc", ".hh", ".cxx", ".hxx"], "style": "block_c_SPDX"},
    "Shell": {"extensions": [".sh", ".bash", ".ksh", ".zsh"], "style": "line", "prefix": "# "},
    "HTML": {"extensions": [".html", ".htm"], "style": "block_xml"},
    "XML": {"extensions": [".xml", ".xaml", ".xsl", ".xslt", ".xsd", ".csproj"], "style": "block_xml"},
    "CSS": {"extensions": [".css"], "style": "block_c"},
    "Ruby": {"extensions": [".rb"], "style": "line", "prefix": "# "},
    "Perl": {"extensions": [".pl", ".pm"], "style": "line", "prefix": "# "},
    # Add more languages:
    # "Go": {"extensions": [".go"], "style": "line", "prefix": "// "},
}

# Build reverse map for quick lookup
EXTENSION_TO_LANG_STYLE = {}
for lang, details in LANGUAGE_COMMENT_STYLES.items():
    for ext in details["extensions"]:
        EXTENSION_TO_LANG_STYLE[ext] = {"language": lang, **details}


# --- Helper Functions ---
def load_license_template(template_filepath, year_to_insert):
    """Loads license template and replaces placeholders like {{YEAR}}."""
    try:
        with open(template_filepath, 'r', encoding='utf-8') as f:
            template_content = f.read()
        # Replace placeholders
        template_content = template_content.replace("{{YEAR}}", str(year_to_insert))
        # Add more placeholder replacements here if needed
        return template_content.splitlines() # Return as a list of lines
    except FileNotFoundError:
        print(f"Error: License template file '{template_filepath}' not found.", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error reading or processing template file '{template_filepath}': {e}", file=sys.stderr)
        return None

def format_license_for_lang(license_lines, lang_style_info):
    """Formats the license text with language-specific comment markers."""
    style = lang_style_info["style"]
    formatted_lines = []

    if style == "line":
        prefix = lang_style_info["prefix"]
        for line in license_lines:
            formatted_lines.append(f"{prefix}{line}".rstrip()) # rstrip to remove trailing space if line is empty
    elif style == "block_c" or style == "block_c_SPDX":
        # Standard C-style block comment where each line often starts with ' * '
        # SPDX variant often has the SPDX line first, then /*
        if style == "block_c_SPDX" and license_lines and "SPDX-License-Identifier:" in license_lines[0]:
            formatted_lines.append(f"// {license_lines[0]}") # Assuming // for SPDX line as common practice
            formatted_lines.append("/*")
            for line in license_lines[1:]: # Remaining lines
                formatted_lines.append(f" * {line}".rstrip())
            formatted_lines.append(" */")
        else: # Regular block_c
            formatted_lines.append("/*")
            for line in license_lines:
                formatted_lines.append(f" * {line}".rstrip())
            formatted_lines.append(" */")
    elif style == "block_xml": # HTML, XML
        formatted_lines.append("<!--")
        for line in license_lines:
            formatted_lines.append(f"  {line}".rstrip()) # Indent content
        formatted_lines.append("-->")
    else: # Fallback or unknown style, treat as plain text (no comments)
        formatted_lines = license_lines

    return formatted_lines

def check_for_existing_header(file_lines, formatted_header_lines, lang_style):
    """
    Checks if a version of the header already exists.
    Returns:
        "identical" if an exact match is found.
        "present_different" if a comment block resembling a license is found but not identical.
        None if no significant header comment block is found at the top.
    This is a heuristic. A common check is for a copyright string or a specific license ID.
    For this version, we'll check if the file starts with the exact formatted header.
    A more advanced check could strip comment markers and compare raw text, or look for specific keywords.
    """
    if not file_lines or not formatted_header_lines:
        return None

    # Simple check: does the file start exactly with the formatted header?
    if len(file_lines) >= len(formatted_header_lines):
        potential_existing_header = file_lines[:len(formatted_header_lines)]
        if potential_existing_header == formatted_header_lines:
            return "identical"

    # Heuristic: check for any comment block at the beginning of the file
    # This is very basic. For example, check if first few lines are comments.
    # A more robust check would look for "Copyright" or "Licensed under" etc.
    # For this script, we'll keep it simple: if not identical, it's either not there or different.
    # We won't try to differentiate "present_different" vs "None" very hard without more specific markers.

    # Let's check if the file starts with *any* comment block of the expected type.
    # This is still tricky. For now, "identical" or "assume_not_present_or_different".
    # A placeholder for a more advanced check:
    # if file_lines[0].strip().startswith(lang_style.get("prefix", "###INVALID###").strip()) or \
    #    file_lines[0].strip().startswith("/*") or \
    #    file_lines[0].strip().startswith("<!--"):
    #     # This means there's *some* comment at the top. Is it *our* license, but different?
    #     # This requires comparing the content of the comment block, not just its presence.
    #     # For now, if it's not an identical match, we'll treat it as "needs update/add".
    #     pass

    return None # Assume not present or different if not an exact match


def process_target_file(filepath, license_template_lines, lang_style_map, current_year, dry_run, update_existing_flag):
    """Processes a single file to add/update license header."""
    _, extension = os.path.splitext(filepath)
    extension = extension.lower()

    lang_info = lang_style_map.get(extension)
    if not lang_info:
        print(f"Skipping '{filepath}': Unknown file type or unsupported extension '{extension}'.")
        return "skipped_unsupported", 0

    # Generate the desired header for this file type
    # The template lines are already year-replaced if placeholder was used
    formatted_header = format_license_for_lang(license_template_lines, lang_info)
    if not formatted_header: # Should not happen if lang_info is valid
        print(f"Warning: Could not format header for '{filepath}'. Skipping.", file=sys.stderr)
        return "skipped_formatting_error", 0

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            original_content_lines = f.read().splitlines()
    except Exception as e:
        print(f"Error reading file '{filepath}': {e}. Skipping.", file=sys.stderr)
        return "error_reading", 0

    # Check for shebang in the first line for certain file types (e.g. Python, Shell)
    shebang_line = None
    content_starts_at_line_idx = 0
    if lang_info["language"] in ["Python", "Shell", "Perl", "Ruby"]: # Add others if needed
        if original_content_lines and original_content_lines[0].startswith("#!"):
            shebang_line = original_content_lines[0]
            content_starts_at_line_idx = 1

    # Check existing header (on content after potential shebang)
    header_status = check_for_existing_header(original_content_lines[content_starts_at_line_idx:], formatted_header, lang_info)

    if header_status == "identical":
        print(f"'{filepath}': License header already present and identical. Skipping.")
        return "skipped_identical", 0

    action_taken_message = ""
    # For now, treat "present_different" similar to not present for simplicity,
    # unless --update-existing is smarter.
    # Current check_for_existing_header only returns "identical" or None.

    # If we are here, header is not identical or not found.
    # A more advanced version would remove an old, different header if --update-existing.
    # For now, we just prepend if not identical. This could lead to double headers if an old one exists.
    # Let's refine: if --update-existing, and some comment block is at top, remove it.
    # This is still heuristic. Best is usually to remove N lines if an old header is detected.

    # Simple "prepend" logic for this version:
    lines_to_write = []
    if shebang_line:
        lines_to_write.append(shebang_line)

    lines_to_write.extend(formatted_header)
    # Add a blank line after header if content exists and header doesn't end with blank
    if original_content_lines[content_starts_at_line_idx:] and formatted_header and formatted_header[-1].strip() != "":
        lines_to_write.append("")

    lines_to_write.extend(original_content_lines[content_starts_at_line_idx:])

    final_content = "\n".join(lines_to_write) + "\n" # Ensure trailing newline

    if dry_run:
        action_taken_message = f"'{filepath}': Would prepend license header."
        if header_status is not None : # Placeholder for more detailed status
             action_taken_message = f"'{filepath}': Would update existing header (simplified: treat as prepend)."
        print(action_taken_message)
        return "dry_run_action", 1 # "1" meaning one file would be affected
    else:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(final_content)
            action_taken_message = f"'{filepath}': Prepended license header."
            if header_status is not None:
                 action_taken_message = f"'{filepath}': Updated license header (simplified: treated as prepend)."
            print(action_taken_message)
            return "modified", 1
        except Exception as e:
            print(f"Error writing changes to '{filepath}': {e}. Skipping.", file=sys.stderr)
            return "error_writing", 0


def collect_target_files(targets_patterns_list):
    """Collects all files based on input targets (files, dirs, globs)."""
    # This is a simplified collector. It assumes targets are file paths or globs.
    # It does not recursively walk directories unless glob pattern `**` is used.
    # For explicit directory targets, user should use `my_dir/**/*.py` or similar.
    collected_files = set()
    for pattern in targets_patterns_list:
        # Use glob for all patterns; it handles direct file paths correctly too.
        # Set recursive=True to enable `**` globbing.
        expanded_paths = glob.glob(pattern, recursive=True)
        for path_item in expanded_paths:
            if os.path.isfile(path_item):
                collected_files.add(os.path.abspath(path_item))
    return sorted(list(collected_files))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Add or update license headers in source files.",
        epilog='Example: python licenseHeaderAdder.py --template lic.txt "src/**/*.py" --year 2023'
    )
    parser.add_argument(
        "--template",
        required=True,
        help="Path to the license header template file (plain text)."
    )
    parser.add_argument(
        "targets",
        nargs="+",
        help="One or more file paths or glob patterns (e.g., '*.py', 'src/**/*.java'). Quote patterns."
    )
    parser.add_argument(
        "--year",
        default=str(datetime.now().year),
        help="Year to use for placeholders like {{YEAR}} in the template. Defaults to current year."
    )
    parser.add_argument(
        "--update-existing", # This flag is noted, but current implementation is simple prepend
        action="store_true",
        help="If an existing header is found and is different, attempt to update it. (Currently, this means replace if any comment block is at top - very heuristic or just prepend)."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what files would be modified, but do not make any changes."
    )

    args = parser.parse_args()

    print("--- License Header Adder ---")
    if args.dry_run:
        print("Dry Run Mode: No files will be modified.\n")

    license_lines = load_license_template(args.template, args.year)
    if license_lines is None:
        sys.exit(1)

    target_files = collect_target_files(args.targets)
    if not target_files:
        print("No files found matching the specified targets.")
        sys.exit(0)

    print(f"Found {len(target_files)} file(s) to process...")

    files_modified_count = 0
    files_skipped_identical_count = 0
    files_skipped_unsupported_count = 0
    files_error_count = 0

    for f_path in target_files:
        status, count_modified_flag = process_target_file(
            f_path,
            license_lines,
            EXTENSION_TO_LANG_STYLE,
            args.year, # Year already used in load_license_template, not strictly needed here
            args.dry_run,
            args.update_existing
        )
        if status == "modified" or status == "dry_run_action":
            files_modified_count += count_modified_flag # Should be 1 if action would be taken
        elif status == "skipped_identical":
            files_skipped_identical_count += 1
        elif status == "skipped_unsupported":
            files_skipped_unsupported_count +=1
        elif status == "error_reading" or status == "error_writing" or status == "skipped_formatting_error":
            files_error_count +=1


    print("\n--- Summary ---")
    if args.dry_run:
        print(f"Files that would be modified: {files_modified_count}")
    else:
        print(f"Files actually modified: {files_modified_count}")
    print(f"Files skipped (header identical): {files_skipped_identical_count}")
    print(f"Files skipped (unsupported type): {files_skipped_unsupported_count}")
    print(f"Files with errors (read/write/format): {files_error_count}")

    print("\nLicense header processing complete.")
    sys.exit(0)
