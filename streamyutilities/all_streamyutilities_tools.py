# All StreamyUtilities Tools Unified Script
# This script combines all tools from the streamyutilities folder and subfolders into a single file.
# Each tool is accessible via a master CLI menu.

# --- Datetime Tools ---
def datetime_countdown():
    import datetime
    import time
    def get_target_datetime():
        while True:
            datetime_str = input("Enter target date and time (YYYY-MM-DD HH:MM:SS): ")
            try:
                target_dt = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
                if target_dt > datetime.datetime.now():
                    return target_dt
                else:
                    print("Error: Target date and time must be in the future. Please try again.")
            except ValueError:
                print("Error: Invalid date and time format. Please use YYYY-MM-DD HH:MM:SS. Please try again.")
    def countdown(target_dt):
        print("\nStarting countdown...")
        while True:
            now = datetime.datetime.now()
            remaining_time = target_dt - now
            if remaining_time.total_seconds() <= 0:
                print("\nCountdown complete!")
                break
            days = remaining_time.days
            seconds_in_day = remaining_time.seconds
            hours = seconds_in_day // 3600
            minutes = (seconds_in_day % 3600) // 60
            seconds = seconds_in_day % 60
            print(f"Time remaining: {days} days, {hours:02} hours, {minutes:02} minutes, {seconds:02} seconds", end="\r")
            time.sleep(1)
    print("--- Countdown Timer ---")
    if (target_datetime := get_target_datetime()):
        countdown(target_datetime)

# --- Text Tools ---
def text_case_converter():
    def to_uppercase(input_text):
        return input_text.upper()
    def to_lowercase(input_text):
        return input_text.lower()
    def to_titlecase(input_text):
        return input_text.title()
    text = input("Enter text: ")
    print("Choose conversion:")
    print("1. Uppercase\n2. Lowercase\n3. Title Case")
    choice = input("Enter choice (1-3): ")
    if choice == "1":
        result = to_uppercase(text)
        print(f"Result: {result}")
    elif choice == "2":
        result = to_lowercase(text)
        print(f"Result: {result}")
    elif choice == "3":
        result = to_titlecase(text)
        print(f"Result: {result}")
    else:
        print("Invalid choice.")

# --- Unit Conversion Tools ---
def unit_distance_converter():
    class UniversalDistanceConverter:
        CONVERSION_FACTORS = {
            "nm": 1e-9, "[1m[0m b5m": 1e-6, "mm": 1e-3, "cm": 1e-2, "m": 1, "km": 1e3,
            "in": 0.0254, "ft": 0.3048, "yd": 0.9144, "mi": 1609.344,
            "au": 149597870700, "ly": 9460730472580800, "pc": 3.08567758149137e16,
        }
        UNIT_ALIASES = {
            "nanometer": "nm", "nanometers": "nm", "micron": " b5m", "microns": " b5m", "micrometer": " b5m", "micrometers": " b5m",
            "millimeter": "mm", "millimeters": "mm", "centimeter": "cm", "centimeters": "cm", "meter": "m", "meters": "m", "kilometer": "km", "kilometers": "km",
            "inch": "in", "inches": "in", "foot": "ft", "feet": "ft", "yard": "yd", "yards": "yd", "mile": "mi", "miles": "mi",
            "astronomical unit": "au", "astronomical units": "au", "light year": "ly", "light years": "ly", "parsec": "pc", "parsecs": "pc",
        }
        @classmethod
        def convert(cls, value, from_unit, to_unit):
            from_unit = cls._normalize_unit(from_unit)
            to_unit = cls._normalize_unit(to_unit)
            valid_units = cls.CONVERSION_FACTORS.keys()
            if from_unit not in valid_units or to_unit not in valid_units:
                raise ValueError(f"Invalid unit. Supported units are: {', '.join(valid_units)}")
            meters = value * cls.CONVERSION_FACTORS[from_unit]
            return meters / cls.CONVERSION_FACTORS[to_unit]
        @classmethod
        def _normalize_unit(cls, unit):
            unit = unit.lower().strip()
            return cls.UNIT_ALIASES.get(unit, unit)
    print("Distance Converter")
    value = float(input("Enter value: "))
    from_unit = input("From unit: ")
    to_unit = input("To unit: ")
    try:
        result = UniversalDistanceConverter.convert(value, from_unit, to_unit)
        print(f"{value} {from_unit} = {result} {to_unit}")
    except Exception as e:
        print(f"Error: {e}")

