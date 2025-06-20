import os
import shutil

def organize_text_files():
    # Create the target directory if it doesn't exist
    target_dir = "textfiles"
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    # Counter for moved files
    moved_count = 0
    
    # Walk through all directories and subdirectories
    for root, dirs, files in os.walk('.'):
        # Skip the target directory to prevent moving files we've already moved
        if target_dir in root:
            continue
            
        for file in files:
            # Check if file is a text file (by extension)
            if file.lower().endswith('.txt'):
                # Construct source and destination paths
                src = os.path.join(root, file)
                dst = os.path.join(target_dir, file)
                
                # Handle duplicate filenames
                counter = 1
                while os.path.exists(dst):
                    name, ext = os.path.splitext(file)
                    dst = os.path.join(target_dir, f"{name}_{counter}{ext}")
                    counter += 1
                
                # Move the file
                try:
                    shutil.move(src, dst)
                    moved_count += 1
                    print(f"Moved: {src} → {dst}")
                except Exception as e:
                    print(f"Error moving {src}: {e}")
    
    print(f"\nDone! Moved {moved_count} text files to {target_dir}/")

if __name__ == "__main__":
    organize_text_files()