#!/usr/bin/env python3

import subprocess
import argparse
import re
from collections import defaultdict
import sys
import os

# --- Git Command Runner ---
def run_git_command(command_list):
    """Runs a git command and returns its stdout, stderr, and return code."""
    try:
        process = subprocess.run(command_list, capture_output=True, text=True, check=False, encoding='utf-8')
        return process.stdout.strip(), process.stderr.strip(), process.returncode
    except FileNotFoundError:
        return None, "Error: 'git' command not found. Ensure Git is installed and in PATH.", -1
    except Exception as e:
        return None, f"Error running command '{' '.join(command_list)}': {e}", -2

# --- Changelog Configuration ---
# Conventional Commit types and their corresponding changelog sections
# Order here will influence order in changelog
CONVENTIONAL_COMMIT_TYPES_TO_SECTIONS = {
    "feat": "🚀 Features",
    "fix": "🐛 Bug Fixes",
    "perf": "⚡ Performance Improvements",
    "build": "🏗️ Build System & Dependencies",
    "ci": "🔄 Continuous Integration",
    "docs": "📚 Documentation",
    "refactor": "✨ Refactoring",
    "style": "💄 Code Style",
    "test": "✅ Testing",
    "chore": "🧹 Chores & Maintenance",
    # Add more or customize as needed
}
# Commits that don't match these will go into a "Miscellaneous" section or be skipped.
DEFAULT_MISC_SECTION_TITLE = "📝 Miscellaneous Tasks"

# Regex to parse conventional commit messages
# Example: feat(scope)!: description
# Group 1: type (feat)
# Group 3: scope (optional scope)
# Group 4: ! (optional breaking change indicator)
# Group 5: subject (description)
CONVENTIONAL_COMMIT_REGEX = re.compile(r"^(\w+)(\(([\w\-\.]+)\))?(!)?: (.*)$")


def get_latest_git_tag():
    """Fetches the most recent tag from the repository."""
    stdout, stderr, retcode = run_git_command(['git', 'describe', '--tags', '--abbrev=0'])
    if retcode == 0 and stdout:
        return stdout
    else:
        # Try to get the first commit if no tags are found
        # print("Warning: No tags found to default '--from-rev'. Trying first commit.", file=sys.stderr)
        # stdout_fc, stderr_fc, retcode_fc = run_git_command(['git', 'rev-list', '--max-parents=0', 'HEAD'])
        # if retcode_fc == 0 and stdout_fc:
        #     return stdout_fc.splitlines()[0] # Get the first line (oldest commit)
        # print(f"Warning: Could not get latest tag or first commit. Git error: {stderr or stderr_fc}", file=sys.stderr)
        return None # Indicate failure to find a default "from"

def get_commit_details(commit_hash, format_str="%s"):
    """Gets specific details for a single commit."""
    stdout, _, retcode = run_git_command(['git', 'show', '-s', f"--format={format_str}", commit_hash])
    return stdout if retcode == 0 else None


def generate_changelog_data(from_revision, to_revision, excluded_types_list):
    """
    Fetches git log between revisions and parses commits.
    Returns a dictionary of categorized commits and a list of breaking changes.
    """
    # Using a unique multi-char separator to reduce chance of it appearing in commit messages
    # Format: HASH<SEP>SUBJECT<SEP>BODY<SEP>AUTHOR_NAME<SEP>COMMIT_DATE_ISO
    # Body (%b) can be multi-line. Need to handle that.
    # A more robust way is one commit per `git show` call or use null terminators.
    # For simplicity, let's try a simpler format first, subject only for categorization.
    # Format: HASH<--GITLINE-->SUBJECT
    # We can fetch more details later if needed for the body.

    log_format = "%H<--GITLINE-->%s" # Hash and Subject
    git_log_command = ['git', 'log', f"{from_revision}..{to_revision}", f"--pretty=format:{log_format}", "--no-merges"]

    stdout, stderr, retcode = run_git_command(git_log_command)
    if retcode != 0:
        print(f"Error fetching git log: {stderr}", file=sys.stderr)
        # Try to see if revisions are valid
        for rev in [from_revision, to_revision]:
            _, _, rev_retcode = run_git_command(['git', 'rev-parse', '--verify', f"{rev}^{{commit}}"])
            if rev_retcode != 0:
                print(f"Error: Revision '{rev}' is not a valid Git revision.", file=sys.stderr)
        return None, None

    categorized_commits = defaultdict(list)
    breaking_changes = [] # List of {"hash": ..., "subject": ..., "body_note": ...}

    for line in stdout.splitlines():
        if not line:
            continue

        parts = line.split("<--GITLINE-->", 1)
        if len(parts) != 2:
            # print(f"Warning: Skipping malformed log line: {line}", file=sys.stderr)
            continue # Should not happen with the format string used

        commit_hash_full, subject_full = parts
        commit_hash_short = commit_hash_full[:7] # Short hash

        match = CONVENTIONAL_COMMIT_REGEX.match(subject_full)
        commit_type = None
        commit_scope = None
        is_breaking = False
        subject_text = subject_full # Default if not conventional

        if match:
            commit_type = match.group(1).lower()
            commit_scope = match.group(3) # Can be None
            is_breaking = (match.group(4) == '!')
            subject_text = match.group(5)

        if commit_type in excluded_types_list:
            continue

        # Add to breaking changes list if marked or "BREAKING CHANGE:" in body (more advanced)
        if is_breaking:
            # For now, just use subject. A full implementation would fetch body for breaking change details.
            breaking_changes.append({
                "hash": commit_hash_short,
                "subject": subject_text,
                "type": commit_type,
                "scope": commit_scope,
                "original_subject": subject_full
            })

        commit_data = {
            "hash": commit_hash_short,
            "subject": subject_text,
            "type": commit_type,
            "scope": commit_scope,
            "original_subject": subject_full # Keep original for uncategorized or if needed
        }

        if commit_type and commit_type in CONVENTIONAL_COMMIT_TYPES_TO_SECTIONS:
            section_title = CONVENTIONAL_COMMIT_TYPES_TO_SECTIONS[commit_type]
            categorized_commits[section_title].append(commit_data)
        else:
            # If no type or type not in mapping, add to miscellaneous
            categorized_commits[DEFAULT_MISC_SECTION_TITLE].append(commit_data)

    return categorized_commits, breaking_changes