# --- Unorganised Tools ---
def unorganised_word_count():
    import re
    from collections import Counter
    def analyze_file_content(filepath, top_n_words=0):
        stats = {
            "lines": 0,
            "words": 0,
            "characters": 0,
            "unique_words": 0,
            "avg_word_length": 0.0,
            "word_frequencies": Counter(),
            "top_words_list": [],
        }
        total_cleaned_word_length = 0
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    stats["lines"] += 1
                    stats["characters"] += len(line)
                    words = re.findall(r"\b\w+\b", line.lower())
                    stats["words"] += len(words)
                    stats["word_frequencies"].update(words)
                    total_cleaned_word_length += sum(map(len, words))
            stats["unique_words"] = len(stats["word_frequencies"])
            stats["avg_word_length"] = (
                total_cleaned_word_length / stats["words"] if stats["words"] else 0
            )
            if top_n_words > 0 and stats["word_frequencies"]:
                stats["top_words_list"] = stats["word_frequencies"].most_common(top_n_words)
            return stats, None
        except FileNotFoundError:
            return None, f"Error: File '{filepath}' not found."
        except IOError as e:
            return None, f"Error reading file '{filepath}': {e}."
        except Exception as e:
            return None, f"An unexpected error occurred with file '{filepath}': {e}."
    print("Word Count Tool")
    filepath = input("Enter path to text file: ")
    try:
        top_n = int(input("Show top N most frequent words (0 for none): "))
    except ValueError:
        top_n = 0
    file_stats, error_message = analyze_file_content(filepath, top_n)
    if error_message:
        print(error_message)
        return
    print(f"  Lines: {file_stats['lines']}")
    print(f"  Words: {file_stats['words']}")
    print(f"  Characters: {file_stats['characters']}")
    print(f"  Unique words: {file_stats['unique_words']}")
    print(f"  Average word length: {file_stats['avg_word_length']:.2f}")
    if file_stats["top_words_list"]:
        print(f"  Top {top_n} most frequent words:")
        for word, count in file_stats["top_words_list"]:
            print(f'    - "{word}": {count} times')
    print("Word count process complete.")

# --- UNORGANISED TOOLS ---

def csv_to_json_cli():
    # ...csvToJson.py logic...
    import csv, json, os
    input_filepath = input("Enter path to input CSV file: ")
    output_filepath = input("Enter path for output JSON file: ")
    delimiter = input("Enter delimiter (default ','): ") or ","
    try:
        with open(input_filepath, mode="r", newline="", encoding="utf-8") as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=delimiter)
            data_list = [row for row in csv_reader]
        with open(output_filepath, mode="w", encoding="utf-8") as json_file:
            json.dump(data_list, json_file, indent=4)
        print(f"Successfully converted '{input_filepath}' to '{output_filepath}'.")
    except Exception as e:
        print(f"Error: {e}")

def disk_space_cli():
    # ...diskSpace.py logic...
    import psutil, os
    def bytes_to_human_readable(n_bytes, suffix="B", precision=1):
        factor = 1024
        for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
            if abs(n_bytes) < factor:
                return f"{n_bytes:.{precision}f}{unit}{suffix}"
            n_bytes /= factor
        return f"{n_bytes:.{precision}f}Yi{suffix}"
    partitions = psutil.disk_partitions(all=False)
    for part in partitions:
        usage = psutil.disk_usage(part.mountpoint)
        print(f"{part.device} {part.mountpoint} {part.fstype} | Total: {bytes_to_human_readable(usage.total)}, Used: {bytes_to_human_readable(usage.used)}, Free: {bytes_to_human_readable(usage.free)}, Use%: {usage.percent}%")

