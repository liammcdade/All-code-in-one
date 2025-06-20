import os
import subprocess
import sys

def run_flake8_on_file(file_path):
    try:
        # Run flake8 and capture output
        result = subprocess.run(['flake8', file_path], capture_output=True, text=True)
        output = result.stdout.strip()
        return output
    except FileNotFoundError:
        return "Error: flake8 not found. Please install flake8 first."
    except subprocess.SubprocessError as e:
        return f"Error running flake8: {e}"

def find_python_files(root_dir):
    py_files = []
    try:
        for dirpath, _, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename.endswith('.py'):
                    py_files.append(os.path.join(dirpath, filename))
    except PermissionError as e:
        print(f"Warning: Permission denied accessing some directories: {e}")
    return py_files

def main(root_dir):
    py_files = find_python_files(root_dir)
    if not py_files:
        print("No Python files found.")
        return

    issues_found = False
    for file in py_files:
        print(f"Checking {file}...")
        report = run_flake8_on_file(file)
        if report:
            issues_found = True
            print(f"Issues in {file}:\n{report}\n")
        else:
            print(f"No issues found in {file}.\n")

    if not issues_found:
        print("No issues found in any Python files.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python lintreport.py /path/to/codebase")
        sys.exit(1)
    main(sys.argv[1])
