#!/usr/bin/env python3

import random
import string
import argparse

# Character sets
LOWERCASE = string.ascii_lowercase
UPPERCASE = string.ascii_uppercase
DIGITS = string.digits
SYMBOLS = string.punctuation # Common symbols. User might want to customize this.

def generate_single_password(length, use_lowercase, use_uppercase, use_digits, use_symbols):
    """Generates a single random password based on specified criteria."""

    char_pool = []
    password_components = []

    if use_lowercase:
        char_pool.extend(LOWERCASE)
        password_components.append(random.choice(LOWERCASE))
    if use_uppercase:
        char_pool.extend(UPPERCASE)
        password_components.append(random.choice(UPPERCASE))
    if use_digits:
        char_pool.extend(DIGITS)
        password_components.append(random.choice(DIGITS))
    if use_symbols:
        char_pool.extend(SYMBOLS)
        # Ensure we don't pick a symbol that might cause issues if copy-pasted in some contexts
        # For this general tool, string.punctuation is fine.
        password_components.append(random.choice(SYMBOLS))

    if not char_pool:
        # This happens if all --no-* flags are used or if defaults were all False and none enabled
        print("Error: No character types selected. Cannot generate password.")
        print("Please enable at least one character type (e.g., --lowercase, --digits).")
        return None

    # Check if the number of required components exceeds the desired length
    if len(password_components) > length:
        print(f"Error: Password length {length} is too short to include all required character types.")
        print(f"Minimum length required for current selection: {len(password_components)}.")
        return None

    # Fill the rest of the password length with random characters from the combined pool
    remaining_length = length - len(password_components)
    for _ in range(remaining_length):
        password_components.append(random.choice(char_pool))

    # Shuffle the components to ensure randomness of character positions
    random.shuffle(password_components)

    return "".join(password_components)


