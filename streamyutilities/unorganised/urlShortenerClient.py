#!/usr/bin/env python3

import argparse
import urllib.request
import urllib.parse
import urllib.error
import sys

# TinyURL API endpoint
TINYURL_API_ENDPOINT = "http://tinyurl.com/api-create.php"
# A short timeout for the request, e.g., 10 seconds
REQUEST_TIMEOUT = 10


def get_short_url(long_url_to_shorten):
    """
    Connects to the TinyURL API to shorten the given long URL.
    Returns the shortened URL string if successful, None otherwise.
    """
    try:
        # URL-encode the long URL to be safely included as a query parameter
        encoded_params = urllib.parse.urlencode({"url": long_url_to_shorten})
        full_api_url = f"{TINYURL_API_ENDPOINT}?{encoded_params}"

        # print(f"Debug: Requesting URL: {full_api_url}") # For debugging

        req = urllib.request.Request(full_api_url)
        # Some services might require a common User-Agent
        req.add_header(
            "User-Agent",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
        )

        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as response:
            # Read the response content
            response_bytes = response.read()
            # The response from this TinyURL API is expected to be plain text (the short URL)
            # Decode it from bytes to a string, assuming UTF-8 or ASCII
            short_url = response_bytes.decode("utf-8")

            if response.status == 200:
                if short_url.startswith("http://tinyurl.com/") or short_url.startswith(
                    "https://tinyurl.com/"
                ):
                    return short_url
                else:
                    # Response might be an error message from TinyURL not sent with an HTTP error code
                    print(
                        f"Error: Service returned an unexpected response: {short_url[:100]}"
                    )
                    return None
            else:  # Should be caught by HTTPError, but as a fallback
                print(f"Error: Service responded with status code {response.status}")
                return None

    except urllib.error.HTTPError as e:
        # HTTP errors (e.g., 400 Bad Request, 500 Internal Server Error)
        error_content = ""
        try:
            error_content = e.read().decode("utf-8")
        except Exception:
            error_content = "Could not read error response body."
        print(
            f"HTTP Error from service: {e.code} {e.reason}. Response: {error_content[:200]}"
        )
        if e.code == 400:
            print("Hint: The provided URL might be invalid or malformed.")
        return None
    except urllib.error.URLError as e:
        # Network-related errors (e.g., no internet connection, DNS failure)
        print(
            f"URL Error: Could not reach the URL shortening service. Reason: {e.reason}"
        )
        return None
    except TimeoutError:  # Explicitly catch timeout from urllib.request.urlopen
        print(
            f"Error: The request to the URL shortening service timed out after {REQUEST_TIMEOUT} seconds."
        )
        return None
    except Exception as e:
        # Catch any other unexpected errors
        print(f"An unexpected error occurred: {e}")
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Shorten a long URL using the TinyURL service.",
        epilog='Example: python urlShortenerClient.py "https://www.example.com/a/very/long/path?and=query_params"',
    )
    parser.add_argument("long_url", help="The long URL that you want to shorten.")

    args = parser.parse_args()

    # Basic validation for the input URL structure (very simple check)
    if not (
        args.long_url.startswith("http://") or args.long_url.startswith("https://")
    ):
        # Prepend http:// if scheme is missing, as some services require it.
        # However, TinyURL's web UI adds it, API might be stricter or also flexible.
        # Forcing it might be presumptuous. Better to let user provide valid URL.
        print(
            "Warning: The provided URL does not seem to have a scheme (http:// or https://)."
        )
        print(
            "Attempting to shorten it as is, but the service might require a full URL including the scheme."
        )
        # Consider exiting or automatically prepending:
        # if not urllib.parse.urlparse(args.long_url).scheme:
        #     args.long_url = "http://" + args.long_url
        #     print(f"Note: Prepended 'http://' to the URL: {args.long_url}")

    print(f"Attempting to shorten URL: {args.long_url}")
    shortened_url = get_short_url(args.long_url)

    if shortened_url:
        print("\nShortened URL:")
        print(shortened_url)
    else:
        print("\nFailed to shorten the URL.")
        # Specific error messages are printed by get_short_url()

    print("\nURL shortening process complete.")
