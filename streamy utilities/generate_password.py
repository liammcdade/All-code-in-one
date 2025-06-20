#!/usr/bin/env python3

import argparse
import string

try:
    import secrets

    class SecureRandom:
        @staticmethod
        def choice(seq):
            return secrets.choice(seq)

        @staticmethod
        def shuffle(seq):
            for i in range(len(seq) - 1, 0, -1):
                j = secrets.randbelow(i + 1)
                seq[i], seq[j] = seq[j], seq[i]

    crypto_source = SecureRandom()
    using_secrets = True
except ImportError:
    import random

    crypto_source = random
    using_secrets = False

UPPERCASE = string.ascii_uppercase
LOWERCASE = string.ascii_lowercase
DIGITS = string.digits
SYMBOLS = "!@#$%^&*()_+-=[]{};':\",./<>?"

def generate_password(length, use_uppercase, use_lowercase, use_digits, use_symbols):
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
        raise ValueError("No character types selected. Cannot generate password.")

    password_chars = []

    if use_uppercase:
        password_chars.append(crypto_source.choice(UPPERCASE))
    if use_lowercase:
        password_chars.append(crypto_source.choice(LOWERCASE))
    if use_digits:
        password_chars.append(crypto_source.choice(DIGITS))
    if use_symbols:
        password_chars.append(crypto_source.choice(SYMBOLS))

    if len(password_chars) > length:
        crypto_source.shuffle(password_chars)
        return "".join(password_chars[:length])

    for _ in range(length - len(password_chars)):
        password_chars.append(crypto_source.choice(character_pool))

    crypto_source.shuffle(password_chars)
    return "".join(password_chars)

def main():
    parser = argparse.ArgumentParser(
        description="Generates cryptographically strong random passwords.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("--length", "-l", type=int, default=12,
                        help="Desired length of the password(s). Default is 12.")
    parser.add_argument("--count", "-n", type=int, default=1,
                        help="Number of passwords to generate. Default is 1.")
    parser.add_argument("--no-uppercase", action="store_false", dest="use_uppercase",
                        help="Exclude uppercase letters (A-Z).")
    parser.add_argument("--no-lowercase", action="store_false", dest="use_lowercase",
                        help="Exclude lowercase letters (a-z).")
    parser.add_argument("--no-digits", action="store_false", dest="use_digits",
                        help="Exclude digits (0-9).")
    parser.add_argument("--no-symbols", action="store_false", dest="use_symbols",
                        help="Exclude special symbols.")

    parser.set_defaults(use_uppercase=True, use_lowercase=True, use_digits=True, use_symbols=True)

    args = parser.parse_args()

    if not (args.use_uppercase or args.use_lowercase or args.use_digits or args.use_symbols):
        parser.error("At least one character type must be selected.")

    if args.length <= 0:
        parser.error("Password length must be positive.")

    selected_types = sum([args.use_uppercase, args.use_lowercase, args.use_digits, args.use_symbols])
    if args.length < selected_types:
        parser.error(f"Password length must be at least {selected_types} to include one of each selected type.")

    if args.count <= 0:
        parser.error("Password count must be positive.")

    print(f"Generating {args.count} password(s):")
    print(f"  Length: {args.length}")
    print(f"  Include Uppercase: {'Yes' if args.use_uppercase else 'No'}")
    print(f"  Include Lowercase: {'Yes' if args.use_lowercase else 'No'}")
    print(f"  Include Digits: {'Yes' if args.use_digits else 'No'}")
    print(f"  Include Symbols: {'Yes' if args.use_symbols else 'No'}")
    print(f"  Using {'secrets' if using_secrets else 'random'} module")
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
            print(f"Password {i + 1}: {password}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
