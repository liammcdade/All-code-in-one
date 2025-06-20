#!/usr/bin/env python3

import urllib.request
import urllib.error
import argparse
import sys
import re # For optional IP validation

# Configuration for the IP fetching service
DEFAULT_IP_SERVICE_URL = "https://api.ipify.org"
REQUEST_TIMEOUT = 5  # seconds

# Simple regex to validate if a string looks like an IPv4 address
IPV4_REGEX = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
# For IPv6, it's more complex, e.g. from https://stackoverflow.com/a/17871737/436706
# IPV6_REGEX = re.compile(r"(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))")
# For simplicity, this tool will primarily focus on IPv4 from ipify, but ipify can return IPv6 too.
# The regex validation will be basic.

def fetch_public_ip(service_url=DEFAULT_IP_SERVICE_URL, timeout=REQUEST_TIMEOUT):
    """
    Fetches the public IP address from the specified service URL.
    Returns the IP address string if successful, None otherwise.
    """
    try:
        req = urllib.request.Request(service_url)
        # Set a common User-Agent header, as some services might block default Python User-Agent
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0')

        with urllib.request.urlopen(req, timeout=timeout) as response:
            if response.status == 200:
                ip_address_bytes = response.read()
                # Response is expected to be plain text (the IP address)
                ip_address_str = ip_address_bytes.decode('utf-8').strip()

                # Optional: Validate if the response looks like an IP address
                # ipify.org can return IPv4 or IPv6. The simple regex is for IPv4.
                # For now, we'll trust the service if status is 200.
                # if not IPV4_REGEX.match(ip_address_str) and not IPV6_REGEX.match(ip_address_str): # More complex if checking both
                if not IPV4_REGEX.match(ip_address_str): # Simple IPv4 check
                     # Check if it might be IPv6 (contains colons)
                     if ':' not in ip_address_str:
                        print(f"Warning: Response '{ip_address_str}' from service doesn't look like a standard IPv4 address.", file=sys.stderr)
                        # Still return it, as it might be IPv6 or other format from a different service

                return ip_address_str
            else:
                print(f"Error: IP service responded with status code {response.status} {response.reason}", file=sys.stderr)
                return None

    except urllib.error.HTTPError as e:
        print(f"HTTP Error from IP service: {e.code} {e.reason}", file=sys.stderr)
        return None
    except urllib.error.URLError as e:
        print(f"URL Error: Could not reach IP service at '{service_url}'. Reason: {e.reason}", file=sys.stderr)
        return None
    except TimeoutError: # Explicitly catch timeout
        print(f"Error: Request to IP service timed out after {timeout} seconds.", file=sys.stderr)
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetches and displays your public IP address from an online service.",
        epilog="Example: python myIp.py"
    )
    # Placeholder for future arguments like --service or --verbose
    # parser.add_argument("--verbose", action="store_true", help="Enable verbose output for errors.")
    # For now, no arguments are strictly needed for basic functionality.

    args = parser.parse_args() # Even if no args defined, this provides -h/--help

    # print("Fetching your public IP address...", file=sys.stderr) # Optional status message

    public_ip = fetch_public_ip()

    if public_ip:
        print(public_ip) # Print IP to stdout as per requirement
        sys.exit(0)
    else:
        print("Failed to retrieve public IP address.", file=sys.stderr)
        sys.exit(1)
