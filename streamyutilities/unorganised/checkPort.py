#!/usr/bin/env python3

import socket
import argparse
import sys
import os

DEFAULT_TIMEOUT = 3.0 # seconds

def check_tcp_port(host, port, timeout):
    """
    Attempts to establish a TCP connection to the specified host and port.
    Returns a tuple (is_open, message).
    """
    try:
        # Create a new socket using IPv4 and TCP
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Set a timeout for the connection attempt
        s.settimeout(timeout)

        # Attempt to connect. connect_ex() returns an error indicator (0 on success)
        # For blocking sockets with a timeout, connect() would raise socket.timeout.
        # connect_ex() is generally preferred for non-blocking mode, but works here too.
        result_code = s.connect_ex((host, port))

        if result_code == 0:
            return True, f"Port {port} on host '{host}' is open."
        else:
            # Provide a more specific message if possible based on common error codes
            # These error codes can be OS-dependent.
            # errno.ECONNREFUSED (111 on Linux) is common for closed ports.
            # errno.ETIMEDOUT (110 on Linux) for timeouts.
            # However, connect_ex() might not always return these directly in all scenarios.
            # The fact that it's not 0 means it failed.
            error_reason = os.strerror(result_code) if hasattr(os, 'strerror') and result_code != 0 else f"Error code {result_code}"
            return False, f"Port {port} on host '{host}' is closed or unreachable. Reason: {error_reason}"

    except socket.timeout: # This can happen if the host is up but the port is filtered, or host is slow
        return False, f"Port {port} on host '{host}' timed out after {timeout} seconds."
    except socket.gaierror: # Address-related error (e.g., hostname not found)
        return False, f"Error: Hostname '{host}' could not be resolved."
    except socket.error as e: # Other socket-related errors
        return False, f"Socket error connecting to '{host}':{port} - {e}"
    except Exception as e: # Catch-all for any other unexpected errors
        return False, f"An unexpected error occurred: {e}"
    finally:
        if 's' in locals() and isinstance(s, socket.socket):
            s.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check if a TCP port is open on a specified host.",
        epilog="Example: python checkPort.py 80 --hostname google.com --timeout 1"
    )
    parser.add_argument(
        "port",
        type=int,
        help="The port number to check (1-65535)."
    )
    parser.add_argument(
        "--hostname",
        default="localhost",
        help="The hostname or IP address to check. Default: 'localhost'."
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help=f"Connection timeout in seconds. Default: {DEFAULT_TIMEOUT}s."
    )

    args = parser.parse_args()

    # Validate port number
    if not (1 <= args.port <= 65535):
        print(f"Error: Port number {args.port} is invalid. Must be between 1 and 65535.")
        sys.exit(1)

    if args.timeout <= 0:
        print(f"Error: Timeout value {args.timeout} is invalid. Must be positive.")
        sys.exit(1)

    print(f"Attempting to connect to host '{args.hostname}' on port {args.port} with a timeout of {args.timeout}s...")

    is_open, message = check_tcp_port(args.hostname, args.port, args.timeout)

    print(message)

    if is_open:
        # Exit with 0 if port is open
        sys.exit(0)
    else:
        # Exit with 1 if port is closed or error occurred
        sys.exit(1)
