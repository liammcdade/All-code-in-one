import sys
import types
import traceback

# Import all functions from the unified tools file
import importlib.util
import os

# Path to the unified tools file
TOOLS_PATH = os.path.join(os.path.dirname(__file__), 'all_streamyutilities_tools.py')

# Dynamically load the module
spec = importlib.util.spec_from_file_location("all_streamyutilities_tools", TOOLS_PATH)
tools = importlib.util.module_from_spec(spec)
sys.modules["all_streamyutilities_tools"] = tools
spec.loader.exec_module(tools)

# List of all function names to test (update if new tools are added)
function_names = [
    'datetime_countdown',
    'text_case_converter',
    'unit_distance_converter',
    'unorganised_word_count',
    'csv_to_json_cli',
    'disk_space_cli',
    'dir_size_cli',
    'extract_emails_cli',
    'find_duplicates_cli',
    'env_vars_cli',
    'empty_trash_cli',
    'create_backup_cli',
    'list_files_by_type_cli',
    'markdown_to_html_cli',
    'mem_usage_cli',
    'my_ip_cli',
    'organize_downloads_cli',
    'path_viewer_cli',
    'pomodoro_timer_cli',
    'qr_code_generator_cli',
    'safe_delete_cli',
    'sys_info_cli',
    'temp_server_cli',
    'text_search_replace_cli',
    'todo_manager_cli',
    'uptime_cli',
    'url_shortener_cli',
    'venv_helper_cli',
    'textfile_cleaner_cli',
]

report = []

for fname in function_names:
    func = getattr(tools, fname, None)
    if not isinstance(func, types.FunctionType):
        report.append(f"Function '{fname}' not found or not callable.")
        continue
    try:
        # Many functions require user input; simulate with patching input if possible
        # For now, just call and catch errors (will hang if input is required)
        print(f"Testing {fname}...")
        func()
        report.append(f"{fname}: SUCCESS")
    except Exception as e:
        tb = traceback.format_exc()
        report.append(f"{fname}: ERROR\n{tb}")

print("\n--- TEST REPORT ---")
for line in report:
    print(line)