def dir_size_cli():
    # ...dirSize.py logic...
    import os
    def get_dir_tree_size(path):
        total_size = 0
        for dirpath, _, filenames in os.walk(path):
            for f_name in filenames:
                fp = os.path.join(dirpath, f_name)
                if not os.path.islink(fp):
                    try:
                        total_size += os.path.getsize(fp)
                    except OSError:
                        pass
        return total_size
    base_dir = input("Enter directory to scan (default '.'): ") or "."
    size = get_dir_tree_size(base_dir)
    print(f"Total size of '{base_dir}': {size} bytes")

def extract_emails_cli():
    # ...extractEmails.py logic...
    import re
    EMAIL_REGEX = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}")
    files = input("Enter file paths (comma separated): ").split(",")
    emails = set()
    for filepath in files:
        try:
            with open(filepath.strip(), "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            emails.update(EMAIL_REGEX.findall(content))
        except Exception as e:
            print(f"Error: {e}")
    print("Found emails:", *emails, sep="\n")

def find_duplicates_cli():
    # ...findDuplicates.py logic...
    import os, hashlib
    directory = input("Enter directory to scan for duplicates: ")
    files_by_size = {}
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            try:
                size = os.path.getsize(filepath)
                files_by_size.setdefault(size, []).append(filepath)
            except OSError:
                continue
    duplicates = []
    for size, files in files_by_size.items():
        if len(files) < 2:
            continue
        hashes = {}
        for filepath in files:
            try:
                with open(filepath, "rb") as f:
                    filehash = hashlib.md5(f.read()).hexdigest()
                hashes.setdefault(filehash, []).append(filepath)
            except Exception:
                continue
        for group in hashes.values():
            if len(group) > 1:
                duplicates.append(group)
    if duplicates:
        print("Found duplicate files:")
        for group in duplicates:
            print("--- Group ---")
            for filepath in group:
                print(filepath)
    else:
        print("No duplicate files found.")

def env_vars_cli():
    # ...envVars.py logic...
    import os, json
    filter_str = input("Filter string (leave blank for all): ")
    fmt = input("Format (list/json/export): ") or "list"
    case_sensitive = input("Case sensitive? (y/n): ").lower() == "y"
    envs = {k: v for k, v in os.environ.items() if (filter_str in (k if case_sensitive else k.lower()) or filter_str in (v if case_sensitive else v.lower()))} if filter_str else dict(os.environ)
    if fmt == "json":
        print(json.dumps(envs, indent=4))
    elif fmt == "export":
        for k, v in envs.items():
            print(f"export {k}='{v}'")
    else:
        for k, v in envs.items():
            print(f"{k}={v}")

def empty_trash_cli():
    # ...emptyTrash.py logic (list only)...
    import os
    trash_dir = os.path.expanduser("~/.local/share/streamyutilities_trash/files")
    if not os.path.isdir(trash_dir):
        print("Trash directory does not exist.")
        return
    files = os.listdir(trash_dir)
    if not files:
        print("Trash is empty.")
    else:
        print("Files in trash:")
        for f in files:
            print(f)

def create_backup_cli():
    # ...createBackup.py logic...
    import shutil, os
    src = input("Enter source file or directory: ")
    dest = input("Enter destination directory (leave blank for default): ") or None
    if not os.path.exists(src):
        print(f"Source '{src}' does not exist.")
        return
    if os.path.isfile(src):
        name, ext = os.path.splitext(os.path.basename(src))
        import datetime
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{name}_backup_{ts}{ext if ext else '.bak'}"
        backup_path = os.path.join(dest or os.path.dirname(src), backup_name)
        shutil.copy2(src, backup_path)
        print(f"Backed up file to {backup_path}")
    elif os.path.isdir(src):
        import zipfile
        import datetime
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{os.path.basename(src)}_backup_{ts}.zip"
        backup_path = os.path.join(dest or os.path.dirname(src), backup_name)
        with zipfile.ZipFile(backup_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for root, _, files in os.walk(src):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, src)
                    zf.write(file_path, arcname)
        print(f"Backed up directory to {backup_path}")
    else:
        print("Source is neither file nor directory.")

def list_files_by_type_cli():
    # ...listFilesByType.py logic...
    import os
    directory = input("Enter directory: ")
    ext = input("Enter file extension (e.g. .txt): ")
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(ext):
                print(os.path.join(root, file))

def markdown_to_html_cli():
    # ...markdownToHtml.py logic...
    import markdown, os
    input_file = input("Enter Markdown file: ")
    output_file = input("Enter output HTML file (leave blank for default): ") or None
    with open(input_file, "r", encoding="utf-8") as f:
        md_content = f.read()
    html_content = markdown.markdown(md_content)
    if not output_file:
        output_file = os.path.splitext(input_file)[0] + ".html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Converted '{input_file}' to '{output_file}'")