def print_markdown_changelog(categorized_commits, breaking_changes, from_rev, to_rev):
    """Prints the changelog in Markdown format."""
    print(f"# Changelog: {from_rev} ... {to_rev}\n")

    if breaking_changes:
        print("## 💥 BREAKING CHANGES")
        for bc in breaking_changes:
            scope_str = f"**({bc['scope']})**" if bc['scope'] else ""
            print(f"- **{bc['type']}{scope_str}:** {bc['subject']} ({bc['hash']})")
            # Here one might add details from commit body if fetched
        print("\n")

    # Print in the order defined in CONVENTIONAL_COMMIT_TYPES_TO_SECTIONS, then miscellaneous
    sorted_sections = list(CONVENTIONAL_COMMIT_TYPES_TO_SECTIONS.values())
    if DEFAULT_MISC_SECTION_TITLE in categorized_commits and DEFAULT_MISC_SECTION_TITLE not in sorted_sections:
        sorted_sections.append(DEFAULT_MISC_SECTION_TITLE)

    for section_title in sorted_sections:
        if section_title in categorized_commits:
            commits_in_section = categorized_commits[section_title]
            if not commits_in_section: continue

            print(f"## {section_title}\n")
            for commit in commits_in_section:
                # Avoid listing breaking changes again if they are already under their type
                # For simplicity, list them. Or filter them out if already in breaking_changes list by hash.
                # For now, they will appear in both sections if they matched a type.

                scope_str = f"**({commit['scope']})**" if commit['scope'] else ""
                # If it's from misc section and we have original_subject, maybe use that if it wasn't parsed.
                # For conventional, subject_text is cleaner.
                display_subject = commit['subject']
                if section_title == DEFAULT_MISC_SECTION_TITLE and not commit['type']: # Was not parsed as conventional
                    display_subject = commit['original_subject']


                print(f"- {scope_str}{display_subject} ({commit['hash']})")
            print("\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a changelog from Git log messages based on Conventional Commits.",
        epilog='Example: python changelogGenerator.py --from-rev v1.0.0 --to-rev v1.1.0 --exclude "chore,docs"'
    )
    parser.add_argument(
        "--from-rev",
        help="The starting Git revision (tag, commit hash, branch name). Defaults to the latest tag."
    )
    parser.add_argument(
        "--to-rev",
        default="HEAD",
        help="The ending Git revision (tag, commit hash, branch name). Defaults to HEAD."
    )
    parser.add_argument(
        "--exclude",
        default="chore,docs,style,test", # Common types to exclude from main changelog
        help="Comma-separated list of commit types (e.g., 'feat', 'fix') to exclude. Default: 'chore,docs,style,test'."
    )
    parser.add_argument(
        "--format", # Placeholder for future formats
        default="markdown",
        choices=["markdown"], # Currently only markdown
        help="Output format for the changelog. Default: 'markdown'."
    )

    args = parser.parse_args()

    # --- Preparations ---
    # 1. Check if inside a Git repository
    _, _, retcode_git_repo = run_git_command(['git', 'rev-parse', '--is-inside-work-tree'])
    if retcode_git_repo != 0 or _ != "true": # Output of command is "true" or "false"
        print("Error: This script must be run inside a Git repository.", file=sys.stderr)
        sys.exit(1)

    # 2. Determine revisions
    from_revision = args.from_rev
    if not from_revision:
        from_revision = get_latest_git_tag()
        if not from_revision:
            print("Error: Could not determine default '--from-rev' (no tags found). Please specify a starting revision.", file=sys.stderr)
            sys.exit(1)
        print(f"Defaulted '--from-rev' to latest tag: {from_revision}")

    to_revision = args.to_rev

    # 3. Parse excluded types
    excluded_commit_types = set(t.strip().lower() for t in args.exclude.split(',') if t.strip())

    print(f"Generating changelog from {from_revision} to {to_revision}...")
    if excluded_commit_types:
        print(f"Excluding commit types: {', '.join(sorted(list(excluded_commit_types)))}")

    # --- Generate Data ---
    categorized_data, breaking_changes_data = generate_changelog_data(from_revision, to_revision, excluded_commit_types)

    if categorized_data is None: # Error occurred in generation
        sys.exit(1)

    if not categorized_data and not breaking_changes_data:
        print("No changes found between the specified revisions that match the criteria.")
        sys.exit(0)

    # --- Output Changelog ---
    if args.format == "markdown":
        print_markdown_changelog(categorized_data, breaking_changes_data, from_revision, to_revision)
    else:
        # Should not be reached due to choices in argparse
        print(f"Error: Unsupported format '{args.format}'.", file=sys.stderr)
        sys.exit(1)

    print("\nChangelog generation complete.")
    sys.exit(0)