if __name__ == "__main__":
    # For BooleanOptionalAction, Python 3.9+ is needed.
    # If targeting older, use store_true for --include-* and store_false for --exclude-*.
    # The example usage like --no-symbols suggests BooleanOptionalAction is intended.
    # Let's assume Python 3.9+ for cleaner arg parsing.
    # If this fails in the environment, I'll switch to the older style.

    # Check Python version for BooleanOptionalAction.
    # This is a meta-comment; the actual script won't do this version check at runtime for argparse.
    # For now, I will proceed assuming BooleanOptionalAction is available.
    # If an error occurs during testing in the environment, I'll revise to compatible argparse.
    # Given no direct feedback, I'll use a compatible way (paired flags or careful defaults).

    parser = argparse.ArgumentParser(
        description="Generate random passwords with specified criteria.",
        epilog="Example: python generatePassword.py --length 16 --no-symbols"
    )
    parser.add_argument(
        "--length",
        type=int,
        default=16,
        help="Specify the length of the password(s). Default: 16."
    )
    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="Number of passwords to generate. Default: 1."
    )
    # Using explicit --include/--exclude pairs for broader compatibility than BooleanOptionalAction
    parser.add_argument('--include-lowercase', dest='use_lowercase', action='store_true', help="Include lowercase letters (default: true if no specific includes, else false).")
    parser.add_argument('--exclude-lowercase', dest='use_lowercase', action='store_false', help="Exclude lowercase letters.")

    parser.add_argument('--include-uppercase', dest='use_uppercase', action='store_true', help="Include uppercase letters (default: true if no specific includes, else false).")
    parser.add_argument('--exclude-uppercase', dest='use_uppercase', action='store_false', help="Exclude uppercase letters.")

    parser.add_argument('--include-digits', dest='use_digits', action='store_true', help="Include digits (default: true if no specific includes, else false).")
    parser.add_argument('--exclude-digits', dest='use_digits', action='store_false', help="Exclude digits.")

    parser.add_argument('--include-symbols', dest='use_symbols', action='store_true', help="Include symbols (default: true if no specific includes, else false).")
    parser.add_argument('--exclude-symbols', dest='use_symbols', action='store_false', help="Exclude symbols.")

    # Set defaults for character types
    # If NO include/exclude options are specified for a type, it defaults to True.
    # If ANY include/exclude is specified, that takes precedence.
    # This logic needs to be handled after parsing.
    parser.set_defaults(use_lowercase=None, use_uppercase=None, use_digits=None, use_symbols=None)

    args = parser.parse_args()

    # Determine final character type usage
    # If no specific choice made for a type, default to True.
    # If any specific choice was made (e.g. --exclude-lowercase), it's already set by set_defaults + action.
    # This logic means: if a user specifies *any* --include or --exclude, they are taking full control.
    # If they specify *nothing* about types, all types are included.

    # A simpler default: if no specific --include-* are given, assume all are true unless an --exclude-* is given.
    # Let's refine the defaults based on what's specified.
    # If a user specifies *any* --include-* flag, then only those included are true.
    # If a user specifies *only* --exclude-* flags, then all others are true.
    # If a user specifies *neither*, all are true.

    # Simplified logic:
    # Default to all True. If user uses any --exclude-* it turns that one off.
    # If user uses any --include-*, it implies they want finer control. This is tricky with argparse's default system.
    # The provided example `generatePassword.py --length 20 --no-symbols --count 3` implies that
    # by default most things are on, and `--no-symbols` turns one off.

    # Let's use the set_defaults(use_type=True) and then --exclude-type sets it to False.
    # This is the most straightforward interpretation of the example.
    # So, if user says --exclude-symbols, use_symbols becomes False. Otherwise, it's True.

    # Re-evaluating default strategy for argparse for clarity:
    # Each type is ON by default. User can turn it OFF with --exclude-<type>.
    # The --include-<type> flags are then only for turning them back ON if a user
    # for some reason did --exclude-<type> then --include-<type>.
    # Argparse handles the last one specified. So, let's set default=True for use_ flags.

    # Resetting parser for clearer default handling:
    parser = argparse.ArgumentParser(
        description="Generate random passwords with specified criteria.",
        epilog="Example: python generatePassword.py --length 16 --exclude-symbols" # Adjusted example
    )
    parser.add_argument("--length", type=int, default=16, help="Length of the password(s). Default: 16.")
    parser.add_argument("--count", type=int, default=1, help="Number of passwords to generate. Default: 1.")

    # Python 3.9+ BooleanOptionalAction would be:
    # parser.add_argument('--lowercase', action=argparse.BooleanOptionalAction, default=True)
    # Emulating for broader compatibility:
    parser.add_argument('--lowercase', dest='use_lowercase', action='store_true', default=True, help="Include lowercase letters (default).")
    parser.add_argument('--no-lowercase', dest='use_lowercase', action='store_false', help="Exclude lowercase letters.")
    parser.add_argument('--uppercase', dest='use_uppercase', action='store_true', default=True, help="Include uppercase letters (default).")
    parser.add_argument('--no-uppercase', dest='use_uppercase', action='store_false', help="Exclude uppercase letters.")
    parser.add_argument('--digits', dest='use_digits', action='store_true', default=True, help="Include digits (default).")
    parser.add_argument('--no-digits', dest='use_digits', action='store_false', help="Exclude digits.")
    parser.add_argument('--symbols', dest='use_symbols', action='store_true', default=True, help="Include symbols (default).")
    parser.add_argument('--no-symbols', dest='use_symbols', action='store_false', help="Exclude symbols.")

    # The example also had --require-uppercase. This is different from --use-uppercase.
    # --use implies it's in the pool. --require implies it *must* be in the output.
    # My current generate_single_password *ensures* one of each `use_` type. So `use_` effectively means `require_`.
    # This is a common and good behavior.

    args = parser.parse_args()


    if args.length <= 0:
        print("Error: Password length must be a positive integer.")
        return
    if args.count <= 0:
        print("Error: Number of passwords to generate must be a positive integer.")
        return

    # Check if all character types are disabled
    if not args.use_lowercase and not args.use_uppercase and not args.use_digits and not args.use_symbols:
        print("Error: All character types are disabled. At least one character type must be enabled to generate a password.")
        print("Using lowercase letters as a fallback.") # Or exit(1)
        args.use_lowercase = True # Fallback

    print(f"Generating {args.count} password(s) with length {args.length}:")
    print(f"(Lowercase: {args.use_lowercase}, Uppercase: {args.use_uppercase}, Digits: {args.use_digits}, Symbols: {args.use_symbols})")

    for i in range(args.count):
        password = generate_single_password(
            args.length,
            args.use_lowercase,
            args.use_uppercase,
            args.use_digits,
            args.use_symbols
        )
        if password:
            print(password)
        else:
            # Error message already printed by generate_single_password
            print(f"Could not generate password {i+1} due to unmet constraints.")
            break # Stop if one password fails, as others likely will too.

    print("\nPassword generation complete.")