def mem_usage_cli():
    # ...memUsage.py logic...
    import psutil
    vmem = psutil.virtual_memory()
    print(f"Total: {vmem.total} bytes, Used: {vmem.used} bytes, Free: {vmem.available} bytes, Percent: {vmem.percent}%")

def my_ip_cli():
    # ...myIp.py logic...
    import urllib.request
    try:
        ip = urllib.request.urlopen("https://api.ipify.org").read().decode("utf-8")
        print(f"Your public IP is: {ip}")
    except Exception as e:
        print(f"Error: {e}")

def organize_downloads_cli():
    # ...organizeDownloads.py logic...
    import os, shutil
    downloads_dir = input("Enter downloads directory: ")
    if not os.path.isdir(downloads_dir):
        print("Directory not found.")
        return
    for file in os.listdir(downloads_dir):
        src = os.path.join(downloads_dir, file)
        if os.path.isfile(src):
            ext = os.path.splitext(file)[1].lower()
            if ext in ['.jpg', '.jpeg', '.png', '.gif']:
                folder = 'Images'
            elif ext in ['.pdf', '.docx', '.txt']:
                folder = 'Documents'
            else:
                folder = 'Other'
            dest_folder = os.path.join(downloads_dir, folder)
            os.makedirs(dest_folder, exist_ok=True)
            shutil.move(src, os.path.join(dest_folder, file))
    print("Organization complete.")

def path_viewer_cli():
    # ...pathViewer.py logic...
    import os
    path = os.getenv("PATH")
    print("System PATH:")
    for i, p in enumerate(path.split(os.pathsep)):
        print(f"{i+1}: {p}")

def pomodoro_timer_cli():
    # ...pomodoroTimer.py logic...
    import time
    work = int(input("Work duration (minutes): ") or 25)
    short_break = int(input("Short break (minutes): ") or 5)
    long_break = int(input("Long break (minutes): ") or 15)
    sessions = int(input("Sessions before long break: ") or 4)
    for i in range(sessions):
        print(f"Work session {i+1} started.")
        time.sleep(work * 60)
        print("Work session ended. Take a short break.")
        time.sleep(short_break * 60)
    print("Take a long break!")
    time.sleep(long_break * 60)
    print("Pomodoro complete.")

def qr_code_generator_cli():
    # ...qrCodeGenerator.py logic...
    import qrcode
    data = input("Enter data for QR code: ")
    output = input("Enter output file (e.g. qr.png): ")
    img = qrcode.make(data)
    img.save(output)
    print(f"QR code saved to {output}")

def safe_delete_cli():
    # ...safeDelete.py logic...
    import os, shutil
    trash_dir = os.path.expanduser("~/.local/share/streamyutilities_trash/files")
    os.makedirs(trash_dir, exist_ok=True)
    paths = input("Enter file(s) or folder(s) to delete (comma separated): ").split(",")
    for path in paths:
        path = path.strip()
        if os.path.exists(path):
            shutil.move(path, os.path.join(trash_dir, os.path.basename(path)))
            print(f"Moved '{path}' to trash.")
        else:
            print(f"'{path}' not found.")

