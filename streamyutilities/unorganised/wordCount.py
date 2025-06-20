#!/usr/bin/env python3

import os
import argparse
import re
from collections import Counter
import string

def analyze_file_content(filepath, top_n_words=0):
    """
    Analyzes the content of a single file to count lines, words, characters,
    unique words, average word length, and optionally lists top N frequent words.
    """
    stats = {
        "lines": 0,
        "words": 0,
        "characters": 0,
        "unique_words": 0,
        "avg_word_length": 0.0,
        "word_frequencies": Counter(),
        "top_words_list": []
    }

    total_cleaned_word_length = 0

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                stats["lines"] += 1
                stats["characters"] += len(line) # wc -m behavior (includes newline)

                # For word splitting, use regex to find sequences of word characters.
                # This handles punctuation better than line.split() for word counting.
                # \w typically includes alphanumeric characters and underscore.
                # Convert line to lowercase for consistent word counting for frequency.
                words = re.findall(r'\b\w+\b', line.lower())

                stats["words"] += len(words)
                stats["word_frequencies"].update(words)
                total_cleaned_word_length += sum(map(len, words))

        stats["unique_words"] = len(stats["word_frequencies"])
        stats["avg_word_length"] = total_cleaned_word_length / stats["words"] if stats["words"] else 0

        if top_n_words > 0 and stats["word_frequencies"]:
            stats["top_words_list"] = stats["word_frequencies"].most_common(top_n_words)

        return stats, None # No error

    except FileNotFoundError:
        return None, f"Error: File '{filepath}' not found."
    except IOError as e:
        return None, f"Error reading file '{filepath}': {e}."
    except Exception as e:
        return None, f"An unexpected error occurred with file '{filepath}': {e}."


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Count lines, words, characters, unique words, and analyze word frequency in files.",
        epilog="Example: python wordCount.py report.txt --top-words 10"
    )
    parser.add_argument(
        "filepaths",
        nargs="+",
        help="One or more paths to text files to analyze."
    )
    parser.add_argument(
        "--top-words",
        type=int,
        default=0,
        metavar="N",
        help="Optional: Display the top N most frequent words. Default is 0 (no list)."
    )

    args = parser.parse_args()

    grand_total_lines = 0
    grand_total_words = 0
    grand_total_characters = 0
    files_processed_count = 0

    for filepath_arg in args.filepaths:
        print(f"\n--- Statistics for file: {filepath_arg} ---")

        file_stats, error_message = analyze_file_content(filepath_arg, args.top_words)

        if error_message:
            print(error_message)
            continue

        files_processed_count += 1
        grand_total_lines += file_stats["lines"]
        grand_total_words += file_stats["words"]
        grand_total_characters += file_stats["characters"]

        print(f"  Lines: {file_stats['lines']}")
        print(f"  Words: {file_stats['words']}")
        print(f"  Characters: {file_stats['characters']}")
        print(f"  Unique words: {file_stats['unique_words']}")
        print(f"  Average word length: {file_stats['avg_word_length']:.2f}")

        if file_stats["top_words_list"]:
            print(f"  Top {args.top_words} most frequent words:")
            for word, count in file_stats["top_words_list"]:
                print(f"    - \"{word}\": {count} times")

    if files_processed_count > 1:
        print("\n--- Grand Totals for Processed Files ---")
        print(f"  Total Lines: {grand_total_lines}")
        print(f"  Total Words: {grand_total_words}")
        print(f"  Total Characters: {grand_total_characters}")
        # Note: Grand total for unique words and avg word length across all files combined
        # would require processing all content together, which is not done here for simplicity.
        # The current grand totals are sums of per-file stats for lines, words, chars.

    if files_processed_count == 0 and args.filepaths:
        print("\nNo files were successfully processed.")

    print("\nWord count process complete.")
