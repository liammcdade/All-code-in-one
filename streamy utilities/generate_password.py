"""
Generates cryptographically strong random passwords based on specified criteria.

Usage:
    python generate_password.py [--length L] [--count C] \
                                [--no-uppercase] [--no-lowercase] \
                                [--no-digits] [--no-symbols]

Arguments:
    --length L, -l L:   Desired length of the password. Default is 12.
    --count C, -n C:    Number of passwords to generate. Default is 1.
    --no-uppercase:     Exclude uppercase letters (A-Z).
    --no-lowercase:     Exclude lowercase letters (a-z).
    --no-digits:        Exclude digits (0-9).
    --no-symbols:       Exclude special symbols (e.g., !@#$%^&*).

At least one character type (uppercase, lowercase, digits, symbols) must be included.
Uses the 'secrets' module for generation if available, otherwise 'random'.
"""

import argparse
import string

try:
    import secrets
    crypto_source = secrets
except ImportError:
    import random
    crypto_source = random

# Define character sets
LOWERCASE = string.ascii_lowercase
UPPERCASE = string.ascii_uppercase
DIGITS = string.digits
SYMBOLS = "!@#$%^&*()_+-=[]{};':\",./<>?" # Common symbols; can be customized

def generate_password(length, use_uppercase, use_lowercase, use_digits, use_symbols):
    """Generates a single random password based on the criteria."""

    character_pool = []
    if use_uppercase:
        character_pool.extend(UPPERCASE)
    if use_lowercase:
        character_pool.extend(LOWERCASE)
    if use_digits:
        character_pool.extend(DIGITS)
    if use_symbols:
        character_pool.extend(SYMBOLS)

    if not character_pool:
        # This should be caught by pre-check in main, but as a safeguard:
        raise ValueError("No character types selected. Cannot generate password.")

    # Ensure the password contains at least one of each selected character type
    # This makes the generation a bit more complex but ensures policy compliance.
    password_chars = []

    # Pre-fill with one of each required type to guarantee their presence
    # This is important if the length is very small.
    if use_uppercase:
        password_chars.append(crypto_source.choice(UPPERCASE))
    if use_lowercase:
        password_chars.append(crypto_source.choice(LOWERCASE))
    if use_digits:
        password_chars.append(crypto_source.choice(DIGITS))
    if use_symbols:
        password_chars.append(crypto_source.choice(SYMBOLS))

    # If length is less than the number of required types, it's impossible to satisfy.
    # The argument parser should ideally prevent this based on length.
    # However, if it happens, the password will be shorter than requested but contain one of each.
    # For now, let's assume length >= number of selected categories.
    # If not, the fill below will make up the difference.

    if len(password_chars) > length:
        # This happens if, e.g., length=2 but all 4 types are required.
        # We'll shuffle and truncate. This isn't ideal, but better than erroring here
        # if the length check wasn't sufficient earlier.
        crypto_source.shuffle(password_chars)
        return "".join(password_chars[:length])

    # Fill the rest of the password length from the full pool
    remaining_length = length - len(password_chars)
    for _ in range(remaining_length):
        password_chars.append(crypto_source.choice(character_pool))

    # Shuffle the combined list to ensure randomness of positions
    crypto_source.shuffle(password_chars)

    return "".join(password_chars)

def main():
    parser = argparse.ArgumentParser(
        description="Generates cryptographically strong random passwords.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--length", "-l",
        type=int,
        default=12,
        help="Desired length of the password(s). Default is 12."
    )
    parser.add_argument(
        "--count", "-n",
        type=int,
        default=1,
        help="Number of passwords to generate. Default is 1."
    )
    parser.add_argument(
        "--no-uppercase",
        action="store_false",
        dest="use_uppercase",
        help="Exclude uppercase letters (A-Z). Included by default."
    )
    parser.add_argument(
        "--no-lowercase",
        action="store_false",
        dest="use_lowercase",
        help="Exclude lowercase letters (a-z). Included by default."
    )
    parser.add_argument(
        "--no-digits",
        action="store_false",
        dest="use_digits",
        help="Exclude digits (0-9). Included by default."
    )
    parser.add_argument(
        "--no-symbols",
        action="store_false",
        dest="use_symbols",
        help="Exclude special symbols. Included by default."
    )
    # Set defaults for boolean flags explicitly for clarity if needed, though store_false handles it.
    parser.set_defaults(use_uppercase=True, use_lowercase=True, use_digits=True, use_symbols=True)

    args = parser.parse_args()

    if not (args.use_uppercase or args.use_lowercase or args.use_digits or args.use_symbols):
        parser.error("At least one character type (uppercase, lowercase, digits, or symbols) must be selected.")

    if args.length <= 0:
        parser.error("Password length must be a positive integer.")

    # Check if length is sufficient for one of each selected category
    num_selected_categories = sum([args.use_uppercase, args.use_lowercase, args.use_digits, args.use_symbols])
    if args.length < num_selected_categories:
        parser.error(f"Password length ({args.length}) is too short to include at least one of each of the {num_selected_categories} selected character types.")

    if args.count <= 0:
        parser.error("Number of passwords to generate must be a positive integer.")

    print(f"Generating {args.count} password(s) with the following criteria:")
    print(f"  Length: {args.length}")
    print(f"  Include Uppercase: {'Yes' if args.use_uppercase else 'No'}")
    print(f"  Include Lowercase: {'Yes' if args.use_lowercase else 'No'}")
    print(f"  Include Digits: {'Yes' if args.use_digits else 'No'}")
    print(f"  Include Symbols: {'Yes' if args.use_symbols else 'No'}")
    if hasattr(crypto_source, 'SystemRandom'): # Indicates 'random' module is the fallback
        print("  Security Note: Using 'random' module as 'secrets' module was not found (Python < 3.6).")
    else:
        print("  Using 'secrets' module for cryptographically secure generation.")
    print("-" * 30)

    try:
        for i in range(args.count):
            password = generate_password(
                args.length,
                args.use_uppercase,
                args.use_lowercase,
                args.use_digits,
                args.use_symbols
            )
            print(f"Password {i+1}: {password}")
    except ValueError as e:
        # This might catch errors from generate_password if checks there fail,
        # though main() tries to prevent invalid configs.
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
