#!/usr/bin/env python3

import platform
import os
import socket
import argparse
import json

psutil_available = False
try:
    import psutil
    psutil_available = True
except ImportError:
    print("Warning: 'psutil' library not found. Some system information (CPU, RAM details) will be unavailable.")
    print("Consider installing it with: pip install psutil")

def get_system_info():
    """Gathers various system information."""
    info = {}

    # OS Information
    info['os_type'] = platform.system()
    info['os_release'] = platform.release()
    info['os_version'] = platform.version()
    info['os_platform'] = platform.platform()

    # Try to get more specific Linux distribution info
    if info['os_type'] == "Linux":
        try:
            # platform.freedesktop_os_release() is Python 3.10+
            # For broader compatibility, try reading /etc/os-release directly
            if hasattr(platform, 'freedesktop_os_release'):
                 info['linux_distribution_details'] = platform.freedesktop_os_release()
            else: # Manual parsing of /etc/os-release
                # This is a simplified parser
                dist_details = {}
                if os.path.exists("/etc/os-release"):
                    with open("/etc/os-release", "r") as f:
                        for line in f:
                            if "=" in line:
                                key, value = line.strip().split("=", 1)
                                dist_details[key] = value.strip('"')
                    info['linux_distribution_details'] = dist_details
                elif os.path.exists("/etc/lsb-release"): # Fallback for older systems
                     with open("/etc/lsb-release", "r") as f:
                        for line in f:
                            if "=" in line:
                                key, value = line.strip().split("=", 1)
                                dist_details[key.replace("DISTRIB_", "")] = value.strip('"') # e.g. DISTRIB_ID -> ID
                    info['linux_distribution_details'] = dist_details


        except Exception as e:
            info['linux_distribution_error'] = str(e)


    # Hostname
    info['hostname'] = socket.gethostname()

    # Architecture
    info['architecture_machine'] = platform.machine()
    info['architecture_bits_linkage'] = platform.architecture() # (bits, linkage)

    # CPU Information
    info['cpu_processor_generic'] = platform.processor() # Generic, might be empty or less specific
    if psutil_available:
        try:
            info['cpu_physical_cores'] = psutil.cpu_count(logical=False)
            info['cpu_logical_cores'] = psutil.cpu_count(logical=True)

            # CPU Frequencies (may require specific permissions or not be available on all systems/VMs)
            # Wrap in try-except as psutil.cpu_freq() can fail
            try:
                cpu_freq = psutil.cpu_freq()
                if cpu_freq: # cpu_freq() can return None
                    info['cpu_frequency_current_mhz'] = cpu_freq.current
                    info['cpu_frequency_min_mhz'] = cpu_freq.min
                    info['cpu_frequency_max_mhz'] = cpu_freq.max
            except Exception as e:
                 info['cpu_frequency_error'] = f"Could not retrieve CPU frequency: {e}"


            # Getting detailed CPU model/brand string is platform-dependent
            # On Linux, /proc/cpuinfo is a common source. psutil doesn't provide a direct cross-platform way.
            if info['os_type'] == "Linux" and os.path.exists("/proc/cpuinfo"):
                with open("/proc/cpuinfo", "r") as f:
                    for line in f:
                        if "model name" in line:
                            info['cpu_model_name'] = line.split(":")[1].strip()
                            break # Take the first one
            elif info['os_type'] == "Darwin": # macOS
                 # Using sysctl on macOS
                try:
                    model_name_bytes = os.popen('sysctl -n machdep.cpu.brand_string').read().strip()
                    info['cpu_model_name'] = model_name_bytes
                except Exception:
                    pass # Fallback to platform.processor() if sysctl fails
            # For Windows, platform.processor() might be the best bet with standard libs/psutil

        except Exception as e:
            info['psutil_cpu_error'] = str(e)
    else:
        info['cpu_info_note'] = "Detailed CPU info requires 'psutil'."

    # RAM Information
    if psutil_available:
        try:
            mem = psutil.virtual_memory()
            info['ram_total_bytes'] = mem.total
            info['ram_available_bytes'] = mem.available
            info['ram_used_bytes'] = mem.used
            info['ram_percent_used'] = mem.percent
            # For human-readable versions
            info['ram_total_human'] = f"{mem.total / (1024**3):.2f} GB"
            info['ram_available_human'] = f"{mem.available / (1024**3):.2f} GB"
        except Exception as e:
            info['psutil_ram_error'] = str(e)
    else:
        info['ram_info_note'] = "Detailed RAM info requires 'psutil'."

    return info

def print_readable_info(info_dict):
    """Prints system information in a human-readable format."""
    print("--- System Information ---")
    for key, value in info_dict.items():
        if isinstance(value, dict): # For nested dicts like linux_distribution_details
            print(f"{key.replace('_', ' ').title()}:")
            for sub_key, sub_value in value.items():
                print(f"  {sub_key.replace('_', ' ').title()}: {sub_value}")
        elif isinstance(value, tuple): # For architecture_bits_linkage
             print(f"{key.replace('_', ' ').title()}: {value[0]} ({value[1]})")
        else:
            print(f"{key.replace('_', ' ').title()}: {value}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Display basic system information.",
        epilog="Example: python sysInfo.py --json"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output information in JSON format."
    )

    args = parser.parse_args()

    system_info_data = get_system_info()

    if args.json:
        # Output as JSON
        try:
            print(json.dumps(system_info_data, indent=4, sort_keys=True))
        except TypeError as e:
            # Handle cases where some data might not be JSON serializable (e.g. complex objects if not careful)
            # For this script, all data added to info dict should be serializable.
            print(f"Error serializing data to JSON: {e}")
            # Fallback to readable print if JSON fails badly
            # print_readable_info(system_info_data)
            return # Exit if JSON output was specifically requested but failed
    else:
        # Output in human-readable format
        print_readable_info(system_info_data)

    if not psutil_available:
        print("\nNote: For more detailed CPU and RAM information, please install the 'psutil' library (pip install psutil).")

    print("\nSystem information process complete.")
