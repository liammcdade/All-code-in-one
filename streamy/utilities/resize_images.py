"""
Resizes images from a source directory and saves them to an output directory.

This script requires the Pillow library. Install it using:
    pip install Pillow

Usage:
    python resize_images.py <source_dir> <output_dir> (--width <W> --height <H> | --scale <S>)

Arguments:
    source_dir:       Path to the directory containing original images.
    output_dir:       Path to the directory where resized images will be saved.
    --width W:        Target width for resizing. Must be used with --height.
    --height H:       Target height for resizing. Must be used with --width.
    --scale S:        Percentage to scale images by (e.g., 50 for 50%).
                      Cannot be used with --width/--height.

Supported formats: JPG, PNG, and other formats supported by Pillow.
Files that are not valid images or are unsupported will be skipped.
"""

import argparse
import os
from PIL import Image, UnidentifiedImageError

SUPPORTED_FORMATS = ('.jpg', '.jpeg', '.png')

def resize_image(image_path, output_path, new_width=None, new_height=None, scale_percent=None):
    """Resizes a single image and saves it."""
    try:
        img = Image.open(image_path)
        original_width, original_height = img.size

        if scale_percent:
            if not (0 < scale_percent <= 500): # Allow upscaling up to 500%
                print(f"Warning: Scale percent {scale_percent}% is out of reasonable range (1-500). Skipping {image_path}")
                return False
            new_width = int(original_width * scale_percent / 100)
            new_height = int(original_height * scale_percent / 100)
        elif new_width is None or new_height is None:
            # This case should ideally be caught by argument parsing logic
            print(f"Error: Invalid resize parameters for {image_path}. Width/Height or Scale must be provided.")
            return False

        if new_width <= 0 or new_height <= 0:
            print(f"Warning: Calculated dimensions ({new_width}x{new_height}) are invalid for {image_path}. Skipping.")
            return False

        print(f"Processing {image_path}: original ({original_width}x{original_height}) -> new ({new_width}x{new_height})")

        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        resized_img.save(output_path)
        return True
    except UnidentifiedImageError:
        print(f"Skipping {image_path}: Cannot identify image file or format is not supported.")
        return False
    except FileNotFoundError:
        print(f"Skipping {image_path}: Source file not found (should not happen if script logic is correct).")
        return False
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Resizes images from a source directory.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("source_dir", help="Directory containing original images.")
    parser.add_argument("output_dir", help="Directory to save resized images.")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--width", type=int, help="Target width for resizing (requires --height).")
    group.add_argument("--scale", type=float, help="Percentage to scale images by (e.g., 50 for 50%%).")

    parser.add_argument("--height", type=int, help="Target height for resizing (requires --width).")

    args = parser.parse_args()

    if (args.width is not None and args.height is None) or \
       (args.height is not None and args.width is None):
        parser.error("--width and --height must be used together.")

    if not os.path.isdir(args.source_dir):
        print(f"Error: Source directory '{args.source_dir}' not found.")
        return

    if not os.path.exists(args.output_dir):
        try:
            os.makedirs(args.output_dir)
            print(f"Created output directory: {args.output_dir}")
        except OSError as e:
            print(f"Error: Could not create output directory '{args.output_dir}': {e}")
            return
    elif not os.path.isdir(args.output_dir):
        print(f"Error: Output path '{args.output_dir}' exists but is not a directory.")
        return

    processed_count = 0
    success_count = 0
    skipped_count = 0

    print(f"\nStarting image resizing from '{args.source_dir}' to '{args.output_dir}'.")
    if args.scale:
        print(f"Resizing by: {args.scale}%")
    else:
        print(f"Resizing to: {args.width}x{args.height}")

    for filename in os.listdir(args.source_dir):
        if not any(filename.lower().endswith(ext) for ext in SUPPORTED_FORMATS):
            # print(f"Skipping {filename}: Not a recognized image file extension.")
            continue # Silently skip non-image extensions unless verbose mode is added

        source_filepath = os.path.join(args.source_dir, filename)
        output_filepath = os.path.join(args.output_dir, filename)

        if os.path.isfile(source_filepath):
            processed_count += 1
            if resize_image(source_filepath, output_filepath, args.width, args.height, args.scale):
                success_count += 1
            else:
                skipped_count += 1

    print("\n--- Summary ---")
    print(f"Total files considered (based on extension): {processed_count}") # This might be slightly off if listdir has non-files
    print(f"Successfully resized: {success_count}")
    print(f"Skipped or failed: {skipped_count}")

if __name__ == "__main__":
    main()
