#!/usr/bin/env python3

import time
import argparse
import sys

# Default durations in minutes
DEFAULT_WORK_MINS = 25
DEFAULT_SHORT_BREAK_MINS = 5
DEFAULT_LONG_BREAK_MINS = 15
DEFAULT_SESSIONS_BEFORE_LONG_BREAK = 4

TERMINAL_BELL = "\a" # ASCII Bell character

def display_time(remaining_seconds, session_type_str):
    """Displays time in MM:SS format, updating the current line."""
    mins, secs = divmod(remaining_seconds, 60)
    time_str = f"{session_type_str}: {int(mins):02d}:{int(secs):02d}"
    # Use carriage return to overwrite the line. Add spaces to clear previous, longer lines.
    sys.stdout.write(f"\r{time_str}          ")
    sys.stdout.flush()

def play_notification(message_before_sound=""):
    """Prints a message and attempts to play a terminal bell sound."""
    if message_before_sound:
        # Ensure message is on a new line, not overwriting the timer
        sys.stdout.write("\r" + " " * 80 + "\r") # Clear the timer line
        print(message_before_sound)

    sys.stdout.write(TERMINAL_BELL)
    sys.stdout.flush()


def run_timer_session(duration_seconds, session_name_str):
    """Runs a single timer session for the given duration (in seconds)."""
    print(f"\nStarting '{session_name_str}' session for {int(duration_seconds // 60)} minutes.")

    for i in range(int(duration_seconds), -1, -1):
        display_time(i, session_name_str)
        time.sleep(1)

    # Ensure the final display is 00:00 and then clear it for the notification
    display_time(0, session_name_str)
    sys.stdout.write("\r" + " " * 80 + "\r") # Clear the timer line
    sys.stdout.flush()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A simple command-line Pomodoro timer.",
        epilog="Example: python pomodoroTimer.py --work 20 --short-break 4 --long-break 20 --sessions 3"
    )
    parser.add_argument(
        "--work",
        type=int,
        default=DEFAULT_WORK_MINS,
        metavar="MINUTES",
        help=f"Duration of a work session in minutes. Default: {DEFAULT_WORK_MINS} min."
    )
    parser.add_argument(
        "--short-break",
        type=int,
        default=DEFAULT_SHORT_BREAK_MINS,
        metavar="MINUTES",
        help=f"Duration of a short break in minutes. Default: {DEFAULT_SHORT_BREAK_MINS} min."
    )
    parser.add_argument(
        "--long-break",
        type=int,
        default=DEFAULT_LONG_BREAK_MINS,
        metavar="MINUTES",
        help=f"Duration of a long break in minutes. Default: {DEFAULT_LONG_BREAK_MINS} min."
    )
    parser.add_argument(
        "--sessions",
        type=int,
        default=DEFAULT_SESSIONS_BEFORE_LONG_BREAK,
        metavar="COUNT",
        help=f"Number of work sessions before a long break. Default: {DEFAULT_SESSIONS_BEFORE_LONG_BREAK}."
    )

    args = parser.parse_args()

    # Validate inputs
    if any(arg_val <= 0 for arg_val in [args.work, args.short_break, args.long_break, args.sessions]):
        print("Error: All duration and session count arguments must be positive integers.", file=sys.stderr)
        sys.exit(1)

    work_duration_sec = args.work * 60
    short_break_sec = args.short_break * 60
    long_break_sec = args.long_break * 60
    sessions_for_long_break = args.sessions

    print("--- Pomodoro Timer Started ---")
    print(f"Work: {args.work} min | Short Break: {args.short_break} min | Long Break: {args.long_break} min | Sessions for Long Break: {sessions_for_long_break}")
    print("Press Ctrl+C to exit at any time.")

    work_session_counter = 0
    try:
        while True:
            work_session_counter += 1
            session_label = f"Work Session {work_session_counter}"

            # Work session
            run_timer_session(work_duration_sec, session_label)
            play_notification(f"Work session {work_session_counter} finished! Time for a break.")

            # Break session
            if work_session_counter > 0 and work_session_counter % sessions_for_long_break == 0:
                run_timer_session(long_break_sec, "Long Break")
                play_notification("Long break finished! Time for the next work session.")
            else:
                run_timer_session(short_break_sec, "Short Break")
                play_notification("Short break finished! Time for the next work session.")

    except KeyboardInterrupt:
        print("\nPomodoro timer interrupted by user. Exiting.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}", file=sys.stderr)
    finally:
        # Ensure cursor is on a new line and visible if it was hidden or manipulated
        sys.stdout.write("\r" + " " * 80 + "\r") # Clear any leftover timer line
        print("Pomodoro timer stopped.")
        sys.exit(0)
