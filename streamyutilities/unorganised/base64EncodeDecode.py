#!/usr/bin/env python3

import base64
import argparse
import sys
import os
import binascii # For specific Base64 decoding errors

def process_base64(mode, input_data_bytes=None, output_filepath=None):
    """
    Processes data for Base64 encoding or decoding.
    input_data_bytes: The raw bytes to process.
    Returns True on success, False on failure.
    """
    processed_output = None

    if mode == 'encode':
        try:
            encoded_bytes = base64.b64encode(input_data_bytes)
            # Base64 encoded output is safe to represent as an ASCII string
            processed_output = encoded_bytes.decode('ascii')
            print("Encoding successful.")
        except Exception as e:
            print(f"Error during Base64 encoding: {e}")
            return False
    elif mode == 'decode':
        try:
            # b64decode expects bytes. If input_data_bytes came from a string, it should be ascii encoded.
            # If from a file, it's already bytes.
            decoded_bytes = base64.b64decode(input_data_bytes)
            processed_output = decoded_bytes # Keep as bytes for output handling
            print("Decoding successful.")
        except binascii.Error as e: # Specific error for invalid Base64
            print(f"Error during Base64 decoding: Invalid Base64 string/data. {e}")
            return False
        except Exception as e:
            print(f"Error during Base64 decoding: {e}")
            return False
    else: # Should not happen due to argparse choices
        print(f"Error: Invalid mode '{mode}'. Choose 'encode' or 'decode'.")
        return False

    # Handle output
    if output_filepath:
        try:
            if mode == 'encode': # Encoded output is text (ASCII string)
                with open(output_filepath, 'w', encoding='ascii') as f:
                    f.write(processed_output)
            elif mode == 'decode': # Decoded output can be any binary data
                with open(output_filepath, 'wb') as f:
                    f.write(processed_output) # processed_output is bytes here
            print(f"Output successfully written to: '{output_filepath}'")
        except IOError as e:
            print(f"Error writing to output file '{output_filepath}': {e}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred while writing to '{output_filepath}': {e}")
            return False
    else: # Print to stdout
        if mode == 'encode':
            print("Encoded output:")
            print(processed_output)
        elif mode == 'decode':
            # Try to print as UTF-8 string; if not, indicate binary
            try:
                print("Decoded output (UTF-8):")
                print(processed_output.decode('utf-8'))
            except UnicodeDecodeError:
                print("Decoded output (likely binary, showing partial representation or info):")
                # Avoid printing raw binary to terminal. Show length or a message.
                print(f"[Binary data: {len(processed_output)} bytes]")
                if sys.stdout.isatty():
                     print("Hint: Use --output-file to save binary data correctly.")
                # For non-tty, printing the representation above is fine.
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Encode or decode data using Base64. Handles text and binary files.",
        epilog='Example: python base64EncodeDecode.py encode --string "hello" --output out.txt'
    )
    parser.add_argument("mode", choices=['encode', 'decode'], help="Operation mode: 'encode' or 'decode'.")

    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--string", metavar="TEXT", help="Input string for encoding/decoding.")
    input_group.add_argument("--input-file", metavar="FILEPATH", help="Path to input file for encoding/decoding.")

    parser.add_argument("--output-file", metavar="FILEPATH", help="Optional: Path to output file.")

    args = parser.parse_args()

    input_bytes_to_process = None

    if args.string is not None:
        print(f"Input from string: '{args.string[:30]}{'...' if len(args.string)>30 else ''}'")
        if args.mode == 'encode':
            # For encoding, the input string must be converted to bytes
            try:
                input_bytes_to_process = args.string.encode('utf-8')
            except UnicodeEncodeError as e: # Should not happen with standard strings
                print(f"Error encoding input string to UTF-8 bytes: {e}")
                exit(1)
        else: # mode == 'decode'
            # For decoding, the input string itself is the Base64 data.
            # b64decode expects bytes, and Base64 strings are ASCII.
            input_bytes_to_process = args.string.encode('ascii')
            # Pad if necessary - Python's b64decode can handle missing padding
            # if len(input_bytes_to_process) % 4 != 0:
            #     input_bytes_to_process += b'=' * (4 - len(input_bytes_to_process) % 4)

    elif args.input_file:
        print(f"Input from file: '{args.input_file}'")
        try:
            # Always read files in binary mode for consistent Base64 operations
            with open(args.input_file, 'rb') as f:
                input_bytes_to_process = f.read()
        except FileNotFoundError:
            print(f"Error: Input file '{args.input_file}' not found.")
            exit(1)
        except IOError as e:
            print(f"Error reading input file '{args.input_file}': {e}")
            exit(1)
        except Exception as e:
            print(f"An unexpected error occurred while reading input file '{args.input_file}': {e}")
            exit(1)

    if input_bytes_to_process is None and args.mode == 'encode': # Should not happen if string or file is required
        print("Error: No input data provided for encoding.")
        exit(1)
    # For decoding, input_bytes_to_process could be empty string from --string "" which is valid b64 for empty bytes

    success = process_base64(args.mode, input_bytes_to_process, args.output_file)

    if success:
        print("\nOperation completed.")
    else:
        print("\nOperation failed.")
        return
