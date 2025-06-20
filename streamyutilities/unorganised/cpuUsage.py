#!/usr/bin/env python3

import psutil
import time
import argparse
import sys

DEFAULT_INTERVAL = 1.0  # seconds
DEFAULT_COUNT = 0       # 0 means run indefinitely

def create_bar(percentage, length=20):
    """Creates a simple character-based progress bar."""
    filled_length = int(length * percentage // 100)
    bar = '█' * filled_length + '-' * (length - filled_length)
    return f"[{bar}] {percentage:.1f}%"

def display_cpu_info(overall_usage, per_cpu_usages=None):
    """Displays CPU usage information."""
    print(f"Overall CPU Usage: {create_bar(overall_usage)}")
    if per_cpu_usages:
        print("Per-CPU Usage:")
        for i, usage in enumerate(per_cpu_usages):
            print(f"  CPU {i}: {create_bar(usage)}")
    print("-" * 30) # Separator

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Display current CPU utilization.",
        epilog="Example: python cpuUsage.py --interval 0.5 --count 10 --per-cpu"
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=DEFAULT_INTERVAL,
        help=f"Time interval in seconds between updates. Default: {DEFAULT_INTERVAL}s."
    )
    parser.add_argument(
        "--count",
        type=int,
        default=DEFAULT_COUNT,
        help="Number of updates to display. Default: 0 (run indefinitely until Ctrl+C)."
    )
    parser.add_argument(
        "--per-cpu",
        action="store_true",
        help="Display per-CPU utilization in addition to overall usage."
    )

    args = parser.parse_args()

    if args.interval <= 0:
        print("Error: Interval must be a positive number.", file=sys.stderr)
        sys.exit(1)
    if args.count < 0:
        print("Error: Count must be a non-negative number.", file=sys.stderr)
        sys.exit(1)

    print(f"Starting CPU usage monitoring (Interval: {args.interval}s, Count: {'Infinite' if args.count == 0 else args.count}).")
    print("Press Ctrl+C to stop.")
    print("Note: The first reading for overall CPU usage might be 0.0% as psutil establishes a baseline.")

    updates_done = 0
    try:
        # Call cpu_percent once before the loop without an interval to establish initial timings for 'percpu'
        # if per_cpu is True. This helps make the first percpu reading in the loop more accurate.
        if args.per_cpu:
            psutil.cpu_percent(interval=None, percpu=True)
            # A small sleep might be useful if interval is very small, to ensure distinct readings
            if args.interval < 0.2: # Arbitrary small interval threshold
                time.sleep(0.05)


        while True:
            if args.count != 0 and updates_done >= args.count:
                break # Reached desired number of updates

            # Get overall CPU utilization. This call will block for args.interval seconds.
            # The first time it's called with an interval, it returns 0.0 (or a meaningless value)
            # and sets up the baseline for the next call.
            overall_usage = psutil.cpu_percent(interval=args.interval, percpu=False)

            per_cpu_list = None
            if args.per_cpu:
                # Get the per-CPU utilization since the last call to percpu=True (or system boot).
                # This is a non-blocking call if interval=None.
                per_cpu_list = psutil.cpu_percent(interval=None, percpu=True)

            if overall_usage is None : # Should ideally not happen if psutil is working
                print("Warning: Could not retrieve overall CPU usage for this interval.", file=sys.stderr)
                # We still completed an "interval" due to the overall_usage call, so count it.

            # If overall_usage is None, display_cpu_info will handle it or we can skip.
            # For now, let's display even if overall is None, as per_cpu might be valid.
            # Or, if overall_usage is critical, treat as an error for that tick.
            # The create_bar function expects a float, so None would be an issue.
            # Let's ensure overall_usage is a float for display_cpu_info
            if overall_usage is None: # If psutil call actually returns None
                print("Overall CPU usage measurement failed for this interval.", file=sys.stderr)
                # Skip this update display or show placeholders? For now, skip display.
                updates_done += 1
                if args.count != 0 and updates_done >= args.count: # check again in case this was the last
                    break
                # If in infinite mode, and overall_usage failed, we need to manually pause
                # because the blocking call might not have blocked as expected (e.g. if it returned None quickly)
                # However, psutil.cpu_percent(interval=X) should always block for X seconds.
                # If it returns None, it's an issue with psutil/system, but it should have blocked.
                continue


            display_cpu_info(overall_usage, per_cpu_list)
            updates_done += 1

            # No explicit time.sleep() needed here because psutil.cpu_percent(interval=args.interval) is blocking.


            # The first call to cpu_percent with interval > 0 returns 0.0 and is meant to be ignored.
            # If this is the first iteration AND args.count is specified (not infinite),
            # and we want N *meaningful* updates, we might need to handle this.
            # A simple way: if updates_done == 0 and args.count == 1, this first 0.0 is the only output.
            # Alternative: run an extra iteration if count > 0.
            # For now, just print what psutil gives. Users familiar with psutil will understand the first 0.0.

            display_cpu_info(overall_usage, per_cpu_list)
            updates_done += 1

            # No explicit time.sleep() needed here if psutil.cpu_percent has interval set,
            # as it's a blocking call. If interval=None was used for overall_usage, then sleep here.
            # Since overall_usage uses args.interval, it blocks.

    except KeyboardInterrupt:
        print("\nMonitoring stopped by user (Ctrl+C).")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}", file=sys.stderr)
    finally:
        print("Exiting CPU usage monitor.")
        return
