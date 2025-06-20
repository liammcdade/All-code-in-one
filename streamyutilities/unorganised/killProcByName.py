#!/usr/bin/env python3

import psutil
import argparse
import os
import sys
import signal  # For signal names, though psutil handles actual sending


def find_processes_by_name(name_pattern, case_sensitive=False):
    """
    Finds running processes that match the given name pattern in their name or command line.
    Returns a list of psutil.Process objects.
    """
    matched_processes = []
    search_term = name_pattern if case_sensitive else name_pattern.lower()

    # Attributes to fetch for each process. Fetching them here can be more efficient.
    attrs = ["pid", "name", "username", "cmdline", "status"]
    if os.name == "nt":  # 'username' might require admin on Windows for some processes
        pass  # psutil handles this gracefully, username might be None

    for proc in psutil.process_iter(
        attrs=attrs, ad_value=None
    ):  # ad_value=None to skip on AccessDenied
        if proc.info["pid"] == 0:  # Skip system idle process / system process
            continue

        # proc.info might have None for some attrs if process vanished or AccessDenied
        proc_name = proc.info.get("name", "") or ""
        proc_cmdline_list = proc.info.get("cmdline", []) or []
        proc_cmdline_str = " ".join(proc_cmdline_list)

        # Determine if there's a match
        match_found = False
        if case_sensitive:
            if search_term in proc_name or search_term in proc_cmdline_str:
                match_found = True
        else:
            if (
                search_term in proc_name.lower()
                or search_term in proc_cmdline_str.lower()
            ):
                match_found = True

        if match_found:
            # Check if process is actually running (not zombie, etc.)
            # Although, user might want to target zombies specifically with SIGKILL
            # For now, list them if they match by name/cmdline. psutil can handle sending signals to them.
            # if proc.info.get('status') == psutil.STATUS_ZOMBIE and not force_kill_signal:
            #     print(f"Info: Process {proc.info['pid']} ({proc_name}) is a zombie. SIGTERM might not work. Consider --force.", file=sys.stderr)
            matched_processes.append(proc)

    return matched_processes


