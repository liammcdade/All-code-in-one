#!/usr/bin/env python3

import os
import sys
import argparse
import subprocess
import shutil

VENV_BASE_DIR = os.path.expanduser("~/.virtualenvs")
LOCAL_VENV_NAME = ".venv" # Default name for local venv

def get_venv_path(name=None):
    """
    Determines the full path for a virtual environment.
    If name is None, it's for a local .venv in CWD.
    Otherwise, it's in VENV_BASE_DIR.
    """
    if name:
        return os.path.join(VENV_BASE_DIR, name)
    else:
        return os.path.join(os.getcwd(), LOCAL_VENV_NAME)

def venv_exists(path):
    """Checks if a venv seems to exist at the given path."""
    # A simple check for pyvenv.cfg or activate script
    if os.path.isdir(path):
        if os.path.isfile(os.path.join(path, "pyvenv.cfg")):
            return True
        # Check for activate scripts (might vary slightly by OS or venv tool)
        if os.path.isfile(os.path.join(path, "bin", "activate")) or \
           os.path.isfile(os.path.join(path, "Scripts", "activate")):
            return True
    return False

# --- Action Functions ---
def create_venv(name, python_exe):
    target_path = get_venv_path(name)
    display_name = name if name else f"./{LOCAL_VENV_NAME}"

    if venv_exists(target_path):
        print(f"Error: Virtual environment '{display_name}' already exists at '{target_path}'.", file=sys.stderr)
        # Consider adding a --force or --recreate option here
        return

    if name and not os.path.exists(VENV_BASE_DIR):
        try:
            os.makedirs(VENV_BASE_DIR)
            print(f"Created base directory for named virtual environments: '{VENV_BASE_DIR}'")
        except OSError as e:
            print(f"Error: Could not create base directory '{VENV_BASE_DIR}': {e}", file=sys.stderr)
            return

    command = [python_exe, "-m", "venv", target_path]
    print(f"Creating virtual environment '{display_name}' at '{target_path}' using '{python_exe}'...")
    print(f"Running command: {' '.join(command)}")

    try:
        process = subprocess.run(command, capture_output=True, text=True, check=True)
        print(f"Successfully created virtual environment '{display_name}'.")
        if process.stdout: print(f"Output:\n{process.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error creating virtual environment '{display_name}':", file=sys.stderr)
        print(f"  Command: {' '.join(e.cmd)}", file=sys.stderr)
        print(f"  Return code: {e.returncode}", file=sys.stderr)
        if e.stdout: print(f"  Stdout:\n{e.stdout}", file=sys.stderr)
        if e.stderr: print(f"  Stderr:\n{e.stderr}", file=sys.stderr)
    except FileNotFoundError:
        print(f"Error: Python interpreter '{python_exe}' not found.", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred during venv creation: {e}", file=sys.stderr)


def activate_venv_instructions(name):
    target_path = get_venv_path(name)
    display_name = name if name else f"./{LOCAL_VENV_NAME}"

    if not venv_exists(target_path):
        print(f"Error: Virtual environment '{display_name}' not found at '{target_path}'.", file=sys.stderr)
        print(f"Consider creating it first: python {os.path.basename(__file__)} create {name if name else ''}", file=sys.stderr)
        return

    print(f"To activate the virtual environment '{display_name}', run the following command in your shell:")

    if os.name == 'posix': # Linux, macOS, etc.
        activate_script = os.path.join(target_path, "bin", "activate")
        print(f"\n  source {activate_script}\n")
    elif os.name == 'nt': # Windows
        activate_script_cmd = os.path.join(target_path, "Scripts", "activate.bat")
        activate_script_ps = os.path.join(target_path, "Scripts", "Activate.ps1")
        print("\n  For Command Prompt (cmd.exe):")
        print(f"    {activate_script_cmd}")
        print("\n  For PowerShell:")
        print(f"    & \"{activate_script_ps}\"") # Or just `.\path\to\Activate.ps1`
        print("    (If PowerShell script execution is restricted, you might need to run: Set-ExecutionPolicy RemoteSigned -Scope CurrentUser)\n")
    else:
        print(f"\nActivation command for your operating system ('{os.name}') is not pre-defined by this script.")
        print(f"Look for an 'activate' script inside '{os.path.join(target_path, 'bin')}' or '{os.path.join(target_path, 'Scripts')}'.\n")


def list_venvs():
    print(f"--- Available Named Virtual Environments (in '{VENV_BASE_DIR}') ---")
    if not os.path.isdir(VENV_BASE_DIR):
        print("Base directory for named virtual environments does not exist or is not a directory.")
        print(f"(Expected at: '{VENV_BASE_DIR}')")
        return

    found_venvs = []
    for item_name in sorted(os.listdir(VENV_BASE_DIR)):
        item_path = os.path.join(VENV_BASE_DIR, item_name)
        if venv_exists(item_path): # Check if it looks like a venv
            found_venvs.append(item_name)

    if not found_venvs:
        print("No named virtual environments found.")
    else:
        for venv_name in found_venvs:
            print(f"  - {venv_name}")

    # Check for local .venv
    local_path = get_venv_path(None)
    if venv_exists(local_path):
        print(f"\n--- Local Virtual Environment ---")
        print(f"  - ./{LOCAL_VENV_NAME} (in current directory: {os.getcwd()})")


def remove_venv(name):
    target_path = get_venv_path(name)
    display_name = name if name else f"./{LOCAL_VENV_NAME}" # Should require name for remote

    if not name: # Safety: require explicit name for remove, don't just delete ./.venv implicitly
        print("Error: You must specify the name of the virtual environment to remove.", file=sys.stderr)
        print("To remove a local './.venv', provide '.' or '.venv' as the name if that's intended (not yet supported, use manual `rm -rf .venv`).", file=sys.stderr)
        # For now, this tool focuses on named environments for remove.
        # Or, we could allow `remove .` to mean remove local.
        # The prompt `remove [name]` implies named.
        return


    if not venv_exists(target_path): # Checks named venv path
        print(f"Error: Named virtual environment '{name}' not found at '{target_path}'.", file=sys.stderr)
        return

    print(f"WARNING: This will permanently delete the virtual environment '{name}' at '{target_path}'.")
    try:
        confirm = input("Are you sure you want to proceed? (yes/no): ").strip().lower()
    except EOFError:
        print("\nNo input. Aborting.", file=sys.stderr)
        return
    except KeyboardInterrupt:
         print("\nUser cancelled. Aborting.", file=sys.stderr)
         return


    if confirm == 'yes':
        try:
            shutil.rmtree(target_path)
            print(f"Successfully removed virtual environment '{name}'.")
        except OSError as e:
            print(f"Error removing virtual environment '{name}': {e}", file=sys.stderr)
        except Exception as e:
            print(f"An unexpected error occurred during removal: {e}", file=sys.stderr)
    else:
        print("Removal cancelled by user.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage Python virtual environments using the 'venv' module.")
    subparsers = parser.add_subparsers(dest="action", title="Actions", help="Available actions", required=True)

    # Create command
    parser_create = subparsers.add_parser("create", help="Create a new virtual environment.")
    parser_create.add_argument(
        "name",
        nargs="?", # Name is optional
        default=None, # If no name, implies local ./.venv
        help=f"Name of the virtual environment (stored in '{VENV_BASE_DIR}'). If omitted, creates '{LOCAL_VENV_NAME}' in current directory."
    )
    parser_create.add_argument(
        "--python",
        default=sys.executable, # Defaults to the python running this script
        help="Path to the Python interpreter to use for the virtual environment (e.g., python3.9, /usr/bin/python3). Default: current Python."
    )

    # Activate command
    parser_activate = subparsers.add_parser("activate", help="Show command to activate a virtual environment.")
    parser_activate.add_argument(
        "name",
        nargs="?",
        default=None, # If no name, implies local ./.venv
        help=f"Name of the virtual environment to activate. If omitted, assumes '{LOCAL_VENV_NAME}' in current directory."
    )

    # List command
    parser_list = subparsers.add_parser("list", help="List available managed virtual environments.")

    # Remove command
    parser_remove = subparsers.add_parser("remove", help="Remove a named virtual environment.")
    parser_remove.add_argument(
        "name", # Name is required for remove for safety
        help=f"Name of the virtual environment (from '{VENV_BASE_DIR}') to remove."
    )

    args = parser.parse_args()

    if args.action == "create":
        create_venv(args.name, args.python)
    elif args.action == "activate":
        activate_venv_instructions(args.name)
    elif args.action == "list":
        list_venvs()
    elif args.action == "remove":
        remove_venv(args.name)
    else:
        parser.print_help()

    sys.exit(0)
