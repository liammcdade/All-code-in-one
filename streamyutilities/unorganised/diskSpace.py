#!/usr/bin/env python3

import psutil
import argparse
import os
import sys


def bytes_to_human_readable(n_bytes, suffix="B", precision=1):
    """Converts bytes to a human-readable string (KB, MB, GB, TB)."""
    if n_bytes is None:
        return "N/A"
    # Using 1000 for disk space (decimal) as per `df -h` (power of 10)
    # or 1024 for binary (KiB, MiB). Let's use 1024 for consistency with memory utils.
    # `df -H` uses 1000, `df -h` uses 1024. psutil returns raw bytes.
    # Common utilities often use 1024 (binary prefixes).
    factor = 1024
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(n_bytes) < factor:
            return f"{n_bytes:.{precision}f}{unit}{suffix}"
        n_bytes /= factor
    return f"{n_bytes:.{precision}f}Yi{suffix}"


def get_inode_usage(mountpoint):
    """Gets inode usage for a given mountpoint on POSIX systems."""
    if hasattr(os, "statvfs"):  # POSIX specific
        try:
            stats = os.statvfs(mountpoint)
            total_inodes = stats.f_files
            free_inodes = stats.f_ffree  # Free inodes for non-superuser
            # used_inodes = total_inodes - free_inodes # This can be different from total - f_favail
            # Let's use f_favail for available to user, f_ffree for true free
            used_inodes = (
                total_inodes - stats.f_bfree
                if total_inodes >= stats.f_bfree
                else total_inodes - free_inodes
            )  # A common way to calculate used
            # A more direct way based on how df does it:
            used_inodes = total_inodes - free_inodes

            percent_used = 0
            if total_inodes > 0:
                percent_used = (used_inodes / total_inodes) * 100

            return {
                "total": total_inodes,
                "used": used_inodes,
                "free": free_inodes,  # f_ffree is often what df -i reports as "Free"
                "percent": percent_used,
            }
        except OSError as e:
            # print(f"Warning: Could not get inode info for {mountpoint}: {e}", file=sys.stderr)
            return None  # Silently fail for paths where statvfs might not work (e.g. /proc entries)
    return None


def get_disk_partitions_info(specific_path=None, fstype_filter=None, show_inodes=False):
    """
    Gathers disk usage information for filesystems.
    """
    partitions_info = []

    target_device_stat = None
    if specific_path:
        abs_specific_path = os.path.abspath(specific_path)
        if not os.path.exists(abs_specific_path):
            print(
                f"Error: Specified path '{abs_specific_path}' does not exist.",
                file=sys.stderr,
            )
            return []
        try:
            # Get device ID of the filesystem where specific_path resides
            target_device_stat = os.stat(abs_specific_path).st_dev
        except OSError as e:
            print(f"Error stating path '{abs_specific_path}': {e}", file=sys.stderr)
            return []

    # Get all mounted disk partitions. all=False avoids virtual/duplicate fs like /dev/shm unless explicitly wanted
    # For specific path, we need to iterate all to find the match.
    try:
        mounted_partitions = psutil.disk_partitions(all=False)
    except Exception as e:
        print(f"Error getting disk partitions: {e}", file=sys.stderr)
        return []

    for part in mounted_partitions:
        # If specific_path is given, find the partition it belongs to
        if target_device_stat is not None:
            try:
                # Compare device ID of mountpoint with device ID of specific_path
                # This check can be problematic for some virtual/special mountpoints.
                # A simpler check might be if abs_specific_path.startswith(part.mountpoint)
                # but st_dev is more accurate for identifying the true partition.
                # However, st_dev might not be unique enough in all complex scenarios (e.g. bind mounts)
                # For now, we'll use startswith which is simpler and often good enough.
                # Let's use the st_dev method, it's generally more robust for physical devices.
                mountpoint_stat_dev = os.stat(part.mountpoint).st_dev
                if mountpoint_stat_dev != target_device_stat:
                    continue  # Not the partition we're looking for
            except (
                OSError
            ):  # Handle cases like permission denied for os.stat on a mountpoint
                # Fallback: check if specific path is under this mountpoint string-wise
                if not os.path.abspath(specific_path).startswith(part.mountpoint):
                    continue
                # If it is, this could be our partition, proceed with caution.

        # Filter by filesystem type if specified
        if fstype_filter and part.fstype.lower() != fstype_filter.lower():
            continue

        try:
            usage = psutil.disk_usage(part.mountpoint)
            inode_stats = None
            if show_inodes:
                inode_stats = get_inode_usage(part.mountpoint)

            partitions_info.append(
                {
                    "device": part.device,
                    "mountpoint": part.mountpoint,
                    "fstype": part.fstype,
                    "usage": usage,
                    "inodes": inode_stats,
                }
            )

            # If we found the specific path's partition, no need to check others
            if target_device_stat is not None:
                break

        except PermissionError:
            # print(f"Warning: Permission denied for {part.mountpoint}. Skipping.", file=sys.stderr)
            pass  # Silently skip inaccessible mount points
        except Exception as e:  # Catch other errors like CD-ROM drive with no media
            # print(f"Warning: Could not get usage for {part.mountpoint}: {e}. Skipping.", file=sys.stderr)
            pass

    if specific_path and not partitions_info:
        # This can happen if specific_path was valid, but its partition wasn't found or accessible
        # or if using os.stat().st_dev failed to match due to complex setups.
        # Try a direct psutil.disk_usage on the path itself as a fallback.
        try:
            usage = psutil.disk_usage(os.path.abspath(specific_path))
            inode_stats = (
                get_inode_usage(os.path.abspath(specific_path)) if show_inodes else None
            )
            partitions_info.append(
                {
                    "device": "N/A (direct path)",
                    "mountpoint": os.path.abspath(specific_path),
                    "fstype": "N/A",
                    "usage": usage,
                    "inodes": inode_stats,
                }
            )
        except Exception as e:
            print(
                f"Error: Could not get disk usage for path '{specific_path}' directly: {e}",
                file=sys.stderr,
            )

    return partitions_info


