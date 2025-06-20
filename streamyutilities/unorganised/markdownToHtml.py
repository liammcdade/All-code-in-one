#!/usr/bin/env python3

import os
import argparse
import markdown  # Dependency installed via pip


def convert_markdown_to_html(input_filepath, output_filepath=None):
    """
    Reads a Markdown file, converts it to HTML, and saves it.
    """
    # Determine output path if not provided
    if output_filepath is None:
        base, ext = os.path.splitext(input_filepath)
        # Handle common markdown extensions
        if ext.lower() not in [".md", ".markdown", ".mdown", ".mkd"]:
            print(
                f"Warning: Input file '{input_filepath}' does not have a common Markdown extension."
            )
            # Proceed anyway, but the default output name might be less ideal.
        output_filepath = base + ".html"
        print(f"Output HTML file not specified. Defaulting to: '{output_filepath}'")

    try:
        print(f"Reading Markdown content from: '{input_filepath}'")
        with open(input_filepath, "r", encoding="utf-8") as md_file:
            markdown_content = md_file.read()
    except FileNotFoundError:
        print(f"Error: Input Markdown file '{input_filepath}' not found.")
        return False
    except IOError as e:
        print(f"Error reading input Markdown file '{input_filepath}': {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while reading '{input_filepath}': {e}")
        return False

    # Convert Markdown to HTML
    try:
        html_content = markdown.markdown(markdown_content)
    except Exception as e:
        # The markdown library itself might raise errors, though it's usually robust.
        print(f"Error during Markdown to HTML conversion for '{input_filepath}': {e}")
        return False

    # Write the HTML content to the output file
    try:
        print(f"Writing HTML output to: '{output_filepath}'")
        with open(output_filepath, "w", encoding="utf-8") as html_file:
            html_file.write(html_content)
        print(f"Successfully converted '{input_filepath}' to '{output_filepath}'.")
        return True
    except IOError as e:
        print(f"Error writing output HTML file '{output_filepath}': {e}")
        return False
    except Exception as e:
        print(
            f"An unexpected error occurred while writing HTML to '{output_filepath}': {e}"
        )
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert a Markdown file to an HTML file.",
        epilog="Example: python markdownToHtml.py my_doc.md --output my_doc_styled.html",
    )
    parser.add_argument("input_markdown_file", help="Path to the input Markdown file.")
    parser.add_argument(
        "--output",
        metavar="OUTPUT_HTML_FILE",
        help="Optional: Path for the output HTML file. "
        "Defaults to the input filename with an .html extension.",
    )

    args = parser.parse_args()

    print(f"Input Markdown: {args.input_markdown_file}")
    if args.output:
        print(f"Output HTML: {args.output}")

    success = convert_markdown_to_html(args.input_markdown_file, args.output)

    if success:
        print("Markdown to HTML conversion process completed successfully.")
    else:
        print("Markdown to HTML conversion process failed.")
