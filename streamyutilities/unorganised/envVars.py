#!/usr/bin/env python3

import os
import argparse
import json
import shlex  # For robust quoting in export format


def get_env_variables(filter_str=None, case_sensitive=False):
    """
    Retrieves environment variables, optionally filtered.
    Returns a dictionary of matching environment variables.
    """
    s = os.environ
    return (
        {
            k: v
            for k, v in s.items()
            if (filter_str or "") in (k if case_sensitive else k.lower())
            or (filter_str or "") in (v if case_sensitive else v.lower())
        }
        if filter_str
        else dict(s)
    )


def format_variables(variables_dict, output_format):
    """Formats the variables according to the specified output format."""
    output_lines = []
    if not variables_dict:
        return [
            "No environment variables match the criteria or none are set (unlikely)."
        ]

    if output_format == "list":
        # Sort by key for consistent output
        for key, value in sorted(variables_dict.items()):
            output_lines.append(f"{key}={value}")
    elif output_format == "json":
        try:
            # sort_keys for consistent output
            output_lines.append(json.dumps(variables_dict, indent=4, sort_keys=True))
        except TypeError as e:
            output_lines.append(
                f"Error: Could not serialize environment variables to JSON: {e}"
            )
            output_lines.append("Attempting simple key-value list instead:")
            for key, value in sorted(variables_dict.items()):  # Fallback
                output_lines.append(f"{key}={value}")
    elif output_format == "export":
        # Sort by key for consistent output
        for key, value in sorted(variables_dict.items()):
            # Use shlex.quote to handle special characters in values for shell export
            output_lines.append(f"export {key}={shlex.quote(value)}")

    return output_lines


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="List environment variables with filtering and formatting options.",
        epilog='Example: python envVars.py --filter "path" --format export',
    )
    parser.add_argument(
        "--filter",
        metavar="SEARCH_STRING",
        help="Filter variables by a string (searches keys and values, case-insensitive by default).",
    )
    parser.add_argument(
        "--name",
        metavar="VAR_NAME",
        help="Display the value of a single, specific environment variable.",
    )
    parser.add_argument(
        "--format",
        choices=["list", "json", "export"],
        default="list",
        help="Output format: 'list' (KEY=VALUE), 'json', or 'export' (export KEY=\"VALUE\"). Default: 'list'.",
    )
    parser.add_argument(
        "--case-sensitive",
        action="store_true",
        help="Make filtering case-sensitive. Default is case-insensitive.",
    )

    args = parser.parse_args()

    if args.name:
        # If a specific variable name is requested, prioritize that and print its value
        var_value = os.getenv(
            args.name
        )  # os.getenv returns None if not found, vs os.environ[] raising KeyError
        if var_value is not None:
            # How should --format apply here? The example implies direct print.
            # For now, --name ignores --format and just prints the value.
            # Or, it could be formatted:
            if args.format == "export":
                print(f"export {args.name}={shlex.quote(var_value)}")
            elif args.format == "json":  # Output as a simple JSON {"name": "value"}
                print(json.dumps({args.name: var_value}, indent=4))
            else:  # 'list' or default
                print(
                    var_value
                )  # Simple value print for --name as per common expectation
        else:
            print(f"Environment variable '{args.name}' not found.")
            # sys.exit(1) # Optionally exit with error if var not found
    else:
        # General listing, filtering, and formatting
        variables = get_env_variables(args.filter, args.case_sensitive)
        formatted_output_lines = format_variables(variables, args.format)
        for line in formatted_output_lines:
            print(line)

    # print("\nEnvironment variable listing complete.") # Optional completion message.