def print_disk_info_table(partitions_data, show_inodes_flag):
    """Prints disk usage information in a formatted table."""
    if not partitions_data:
        print("No disk partitions found matching criteria or accessible.")
        return

    # Determine headers
    headers = ["Filesystem", "Mountpoint", "Type", "Total", "Used", "Free", "Use%"]
    if show_inodes_flag:
        headers.extend(["INodes_Total", "INodes_Used", "INodes_Free", "IUse%"])

    # Create format string dynamically based on header lengths or fixed widths
    # For simplicity, using fixed estimated widths for now
    header_fmt = "{:<25} {:<25} {:<10} {:>10} {:>10} {:>10} {:>7}"
    row_fmt = "{:<25} {:<25} {:<10} {:>10} {:>10} {:>10} {:>6.1f}%"
    if show_inodes_flag:
        header_fmt += " {:>15} {:>15} {:>15} {:>7}"
        row_fmt += " {:>15} {:>15} {:>15} {:>6.1f}%"

    print(header_fmt.format(*headers))

    for info in partitions_data:
        usage = info["usage"]
        row_values = [
            info["device"][:24],  # Truncate if too long
            info["mountpoint"][:24],
            info["fstype"],
            bytes_to_human_readable(usage.total, suffix=""),
            bytes_to_human_readable(usage.used, suffix=""),
            bytes_to_human_readable(usage.free, suffix=""),
            usage.percent,
        ]
        if show_inodes_flag:
            inodes = info["inodes"]
            if inodes:
                row_values.extend(
                    [
                        str(
                            inodes["total"]
                        ),  # Already numbers, could format if very large
                        str(inodes["used"]),
                        str(inodes["free"]),
                        inodes["percent"],
                    ]
                )
            else:  # Inode info not available/applicable
                row_values.extend(["N/A"] * 4)

        print(row_fmt.format(*row_values))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Display disk space usage for mounted filesystems.",
        epilog="Example: python diskSpace.py /var --fstype ext4 --inodes",
    )
    parser.add_argument(
        "path",
        nargs="?",  # Optional positional argument
        default=None,  # Default to None, meaning all mount points
        help="Optional: Specific path to check disk usage for (e.g., /home, C:\\). Shows usage for the partition containing this path.",
    )
    parser.add_argument(
        "--fstype",
        metavar="TYPE",
        help="Filter filesystems by type (e.g., ext4, ntfs, apfs).",
    )
    parser.add_argument(
        "--inodes",
        action="store_true",
        help="Display inode usage information in addition to disk space (POSIX systems only for inodes).",
    )

    args = parser.parse_args()

    if args.inodes and not hasattr(os, "statvfs"):
        print(
            "Warning: Inode information (--inodes) is typically available on POSIX-compliant systems (Linux, macOS). It may not be shown on this system.",
            file=sys.stderr,
        )

    print("Gathering disk space information...")
    disk_info_list = get_disk_partitions_info(args.path, args.fstype, args.inodes)

    if disk_info_list:
        print_disk_info_table(disk_info_list, args.inodes)
    else:
        if args.path:
            print(
                f"No disk information found or accessible for path '{args.path}' with specified filters."
            )
        else:
            print("No disk partitions found or accessible with specified filters.")

    print("\nDisk space check complete.")
