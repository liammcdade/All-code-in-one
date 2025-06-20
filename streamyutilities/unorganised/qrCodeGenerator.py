#!/usr/bin/env python3

import argparse
import sys
import os

try:
    import qrcode
    # For SVG, qrcode library can use different factories.
    # SvgPathImage is generally good as it creates a scalable path-based SVG.
    # Other options include SvgImage and SvgFragmentImage.
    import qrcode.image.svg
except ImportError:
    print("Error: The 'qrcode' library is required. Please install it (e.g., 'pip install \"qrcode[pil]\"').", file=sys.stderr)
    sys.exit(1)

DEFAULT_BOX_SIZE = 10
DEFAULT_BORDER_SIZE = 4
DEFAULT_OUTPUT_FORMAT = "png" # If not inferable from filename

def generate_qr(data_to_encode, output_filepath, image_format_str, box_s, border_s):
    """
    Generates a QR code and saves it to the specified file.
    """
    print(f"Generating QR code for data (first 50 chars): '{data_to_encode[:50]}{'...' if len(data_to_encode) > 50 else ''}'")
    print(f"Output file: '{output_filepath}', Format: {image_format_str.upper()}")
    print(f"Box size: {box_s}, Border: {border_s}")

    qr = qrcode.QRCode(
        version=None, # Auto-determine version based on data size
        error_correction=qrcode.constants.ERROR_CORRECT_M, # M = ~15% error correction
        box_size=box_s,
        border=border_s,
    )
    qr.add_data(data_to_encode)
    qr.make(fit=True)

    try:
        img = None
        if image_format_str.lower() == 'svg':
            # Using SvgPathImage for scalable SVG (paths instead of rects)
            img = qr.make_image(image_factory=qrcode.image.svg.SvgPathImage)
        elif image_format_str.lower() in ['png', 'jpg', 'jpeg', 'bmp', 'gif', 'tiff']:
            # Pillow is used by default for these raster formats
            img = qr.make_image(fill_color="black", back_color="white")
        else:
            print(f"Error: Unsupported image format '{image_format_str}'. Supported: PNG, JPEG, BMP, GIF, TIFF, SVG.", file=sys.stderr)
            return False

        with open(output_filepath, 'wb') as f: # Open in binary mode for Pillow and SVG factory
            img.save(f, kind=image_format_str.upper() if image_format_str.lower() != 'svg' else None)
            # For SVG, kind is not needed by SvgPathImage's save method directly.
            # For Pillow, 'kind' helps ensure format.

        print(f"QR code successfully saved to '{output_filepath}'.")
        return True

    except Exception as e:
        print(f"Error generating or saving QR code: {e}", file=sys.stderr)
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a QR code from text or file input.",
        epilog='Example: python qrCodeGenerator.py "Hello World" --output qr.png --box-size 10'
    )

    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("data", nargs="?", default=None, help="Text data to encode in the QR code (if --input-file is not used).")
    input_group.add_argument("--input-file", metavar="FILEPATH", help="Path to a file containing data to encode.")

    parser.add_argument("--output", metavar="OUTPUT_FILE", required=True, help="Path to save the generated QR code image (e.g., my_qr.png, qr.svg).")

    parser.add_argument(
        "--format",
        metavar="FORMAT",
        help="Image format (e.g., PNG, SVG, JPEG). If omitted, inferred from output file extension, defaulting to PNG."
    )
    parser.add_argument(
        "--box-size",
        type=int,
        default=DEFAULT_BOX_SIZE,
        help=f"Size of each box (pixel) in the QR code. Default: {DEFAULT_BOX_SIZE}."
    )
    parser.add_argument(
        "--border",
        type=int,
        default=DEFAULT_BORDER_SIZE,
        help=f"Thickness of the border around the QR code (in boxes). Default: {DEFAULT_BORDER_SIZE} (minimum is 4 for QR spec if not version 1)."
    )

    args = parser.parse_args()

    # Determine input data
    input_data_str = ""
    if args.input_file:
        try:
            with open(args.input_file, 'r', encoding='utf-8') as f:
                input_data_str = f.read()
            print(f"Read data from input file: '{args.input_file}'")
        except FileNotFoundError:
            print(f"Error: Input file '{args.input_file}' not found.", file=sys.stderr)
            sys.exit(1)
        except IOError as e:
            print(f"Error reading input file '{args.input_file}': {e}", file=sys.stderr)
            sys.exit(1)
    elif args.data is not None:
        input_data_str = args.data
    else: # Should be caught by argparse if group is required and nargs='?' for data
        parser.error("No data provided. Use positional argument or --input-file.")


    # Determine output format
    final_image_format = args.format
    if not final_image_format: # If format not specified, infer from output filename
        _, ext = os.path.splitext(args.output)
        if ext:
            final_image_format = ext[1:].lower() # Remove dot and lowercase
        else: # No extension, use default
            final_image_format = DEFAULT_OUTPUT_FORMAT
            print(f"No output file extension or --format given. Defaulting to format: {DEFAULT_OUTPUT_FORMAT.upper()}")
            # Optionally append default extension to output filename if none provided
            # args.output = args.output + "." + DEFAULT_OUTPUT_FORMAT

    if not final_image_format: # Should not happen if default is set
         print("Error: Could not determine output image format. Please use --format or provide a file extension.", file=sys.stderr)
         sys.exit(1)


    success = generate_qr(
        input_data_str,
        args.output,
        final_image_format,
        args.box_size,
        args.border
    )

    if success:
        print("QR code generation process complete.")
        return
    else:
        print("QR code generation failed.", file=sys.stderr)
        return
