import os
import shutil


def organize_text_files():
    """
    Moves all .txt files from the current directory and its subdirectories
    into a 'textfiles' directory, handling duplicate filenames gracefully.
    """
    target_dir = "textfiles"
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    moved_count = 0
    for root, dirs, files in os.walk("."):
        # Skip the target directory and its subdirectories
        abs_root = os.path.abspath(root)
        abs_target = os.path.abspath(target_dir)
        if abs_root == abs_target or abs_root.startswith(abs_target + os.sep):
            continue
        for file in files:
            # Only process .txt files, skip hidden files
            if file.lower().endswith(".txt") and not file.startswith("."):
                src = os.path.join(root, file)
                # Don't move files already in the target directory
                if os.path.abspath(os.path.dirname(src)) == abs_target:
                    continue
                # Handle duplicate filenames
                dst = os.path.join(target_dir, file)
                counter = 1
                name, ext = os.path.splitext(file)
                while os.path.exists(dst):
                    dst = os.path.join(target_dir, f"{name}_{counter}{ext}")
                    counter += 1
                try:
                    shutil.move(src, dst)
                    moved_count += 1
                    print(f"Moved: {src}  {dst}")
                except Exception as e:
                    print(f"Error moving {src}: {e}")
    print(f"\nDone! Moved {moved_count} text files to {target_dir}/")


if __name__ == "__main__":
    organize_text_files()
