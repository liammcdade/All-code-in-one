#!/usr/bin/env python3

import subprocess
import argparse
import sys
import os
import re

DEFAULT_PROTECTED_BRANCHES = ["main", "master", "develop", "dev"]

def run_git_command(command_list):
    """Runs a git command and returns its stdout, stderr, and return code."""
    try:
        process = subprocess.run(command_list, capture_output=True, text=True, check=False)
        # `check=False` means it won't raise CalledProcessError for non-zero exit codes.
        # We'll handle errors based on returncode.
        return process.stdout.strip(), process.stderr.strip(), process.returncode
    except FileNotFoundError: # Git not found
        return None, "Error: 'git' command not found. Please ensure Git is installed and in your PATH.", -1
    except Exception as e:
        return None, f"Error running command '{' '.join(command_list)}': {e}", -2

def get_current_branch_name():
    """Gets the current Git branch name."""
    stdout, stderr, retcode = run_git_command(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
    if retcode == 0 and stdout and stdout != "HEAD": # Not in detached HEAD state
        return stdout
    elif stdout == "HEAD": # Detached HEAD
        # Try to get a more specific ref if possible, e.g. a tag name
        stdout_descr, _, retcode_descr = run_git_command(['git', 'describe', '--tags', '--exact-match', 'HEAD'])
        if retcode_descr == 0 and stdout_descr:
            return f"detached HEAD at {stdout_descr}"
        # Fallback to short commit hash if no tag
        stdout_hash, _, retcode_hash = run_git_command(['git', 'rev-parse', '--short', 'HEAD'])
        if retcode_hash == 0 and stdout_hash:
            return f"detached HEAD at {stdout_hash}"
        return "detached HEAD" # Generic if others fail
    else:
        # print(f"Warning: Could not determine current branch. Git error: {stderr}", file=sys.stderr)
        return None # Could not determine current branch

def get_local_branches():
    """Gets a list of all local branches."""
    stdout, stderr, retcode = run_git_command(['git', 'branch'])
    if retcode != 0:
        print(f"Error listing local branches: {stderr}", file=sys.stderr)
        return None
    branches = []
    for line in stdout.splitlines():
        # Strip leading '*' and whitespace
        branch_name = line.lstrip('* ').strip()
        branches.append(branch_name)
    return branches

def main():
    parser = argparse.ArgumentParser(
        description="Clean up local Git branches that have been merged into a target branch.",
        epilog="Example: python gitBranchCleanup.py --target-branch main --protect develop,release --dry-run"
    )
    parser.add_argument(
        "--target-branch",
        help="The branch to check for merged status against. Defaults to the current branch (if not detached) or 'main'/'master'."
    )
    parser.add_argument(
        "--protect",
        default=",".join(DEFAULT_PROTECTED_BRANCHES),
        help=f"Comma-separated list of branches to protect from deletion. Default: {','.join(DEFAULT_PROTECTED_BRANCHES)}"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List branches that would be deleted, but do not delete them."
    )

    args = parser.parse_args()

    print("--- Git Branch Cleanup Utility ---")
    print("WARNING: This script will delete local Git branches. Ensure you understand its operation.\n")

    # 1. Check if inside a Git repository
    _, stderr_git_repo, retcode_git_repo = run_git_command(['git', 'rev-parse', '--is-inside-work-tree'])
    if retcode_git_repo != 0 or stderr_git_repo == "Not a git repository": # Check specific stderr for older git
        # The command might output "true" to stdout but also "Not a git repository" to stderr in some git versions if run outside
        # A more reliable check is often `git rev-parse --git-dir` failing.
        # For now, if `is-inside-work-tree` fails or its output is not "true" (it prints "true" or "false")
        # Let's check the output of the command itself for "true"
        stdout_is_repo, _, _ = run_git_command(['git', 'rev-parse', '--is-inside-work-tree'])
        if stdout_is_repo != "true":
             print("Error: Not inside a Git repository.", file=sys.stderr)
             return


    # 2. Determine protected branches
    protected_branches = set(p.strip() for p in args.protect.split(',') if p.strip())
    print(f"Protected branches: {', '.join(sorted(list(protected_branches)))}")

    # 3. Determine current branch and target branch
    actual_current_branch = get_current_branch_name()
    if actual_current_branch is None or "detached HEAD" in actual_current_branch:
        print(f"Currently in a '{actual_current_branch or 'unknown'}' state.", file=sys.stderr)
        if args.target_branch:
            target_branch = args.target_branch
        else: # Default to main or master if detached and no target specified
            local_branches_for_default = get_local_branches()
            if local_branches_for_default is None: 
                return
            if "main" in local_branches_for_default: target_branch = "main"
            elif "master" in local_branches_for_default: target_branch = "master"
            else:
                print("Error: Detached HEAD and could not determine a default target branch ('main' or 'master' not found). Please specify --target-branch.", file=sys.stderr)
                return
            print(f"Defaulting target branch to '{target_branch}' due to detached HEAD state.")
    else:
        print(f"Current branch is: '{actual_current_branch}'")
        target_branch = args.target_branch if args.target_branch else actual_current_branch

    # Verify target branch exists
    all_local_branches = get_local_branches()
    if all_local_branches is None: 
        return
    if target_branch not in all_local_branches and target_branch not in (actual_current_branch if actual_current_branch else ""): # target_branch could be current if it's symbolic like 'HEAD'
        # A more robust check: `git show-ref --verify --quiet refs/heads/{target_branch}`
        _, _, retcode_verify_target = run_git_command(['git', 'rev-parse', '--verify', f"{target_branch}^{{commit}}"]) # Check if resolvable to a commit
        if retcode_verify_target != 0:
            print(f"Error: Target branch '{target_branch}' does not exist or is not a valid branch.", file=sys.stderr)
            return
    print(f"Using '{target_branch}' as the base for checking merged branches.")


    # 4. Find branches merged into target_branch
    stdout_merged, stderr_merged, retcode_merged = run_git_command(['git', 'branch', '--merged', target_branch])
    if retcode_merged != 0:
        print(f"Error finding merged branches: {stderr_merged}", file=sys.stderr)
        return

    merged_branches_candidates = []
    for line in stdout_merged.splitlines():
        branch_name = line.lstrip("* ").strip()
        # Filter out the target branch itself, the actual current branch (if not detached), and protected branches
        if branch_name == target_branch: continue
        if actual_current_branch and branch_name == actual_current_branch.split(' ')[-1]: continue # Handle "detached HEAD at X"
        if branch_name in protected_branches: continue
        # Ignore remote branches if any happen to be listed (though --merged usually lists local)
        if branch_name.startswith("remotes/"): continue

        merged_branches_candidates.append(branch_name)

    if not merged_branches_candidates:
        print(f"No local branches found that are merged into '{target_branch}' and not protected.")
        return

    print(f"\n--- Branches merged into '{target_branch}' (candidates for deletion) ---")
    for i, branch in enumerate(merged_branches_candidates):
        print(f"  {i+1}. {branch}")

    if args.dry_run:
        print("\n[Dry Run] No branches will be deleted.")
        print(f"The above {len(merged_branches_candidates)} branch(es) would be targeted for deletion.")
        return

    print("\n--- Confirmation ---")
    try:
        action = input("Enter 'all' to delete all listed, 'none' to cancel, or comma/hyphen-separated indices (e.g., 1,3-5) to delete specific branches: ").strip().lower()
    except EOFError:
        print("\nNo input received. Aborting.", file=sys.stderr)
        return
    except KeyboardInterrupt:
        print("\nUser cancelled. Aborting.", file=sys.stderr)
        return

    branches_to_delete = []
    if action == 'all':
        branches_to_delete = merged_branches_candidates
    elif action == 'none' or not action:
        print("No action taken. Exiting.")
        return
    else: # Parse indices
        try:
            selected_indices = set()
            parts = action.split(',')
            for part in parts:
                part = part.strip()
                if not part: continue
                if '-' in part:
                    start_str, end_str = part.split('-', 1)
                    start, end = int(start_str), int(end_str)
                    if not (1 <= start <= end <= len(merged_branches_candidates)):
                        raise ValueError(f"Range '{part}' out of bounds (1-{len(merged_branches_candidates)}).")
                    selected_indices.update(range(start - 1, end)) # User inputs 1-based
                else:
                    idx = int(part)
                    if not (1 <= idx <= len(merged_branches_candidates)):
                        raise ValueError(f"Index '{part}' out of bounds (1-{len(merged_branches_candidates)}).")
                    selected_indices.add(idx - 1) # User inputs 1-based

            for idx in sorted(list(selected_indices)):
                branches_to_delete.append(merged_branches_candidates[idx])
        except ValueError as e:
            print(f"Invalid input for selection: {e}.", file=sys.stderr)
            return

    if not branches_to_delete:
        print("No branches selected for deletion. Exiting.")
        return

    print(f"\n--- Deleting {len(branches_to_delete)} selected branch(es) ---")
    deleted_count = 0
    failed_deletions = []
    for branch_name in branches_to_delete:
        print(f"Deleting local branch '{branch_name}'... ", end="")
        # Use -d for safety (won't delete unmerged changes). -D would force.
        stdout_del, stderr_del, retcode_del = run_git_command(['git', 'branch', '-d', branch_name])
        if retcode_del == 0:
            # stdout_del often contains "Deleted branch X (was YYY)."
            print(f"Success. ({stdout_del or stderr_del or 'OK'})") # stderr might contain info on successful -d too
            deleted_count += 1
        else:
            print(f"Failed. Git error: {stderr_del or stdout_del or 'Unknown error'}")
            failed_deletions.append(branch_name)

    print(f"\nFinished deleting branches. {deleted_count} branch(es) deleted successfully.")
    if failed_deletions:
        print(f"Failed to delete the following branches: {', '.join(failed_deletions)}")
        print("This might be because they have unmerged changes (use 'git branch -D <branchname>' to force delete) or other issues.")
    return

if __name__ == "__main__":
    main()
