#!/usr/bin/env python3

import psutil
import datetime
import argparse
import sys
import time # Not strictly needed if using datetime.timedelta directly

def format_uptime_seconds(total_seconds):
    """
    Converts total seconds into a human-readable string:
    "X day(s), Y hour(s), Z minute(s), W second(s)".
    Skips zero components except for seconds if total uptime is very short.
    """
    if total_seconds < 0:
        return "Uptime calculation error (negative duration)"

    days = int(total_seconds // (24 * 3600))
    total_seconds %= (24 * 3600)
    hours = int(total_seconds // 3600)
    total_seconds %= 3600
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)

    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")

    # Always show seconds, even if other parts are zero (e.g., "0 seconds" if uptime is <1s but >0)
    # or if uptime is exactly 0 seconds (e.g. very fast script run right at boot, though unlikely)
    # A more common case: "1 minute, 0 seconds" or just "1 minute".
    # Let's show seconds if it's the only component or if other components exist.
    if seconds > 0 or not parts: # if parts is empty, means uptime < 1 minute
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")

    if not parts: # Should ideally not happen if seconds are always appended if parts is empty
        return "System just booted or uptime is less than 1 second."

    return ", ".join(parts)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Display system uptime or boot time.",
        epilog="Example: python uptime.py --boot-time"
    )
    parser.add_argument(
        "--boot-time",
        action="store_true",
        help="Display the exact system boot time instead of uptime duration."
    )

    args = parser.parse_args()

    try:
        boot_timestamp = psutil.boot_time()
        boot_datetime = datetime.datetime.fromtimestamp(boot_timestamp)

        if args.boot_time:
            # Display boot time
            print(f"System Boot Time: {boot_datetime.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        else:
            # Display uptime duration
            current_time_dt = datetime.datetime.now()
            uptime_timedelta = current_time_dt - boot_datetime

            # uptime_seconds = uptime_timedelta.total_seconds() # Get total seconds as float
            # For more precision, especially if system clock changed, get current time's timestamp
            # and subtract boot_timestamp. psutil.boot_time() is usually stable.
            # The timedelta calculation is generally fine and idiomatic.
            uptime_seconds_float = uptime_timedelta.total_seconds()


            print(f"System Uptime: {format_uptime_seconds(uptime_seconds_float)}")

    except psutil.Error as e:
        print(f"Error accessing boot time via psutil: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

    sys.exit(0)
