#!/usr/bin/env python3

import http.server
import socketserver
import argparse
import os
import sys
import functools # To pass directory to handler
import socket # To get local IP addresses

DEFAULT_PORT = 8000
DEFAULT_BIND_ADDRESS = "0.0.0.0" # Serve on all available interfaces
DEFAULT_DIRECTORY = "." # Current working directory

def get_local_ip_addresses():
    """Attempts to get local IP addresses for display."""
    ips = set()
    try:
        hostname = socket.gethostname()
        # Get all IP addresses associated with the hostname
        # This can include loopback, ethernet, wifi, etc.
        # (name, aliaslist, addresslist)
        name, aliaslist, addresslist = socket.gethostbyname_ex(hostname)
        for ip in addresslist:
            ips.add(ip)
        # Add common loopback if not already found (e.g. if hostname resolves to external IP first)
        ips.add("127.0.0.1")
    except socket.gaierror: # Could not resolve hostname
        ips.add("127.0.0.1") # At least show loopback
    return sorted(list(ips))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Start a simple HTTP server to serve files from a specified directory.",
        epilog=f"Example: python tempServer.py --port 8080 --directory /tmp --bind 127.0.0.1"
    )
    parser.add_argument(
        "--directory",
        default=DEFAULT_DIRECTORY,
        help=f"Directory to serve files from. Default: '{DEFAULT_DIRECTORY}' (current working directory)."
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"Port number to listen on. Default: {DEFAULT_PORT}."
    )
    parser.add_argument(
        "--bind",
        default=DEFAULT_BIND_ADDRESS,
        help=f"IP address to bind to. Default: '{DEFAULT_BIND_ADDRESS}' (all interfaces)."
    )

    args = parser.parse_args()

    # Validate directory
    serve_directory = os.path.abspath(args.directory)
    if not os.path.isdir(serve_directory):
        print(f"Error: Directory '{serve_directory}' not found or is not a directory.", file=sys.stderr)
        sys.exit(1)

    # Validate port
    if not (1 <= args.port <= 65535):
        print(f"Error: Port number {args.port} is invalid. Must be between 1 and 65535.", file=sys.stderr)
        sys.exit(1)

    # Create a handler partial that serves files from the specified directory
    # This requires Python 3.7+ for the 'directory' parameter in SimpleHTTPRequestHandler
    # For older Python, one would need to os.chdir(serve_directory) before starting the server.
    try:
        HandlerClass = functools.partial(http.server.SimpleHTTPRequestHandler, directory=serve_directory)
    except TypeError: # 'directory' keyword unavailable (Python < 3.7) or other init issue
        print("Warning: functools.partial with directory failed (Python < 3.7 or other issue).")
        print(f"Attempting to serve by changing current directory to '{serve_directory}'.")
        try:
            os.chdir(serve_directory)
            HandlerClass = http.server.SimpleHTTPRequestHandler
        except Exception as e_chdir:
            print(f"Error: Could not change to directory '{serve_directory}': {e_chdir}", file=sys.stderr)
            sys.exit(1)


    httpd = None
    try:
        # Create the server
        httpd = socketserver.TCPServer((args.bind, args.port), HandlerClass)

        print(f"--- Simple HTTP Server ---")
        print(f"Serving files from directory: {serve_directory}")

        display_bind_address = args.bind
        if args.bind == "0.0.0.0":
            print(f"Bound to all interfaces ({args.bind}). Accessible via:")
            local_ips = get_local_ip_addresses()
            for ip_addr in local_ips:
                print(f"  http://{ip_addr}:{args.port}/")
        else:
            print(f"Bound to specific IP: {args.bind}")
            print(f"  http://{args.bind}:{args.port}/")

        print(f"\nListening on port {args.port}...")
        print("Press Ctrl+C to stop the server.")

        # Start the server
        httpd.serve_forever()

    except socket.error as e:
        if e.errno == 98: # Address already in use [Errno 98]
            print(f"\nError: Port {args.port} on address '{args.bind}' is already in use.", file=sys.stderr)
        else:
            print(f"\nSocket error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nServer is shutting down (Ctrl+C pressed)...")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}", file=sys.stderr)
    finally:
        if httpd:
            httpd.shutdown() # Stop the server
            httpd.server_close() # Close the server socket
        print("Server has been shut down.")
        sys.exit(0)