def sys_info_cli():
    # ...sysInfo.py logic...
    import platform, socket
    print(f"OS: {platform.system()} {platform.release()} {platform.version()}")
    print(f"Hostname: {socket.gethostname()}")
    print(f"Machine: {platform.machine()}")
    print(f"Processor: {platform.processor()}")

def temp_server_cli():
    # ...tempServer.py logic...
    import http.server, socketserver
    port = int(input("Enter port (default 8000): ") or 8000)
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving at port {port}")
        httpd.serve_forever()

def text_search_replace_cli():
    # ...textSearchReplace.py logic...
    import os
    search = input("Enter search string: ")
    replace = input("Enter replacement string: ")
    file = input("Enter file to process: ")
    with open(file, "r", encoding="utf-8") as f:
        content = f.read()
    new_content = content.replace(search, replace)
    with open(file, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Replaced all occurrences of '{search}' with '{replace}' in '{file}'.")

def todo_manager_cli():
    # ...todoManager.py logic...
    import os, json
    todo_file = os.path.expanduser("~/.streamyutilities_todos.json")
    if not os.path.exists(todo_file):
        with open(todo_file, "w") as f:
            json.dump([], f)
    print("1. Add Task\n2. List Tasks\n3. Mark Done\n4. Remove Task\n5. Edit Task")
    choice = input("Choose: ")
    with open(todo_file, "r") as f:
        tasks = json.load(f)
    if choice == "1":
        desc = input("Task description: ")
        tasks.append({"id": len(tasks)+1, "description": desc, "status": "pending"})
        with open(todo_file, "w") as f:
            json.dump(tasks, f, indent=4)
        print("Task added.")
    elif choice == "2":
        for t in tasks:
            print(f"{t['id']}: {t['description']} [{t['status']}]")
    elif choice == "3":
        tid = int(input("Task ID to mark done: "))
        for t in tasks:
            if t['id'] == tid:
                t['status'] = 'completed'
        with open(todo_file, "w") as f:
            json.dump(tasks, f, indent=4)
        print("Task marked as done.")
    elif choice == "4":
        tid = int(input("Task ID to remove: "))
        tasks = [t for t in tasks if t['id'] != tid]
        with open(todo_file, "w") as f:
            json.dump(tasks, f, indent=4)
        print("Task removed.")
    elif choice == "5":
        tid = int(input("Task ID to edit: "))
        for t in tasks:
            if t['id'] == tid:
                t['description'] = input("New description: ")
        with open(todo_file, "w") as f:
            json.dump(tasks, f, indent=4)
        print("Task edited.")
    else:
        print("Invalid choice.")

def uptime_cli():
    # ...uptime.py logic...
    import psutil, datetime
    boot = datetime.datetime.fromtimestamp(psutil.boot_time())
    now = datetime.datetime.now()
    uptime = now - boot
    print(f"System Uptime: {uptime}")

def url_shortener_cli():
    # ...urlShortenerClient.py logic...
    import urllib.request, urllib.parse
    url = input("Enter URL to shorten: ")
    api = f"http://tinyurl.com/api-create.php?url={urllib.parse.quote(url)}"
    short = urllib.request.urlopen(api).read().decode("utf-8")
    print(f"Shortened URL: {short}")

def venv_helper_cli():
    # ...venvHelper.py logic...
    print("1. Create venv\n2. List venvs\n3. Remove venv")
    choice = input("Choose: ")
    import os, shutil, sys
    venv_dir = os.path.expanduser("~/.virtualenvs")
    if not os.path.exists(venv_dir):
        os.makedirs(venv_dir)
    if choice == "1":
        name = input("Venv name: ")
        import subprocess
        subprocess.run([sys.executable, "-m", "venv", os.path.join(venv_dir, name)])
        print(f"Created venv '{name}'")
    elif choice == "2":
        for d in os.listdir(venv_dir):
            print(d)
    elif choice == "3":
        name = input("Venv name to remove: ")
        shutil.rmtree(os.path.join(venv_dir, name))
        print(f"Removed venv '{name}'")
    else:
        print("Invalid choice.")

def textfile_cleaner_cli():
    # ...textfilecleaner.py logic...
    import os, shutil
    target_dir = "textfiles"
    os.makedirs(target_dir, exist_ok=True)
    moved_count = 0
    for root, dirs, files in os.walk("."):
        abs_root = os.path.abspath(root)
        abs_target = os.path.abspath(target_dir)
        if abs_root == abs_target or abs_root.startswith(abs_target + os.sep):
            continue
        for file in files:
            if file.lower().endswith(".txt") and not file.startswith("."):
                src = os.path.join(root, file)
                if os.path.abspath(os.path.dirname(src)) == abs_target:
                    continue
                dst = os.path.join(target_dir, file)
                counter = 1
                name, ext = os.path.splitext(file)
                while os.path.exists(dst):
                    dst = os.path.join(target_dir, f"{name}_{counter}{ext}")
                    counter += 1
                shutil.move(src, dst)
                moved_count += 1
                print(f"Moved: {src} -> {dst}")
    print(f"Done! Moved {moved_count} text files to {target_dir}/")

if __name__ == "__main__":
    print("All StreamyUtilities Tools - Unified Menu")
    print("1. Countdown Timer\n2. Case Converter\n3. Distance Converter\n4. Word Count\n5. CSV to JSON\n6. Disk Space\n7. Directory Size\n8. Extract Emails\n9. Find Duplicates\n10. Environment Variables\n11. Empty Trash\n12. Create Backup\n13. List Files by Type\n14. Markdown to HTML\n15. Memory Usage\n16. My IP\n17. Organize Downloads\n18. Path Viewer\n19. Pomodoro Timer\n20. QR Code Generator\n21. Safe Delete\n22. System Info\n23. Temporary Server\n24. Text Search and Replace\n25. Todo Manager\n26. Uptime\n27. URL Shortener\n28. Virtual Environment Helper\n29. Textfile Cleaner")
    choice = input("Select a tool (number): ")
    if choice == "1":
        datetime_countdown()
    elif choice == "2":
        text_case_converter()
    elif choice == "3":
        unit_distance_converter()
    elif choice == "4":
        unorganised_word_count()
    elif choice == "5":
        csv_to_json_cli()
    elif choice == "6":
        disk_space_cli()
    elif choice == "7":
        dir_size_cli()
    elif choice == "8":
        extract_emails_cli()
    elif choice == "9":
        find_duplicates_cli()
    elif choice == "10":
        env_vars_cli()
    elif choice == "11":
        empty_trash_cli()
    elif choice == "12":
        create_backup_cli()
    elif choice == "13":
        list_files_by_type_cli()
    elif choice == "14":
        markdown_to_html_cli()
    elif choice == "15":
        mem_usage_cli()
    elif choice == "16":
        my_ip_cli()
    elif choice == "17":
        organize_downloads_cli()
    elif choice == "18":
        path_viewer_cli()
    elif choice == "19":
        pomodoro_timer_cli()
    elif choice == "20":
        qr_code_generator_cli()
    elif choice == "21":
        safe_delete_cli()
    elif choice == "22":
        sys_info_cli()
    elif choice == "23":
        temp_server_cli()
    elif choice == "24":
        text_search_replace_cli()
    elif choice == "25":
        todo_manager_cli()
    elif choice == "26":
        uptime_cli()
    elif choice == "27":
        url_shortener_cli()
    elif choice == "28":
        venv_helper_cli()
    elif choice == "29":
        textfile_cleaner_cli()
    else:
        print("Invalid choice or tool not yet implemented.")