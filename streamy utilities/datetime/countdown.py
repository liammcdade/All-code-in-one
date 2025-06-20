import datetime
import time

def get_target_datetime():
  """Prompts the user for a target date and time and validates it.

  Returns:
    A datetime object representing the target date and time, or None if input is invalid.
  """
  while True:
    datetime_str = input("Enter target date and time (YYYY-MM-DD HH:MM:SS): ")
    try:
      target_dt = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
      if target_dt > datetime.datetime.now():
        return target_dt
      else:
        print("Error: Target date and time must be in the future. Please try again.")
    except ValueError:
      print("Error: Invalid date and time format. Please use YYYY-MM-DD HH:MM:SS. Please try again.")

def countdown(target_dt):
  """Displays a countdown to the target date and time.

  Args:
    target_dt: A datetime object representing the target date and time.
  """
  print("\nStarting countdown...")
  while True:
    now = datetime.datetime.now()
    remaining_time = target_dt - now

    if remaining_time.total_seconds() <= 0:
      print("\nCountdown complete!")
      break

    days = remaining_time.days
    seconds_in_day = remaining_time.seconds
    hours = seconds_in_day // 3600
    minutes = (seconds_in_day % 3600) // 60
    seconds = seconds_in_day % 60

    # Display the remaining time, updating in place
    # \r (carriage return) moves the cursor to the beginning of the line
    print(f"Time remaining: {days} days, {hours:02} hours, {minutes:02} minutes, {seconds:02} seconds", end="\r")

    time.sleep(1) # Wait for one second before updating

if __name__ == "__main__":
  print("--- Countdown Timer ---")
  target_datetime = get_target_datetime()

  if target_datetime:
    countdown(target_datetime)
