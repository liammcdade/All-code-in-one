#!/usr/bin/env python3

import psutil
import time
import argparse
import sys

DEFAULT_INTERVAL = 1.0  # seconds
DEFAULT_COUNT = 0       # 0 means run indefinitely

def bytes_to_human_readable(n_bytes):
    """Converts bytes to a human-readable string (KB, MB, GB, TB)."""
    if n_bytes == 0:
        return "0B"
    # Using 1024 for KiB, MiB, GiB, etc. which is common in memory reporting
    size_name = ("B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB")
    i = 0
    # Iterate until n_bytes is less than 1024 or we run out of units
    while n_bytes >= 1024 and i < len(size_name) - 1:
        n_bytes /= 1024.0
        i += 1
    return f"{n_bytes:.2f}{size_name[i]}"

def display_memory_usage(virtual_mem_stats, swap_mem_stats=None):
    """Displays memory usage information in a readable format."""
    print("--- RAM Usage ---")
    print(f"  Total:     {bytes_to_human_readable(virtual_mem_stats.total):>10}")
    print(f"  Available: {bytes_to_human_readable(virtual_mem_stats.available):>10}")
    print(f"  Used:      {bytes_to_human_readable(virtual_mem_stats.used):>10}")
    print(f"  Percent:   {virtual_mem_stats.percent:.1f}%")

    if swap_mem_stats:
        print("--- Swap Usage ---")
        print(f"  Total:     {bytes_to_human_readable(swap_mem_stats.total):>10}")
        print(f"  Used:      {bytes_to_human_readable(swap_mem_stats.used):>10}")
        print(f"  Free:      {bytes_to_human_readable(swap_mem_stats.free):>10}") # psutil uses 'free' for swap
        print(f"  Percent:   {swap_mem_stats.percent:.1f}%")

    print("-" * 30) # Separator


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Display current system memory (RAM and Swap) utilization.",
        epilog="Example: python memUsage.py --interval 5 --count 12 --swap"
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
        "--swap",
        action="store_true",
        help="Include swap memory usage in the display."
    )

    args = parser.parse_args()

    if args.interval <= 0:
        print("Error: Interval must be a positive number.", file=sys.stderr)
        sys.exit(1)
    if args.count < 0:
        print("Error: Count must be a non-negative number.", file=sys.stderr)
        sys.exit(1)

    print(f"Starting memory usage monitoring (Interval: {args.interval}s, Count: {'Infinite' if args.count == 0 else args.count}).")
    print("Press Ctrl+C to stop.")

    updates_done = 0
    try:
        # Initial check to ensure psutil calls work before entering loop
        _ = psutil.virtual_memory()
        if args.swap:
            _ = psutil.swap_memory()

        while True:
            if args.count != 0 and updates_done >= args.count:
                break # Reached desired number of updates

            vmem = psutil.virtual_memory()
            smem = psutil.swap_memory() if args.swap else None

            # Clear previous output (simple way, works better in typical terminals)
            # For more complex UIs, libraries like 'curses' would be used.
            # This basic clear might not be perfect in all terminal emulators or if output is very long.
            # A simple approach is just to print fresh lines each time.
            # If interval is long, clearing is less of an issue.
            # For rapid updates, it can be messy. Let's just print fresh for now.
            # os.system('cls' if os.name == 'nt' else 'clear') # Avoid for script portability/safety

            display_memory_usage(vmem, smem)
            updates_done += 1

            if args.count != 0 and updates_done >= args.count: # Check again in case this was the last one
                break

            # Sleep for the specified interval before the next update
            # (unless it was the very last update in a counted loop)
            if args.count == 0 or updates_done < args.count:
                 time.sleep(args.interval)

    except KeyboardInterrupt:
        print("\nMonitoring stopped by user (Ctrl+C).")
    except psutil.Error as e: # Catch psutil specific errors
        print(f"\nA psutil error occurred: {e}", file=sys.stderr)
        print("Please ensure psutil is installed correctly and you have necessary permissions.", file=sys.stderr)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}", file=sys.stderr)
    finally:
        print("Exiting memory usage monitor.")
        sys.exit(0)