def kill_process(proc, use_sigkill=False):
    """Attempts to terminate or kill a single psutil.Process object."""
    pid = proc.pid
    name = proc.name()  # Get fresh name, info cache might be old
    signal_to_use = "SIGKILL" if use_sigkill else "SIGTERM"
    try:
        print(f"Attempting to send {signal_to_use} to PID {pid} ({name})... ", end="")
        if use_sigkill:
            proc.kill()
        else:
            proc.terminate()
        # No error means signal was sent. Check if it's gone after a short delay?
        # For simplicity, assume sent is good enough for this tool.
        print("Signal sent.")
        return True
    except psutil.NoSuchProcess:
        print(f"Process PID {pid} ({name}) no longer exists.")
        return False  # Already gone
    except psutil.AccessDenied:
        print(
            f"Access denied to send signal to PID {pid} ({name}). Try with higher privileges."
        )
        return False
    except Exception as e:
        print(f"Failed to send signal to PID {pid} ({name}): {e}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Find and kill processes by name. Use with extreme caution.",
        epilog='Example: python killProcByName.py "my_script" --dry-run --case-sensitive',
    )
    parser.add_argument(
        "process_name_pattern",
        help="Name or part of the name/command line of the process(es) to find.",
    )
    parser.add_argument(
        "--case-sensitive",
        action="store_true",
        help="Perform a case-sensitive search. Default is case-insensitive.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List processes that would be targeted, but do not send any signals.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force kill the process(es) using SIGKILL. Default is SIGTERM (terminate gracefully).",
    )
    # Placeholder for future --signal option:
    # parser.add_argument("--signal", default="TERM", help="Signal to send (e.g., TERM, KILL, HUP). Default: TERM")

    args = parser.parse_args()

    print("--- Process Killer Utility ---")
    print("WARNING: Killing processes can lead to data loss or system instability.")
    print("Ensure you know what you are targeting.\n")

    if not args.process_name_pattern:
        print("Error: Process name pattern cannot be empty.", file=sys.stderr)
        sys.exit(1)

    print(
        f"Searching for processes matching: '{args.process_name_pattern}' (Case sensitive: {args.case_sensitive})"
    )

    try:
        matched_procs = find_processes_by_name(
            args.process_name_pattern, args.case_sensitive
        )
    except Exception as e:
        print(f"Error during process search: {e}", file=sys.stderr)
        sys.exit(1)

    if not matched_procs:
        print("No running processes found matching the criteria.")
        sys.exit(0)

    print("\n--- Matched Processes ---")
    for i, proc in enumerate(matched_procs):
        try:
            cmdline = " ".join(proc.info.get("cmdline", []) or [])  # Use cached info
            username = proc.info.get("username", "N/A")
            status = proc.info.get("status", "N/A")
            print(
                f"  {i+1}. PID: {proc.pid:<6} User: {username:<15} Status: {status:<10} Name: {proc.info.get('name', 'N/A'):<20} Cmd: {cmdline[:60]}{'...' if len(cmdline)>60 else ''}"
            )
        except psutil.NoSuchProcess:  # Process might have ended since initial listing
            print(
                f"  {i+1}. PID: {proc.pid:<6} (Process ended before details could be fully retrieved)"
            )
        except psutil.AccessDenied:
            print(
                f"  {i+1}. PID: {proc.pid:<6} (Access denied to full details for this process)"
            )

    if args.dry_run:
        print("\n[Dry Run] No signals will be sent.")
        print(
            f"The above {len(matched_procs)} process(es) would be targeted for {'SIGKILL' if args.force else 'SIGTERM' }."
        )
        return

    print("\n--- Confirmation ---")
    try:
        # Input like: "all", "none", "1", "1,3", "1-3,5"
        action = (
            input(
                "Enter 'all' to target all, 'none' to cancel, or comma/hyphen-separated indices (e.g., 1,3-5) to target specific processes: "
            )
            .strip()
            .lower()
        )
    except EOFError:
        print("\nNo input received. Aborting.", file=sys.stderr)
        return
    except KeyboardInterrupt:
        print("\nUser cancelled. Aborting.", file=sys.stderr)
        return

    procs_to_kill = []
    if action == "all":
        procs_to_kill = matched_procs
    elif action == "none" or not action:
        print("No action taken. Exiting.")
        return
    else:  # Parse indices
        try:
            selected_indices = set()
            parts = action.split(",")
            for part in parts:
                part = part.strip()
                if not part:
                    continue
                if "-" in part:
                    start, end = map(int, part.split("-", 1))
                    if not (1 <= start <= end <= len(matched_procs)):
                        raise ValueError(f"Range '{part}' out of bounds.")
                    selected_indices.update(
                        range(start - 1, end)
                    )  # User inputs 1-based
                else:
                    idx = int(part)
                    if not (1 <= idx <= len(matched_procs)):
                        raise ValueError(f"Index '{part}' out of bounds.")
                    selected_indices.add(idx - 1)  # User inputs 1-based

            for idx in sorted(list(selected_indices)):
                procs_to_kill.append(matched_procs[idx])
        except ValueError as e:
            print(
                f"Invalid input for selection: {e}. Please use numbers corresponding to the list.",
                file=sys.stderr,
            )
            return

    if not procs_to_kill:
        print("No processes selected for action. Exiting.")
        return

    print(
        f"\n--- Attempting to send {'SIGKILL' if args.force else 'SIGTERM'} to {len(procs_to_kill)} selected process(es) ---"
    )
    killed_count = 0
    for proc_obj in procs_to_kill:
        # Re-check if process still exists and is the one we think it is, to be safer
        # However, psutil.Process objects are bound to a PID. If PID is reused, it's a different process.
        # proc_obj.is_running() and checking name again could be an option but adds complexity.
        # kill_process already handles NoSuchProcess.
        if kill_process(proc_obj, args.force):
            killed_count += (
                1  # Count successful signal sends, not necessarily successful kills
            )

    print(
        f"\nFinished sending signals. {killed_count} signal(s) were sent successfully."
    )
    print(
        "Note: 'Signal sent' does not guarantee the process terminated, especially for SIGTERM."
    )
    print(
        "You may need to re-run the search or use system tools to verify termination."
    )
    sys.exit(0)
