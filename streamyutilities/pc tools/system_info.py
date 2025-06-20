"""
Displays detailed system information including CPU, memory, disk, network, and boot time.

This script requires the psutil library. Install it using:
    pip install psutil

Usage:
    python system_info.py
"""

import psutil
import datetime
import time  # For psutil.cpu_percent interval


def bytes_to_human_readable(n_bytes):
    """Converts bytes to a human-readable string (KB, MB, GB, TB)."""
    symbols = ("K", "M", "G", "T", "P", "E", "Z", "Y")
    prefix = {s: 1 << (i + 1) * 10 for i, s in enumerate(symbols)}
    for s in reversed(symbols):
        if n_bytes >= prefix[s]:
            value = float(n_bytes) / prefix[s]
            return f"{value:.2f} {s}B"
    return f"{n_bytes} B"


def print_section_header(title):
    """Prints a formatted section header."""
    print("\n" + "=" * 40)
    print(f"{title:^40}")
    print("=" * 40)


def get_cpu_info():
    """Gathers and displays CPU information."""
    print_section_header("CPU Information")
    # Overall CPU usage
    # The interval is important for accuracy; 0.1 to 1 second is typical.
    overall_usage = psutil.cpu_percent(interval=1)
    print(f"Overall CPU Usage: {overall_usage}%")

    # Per-CPU usage
    per_cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
    if per_cpu_usage:  # Check if percpu data is available
        print("Per-CPU Usage:")
        for i, usage in enumerate(per_cpu_usage):
            print(f"  CPU {i}: {usage}%")
    else:
        print("Per-CPU usage information not available.")

    print(f"Logical CPUs: {psutil.cpu_count(logical=True)}")
    print(f"Physical CPUs (cores): {psutil.cpu_count(logical=False)}")

    try:
        cpu_freq = psutil.cpu_freq()
        if cpu_freq:
            print(f"CPU Frequency (Current): {cpu_freq.current:.2f} MHz")
            if hasattr(cpu_freq, "min") and cpu_freq.min > 0:
                print(f"CPU Frequency (Min): {cpu_freq.min:.2f} MHz")
            if hasattr(cpu_freq, "max") and cpu_freq.max > 0:
                print(f"CPU Frequency (Max): {cpu_freq.max:.2f} MHz")
    except NotImplementedError:
        print("CPU frequency information not available on this system.")


def get_memory_info():
    """Gathers and displays memory (RAM) information."""
    print_section_header("Memory Information (RAM)")
    mem = psutil.virtual_memory()
    print(f"Total Memory: {bytes_to_human_readable(mem.total)}")
    print(f"Available Memory: {bytes_to_human_readable(mem.available)}")
    print(f"Used Memory: {bytes_to_human_readable(mem.used)}")
    print(f"Memory Usage Percentage: {mem.percent}%")

    # Swap memory details (if available)
    try:
        swap = psutil.swap_memory()
        print("\nSwap Memory:")
        print(f"  Total Swap: {bytes_to_human_readable(swap.total)}")
        print(f"  Used Swap: {bytes_to_human_readable(swap.used)}")
        print(f"  Free Swap: {bytes_to_human_readable(swap.free)}")
        print(f"  Swap Usage Percentage: {swap.percent}%")
    except (
        psutil.Error
    ) as e:  # psutil.Error can be base for specific errors like "no swap"
        print(f"\nSwap Memory: Not available or error accessing: {e}")


def get_disk_info():
    """Gathers and displays disk space information for all major partitions."""
    print_section_header("Disk Space Information")
    partitions = psutil.disk_partitions()
    for partition in partitions:
        # Filter out some less relevant mountpoints if desired, e.g., snap packages
        # if 'snap' in partition.mountpoint or 'loop' in partition.device:
        #     continue
        print(f"\nPartition: {partition.device}")
        print(f"  Mountpoint: {partition.mountpoint}")
        print(f"  File System Type: {partition.fstype}")
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            print(f"  Total Space: {bytes_to_human_readable(usage.total)}")
            print(f"  Used Space: {bytes_to_human_readable(usage.used)}")
            print(f"  Free Space: {bytes_to_human_readable(usage.free)}")
            print(f"  Usage Percentage: {usage.percent}%")
        except PermissionError:
            print(
                f"  Could not retrieve usage for {partition.mountpoint} due to permissions."
            )
        except Exception as e:
            print(f"  Error retrieving usage for {partition.mountpoint}: {e}")


def get_network_info():
    """Gathers and displays network I/O statistics."""
    print_section_header("Network I/O Statistics")
    # Get I/O counters for all network interfaces
    net_io_counters = psutil.net_io_counters(pernic=True)
    if not net_io_counters:
        print("No network interfaces found or statistics unavailable.")
        return

    for interface, stats in net_io_counters.items():
        print(f"\nInterface: {interface}")
        print(f"  Bytes Sent: {bytes_to_human_readable(stats.bytes_sent)}")
        print(f"  Bytes Received: {bytes_to_human_readable(stats.bytes_recv)}")
        print(f"  Packets Sent: {stats.packets_sent}")
        print(f"  Packets Received: {stats.packets_recv}")
        if hasattr(stats, "errin"):  # Some systems might not have all attributes
            print(f"  Incoming Errors: {stats.errin}")
        if hasattr(stats, "errout"):
            print(f"  Outgoing Errors: {stats.errout}")
        if hasattr(stats, "dropin"):
            print(f"  Incoming Packets Dropped: {stats.dropin}")
        if hasattr(stats, "dropout"):
            print(f"  Outgoing Packets Dropped: {stats.dropout}")


def get_boot_time():
    """Gathers and displays system boot time."""
    print_section_header("System Boot Time")
    try:
        boot_timestamp = psutil.boot_time()
        boot_dt = datetime.datetime.fromtimestamp(boot_timestamp)
        print(f"Boot Time: {boot_dt.strftime('%Y-%m-%d %H:%M:%S')}")

        # Uptime calculation
        uptime_seconds = time.time() - boot_timestamp
        uptime_str = str(datetime.timedelta(seconds=int(uptime_seconds)))
        print(f"System Uptime: {uptime_str}")

    except Exception as e:
        print(f"Could not retrieve boot time: {e}")


def main():
    """Main function to call all info gathering functions."""
    print("Gathering system information...")

    get_cpu_info()
    get_memory_info()
    get_disk_info()
    get_network_info()
    get_boot_time()

    print("\n" + "=" * 40)
    print("System information gathering complete.")
    print("=" * 40)


if __name__ == "__main__":
    main()
