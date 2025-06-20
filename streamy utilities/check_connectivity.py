"""
Checks network connectivity to one or more hosts using the system's ping command.

Usage:
    python check_connectivity.py <host1> [<host2> ...] [--count <number_of_pings>]

Arguments:
    host:             One or more hostnames or IP addresses to check.
    --count N, -c N:  Number of ping packets to send to each host. Default is 3.

Examples:
    python check_connectivity.py google.com 8.8.8.8
    python check_connectivity.py my-internal-server --count 5
"""

import argparse
import subprocess
import platform
import re

def check_host_connectivity(host, count=3):
    """
    Performs a ping operation to the specified host.

    Args:
        host (str): The hostname or IP address to ping.
        count (int): The number of ping packets to send.

    Returns:
        tuple: (is_reachable, summary_string)
               is_reachable (bool): True if the host is reachable, False otherwise.
               summary_string (str): A string containing details from the ping output.
    """
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, str(count), host]

    is_reachable = False
    summary_lines = []

    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate(timeout=count * 2 + 5) # Timeout based on count

        if process.returncode == 0:
            is_reachable = True
            summary_lines.append(f"Host {host} is reachable.")
        else:
            summary_lines.append(f"Host {host} is NOT reachable (return code: {process.returncode}).")

        # Attempt to parse statistics (platform-dependent)
        # This is a basic parsing attempt and might need refinement for different OS languages/ping versions
        if stdout:
            summary_lines.append("\n--- Ping Output ---")
            summary_lines.append(stdout.strip())

            # Extract packet loss and rtt (example for common English output)
            packets_transmitted, packets_received, packet_loss_percent = None, None, None
            rtt_min, rtt_avg, rtt_max, rtt_mdev = None, None, None, None

            if platform.system().lower() == 'windows':
                loss_match = re.search(r"Lost = (\d+) \((\d+)% loss\)", stdout)
                if loss_match:
                    packets_lost = int(loss_match.group(1))
                    packet_loss_percent = int(loss_match.group(2))
                    # Windows ping doesn't always show transmitted, but implies it from count
                    packets_transmitted = count
                    packets_received = count - packets_lost

                rtt_match = re.search(r"Minimum = (\d+)ms, Maximum = (\d+)ms, Average = (\d+)ms", stdout)
                if rtt_match:
                    rtt_min = float(rtt_match.group(1))
                    rtt_max = float(rtt_match.group(2))
                    rtt_avg = float(rtt_match.group(3))
            else: # Linux/macOS-like
                loss_match = re.search(r"(\d+) packets transmitted, (\d+) received, (?:[\d\.]+% packet loss|(\d+)% packet loss)", stdout) # Handles variations
                if loss_match:
                    packets_transmitted = int(loss_match.group(1))
                    packets_received = int(loss_match.group(2))
                    if loss_match.group(3): # If the third group (percentage) is captured directly
                         packet_loss_percent = int(loss_match.group(3))
                    elif packets_transmitted > 0 :
                        packet_loss_percent = ((packets_transmitted - packets_received) / packets_transmitted) * 100

                rtt_match = re.search(r"rtt min/avg/max/(?:mdev|stddev) = ([\d\.]+)/([\d\.]+)/([\d\.]+)/([\d\.]+) ms", stdout)
                if rtt_match:
                    rtt_min = float(rtt_match.group(1))
                    rtt_avg = float(rtt_match.group(2))
                    rtt_max = float(rtt_match.group(3))
                    rtt_mdev = float(rtt_match.group(4))

            if packets_transmitted is not None:
                summary_lines.insert(1, f"  Packets: Transmitted={packets_transmitted}, Received={packets_received}, Loss={packet_loss_percent:.1f}%")
            if rtt_avg is not None:
                 summary_lines.insert(2, f"  RTT (ms): Min={rtt_min}, Avg={rtt_avg}, Max={rtt_max}" + (f", Mdev={rtt_mdev}" if rtt_mdev else ""))


        if stderr:
            summary_lines.append("\n--- Errors (stderr) ---")
            summary_lines.append(stderr.strip())
            if "not found" in stderr.lower() or "not recognized" in stderr.lower():
                 summary_lines.append("  Error: 'ping' command not found. Please ensure it is installed and in your system's PATH.")

    except subprocess.TimeoutExpired:
        summary_lines.append(f"Host {host} check timed out after {count * 2 + 5} seconds.")
        summary_lines.append("  This usually means the host is unreachable or there's a severe network delay.")
        is_reachable = False # Explicitly set
    except FileNotFoundError:
        summary_lines.insert(0, f"Host {host}: ERROR - 'ping' command not found.")
        summary_lines.append("  Please ensure the 'ping' utility is installed and in your system's PATH.")
    except Exception as e:
        summary_lines.insert(0, f"Host {host}: An unexpected error occurred: {e}")

    return is_reachable, "\n".join(summary_lines)

def main():
    parser = argparse.ArgumentParser(
        description="Checks network connectivity to hosts using ping.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("hosts", nargs='+', help="One or more hostnames or IP addresses to check.")
    parser.add_argument(
        "--count", "-c",
        type=int,
        default=3,
        help="Number of ping packets to send to each host. Default is 3."
    )

    args = parser.parse_args()

    if args.count <= 0:
        print("Error: Ping count must be a positive integer.")
        return

    print(f"Starting connectivity check (sending {args.count} pings per host)...\n")

    all_reachable = True
    for host_to_check in args.hosts:
        print(f"--- Checking {host_to_check} ---")
        reachable, summary = check_host_connectivity(host_to_check, args.count)
        print(summary)
        if not reachable:
            all_reachable = False
        print("-" * (len(host_to_check) + 18)) # Print separator
        print() # Extra newline for readability

    print("\n--- Overall Summary ---")
    if all_reachable:
        print("All specified hosts were reachable.")
    else:
        print("At least one host was not reachable or an error occurred.")

if __name__ == "__main__":
    main()
