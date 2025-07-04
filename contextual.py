#!/usr/bin/env python3
# contextual.py
"""
contextual.py - A CLI tool to find and display context for Python symbols.

This tool takes a Python symbol name (function, class, variable) and a codebase path
as input. It then traverses the Python files in the specified path to:
1. Find the definition of the symbol using Abstract Syntax Trees (AST).
2. Extract its docstring and any preceding comments.
3. Find usage examples of the symbol across the project, also using AST.
4. If an exact match for the symbol is not found, it suggests similar symbol names
   found in the codebase (fuzzy matching).
5. Display the gathered information in a clear, formatted way on the terminal.

It uses Python's built-in `ast` module for static code analysis and `argparse`
for command-line argument parsing. `difflib` is used for fuzzy matching.
"""

import argparse
import ast
import os
import difflib

def main():
    parser = argparse.ArgumentParser(description="Finds and displays context for a Python symbol in a codebase.")
    parser.add_argument("symbol_name", help="The name of the function, class, or variable to search for.")
    parser.add_argument("path", nargs="?", default=".", help="The path to the codebase directory (defaults to current directory).")

    args = parser.parse_args()

    # The initial print is now part of find_symbol_context
    # print(f"Searching for symbol: {args.symbol_name} in path: {args.path}")
    results = find_symbol_context(args.symbol_name, args.path)
    results['searched_symbol_name'] = args.symbol_name # Add for display_results
    display_results(results)

def find_python_files(path):
    """Recursively finds all Python files in the given directory."""
    python_files = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    return python_files

def find_symbol_context(symbol_name, path):
    """
    Finds the definition and usages of a symbol in the given path.
    This is a placeholder and will be implemented in subsequent steps.
    """
    print(f"Searching for symbol: {symbol_name} in path: {path}")

    python_files = find_python_files(path)
    definition_info = None
    all_defined_symbols = set()

    for py_file in python_files:
        try:
            with open(py_file, "r", encoding="utf-8") as source_file:
                source_code = source_file.read()
                tree = ast.parse(source_code, filename=py_file)

                for node in ast.walk(tree):
                    # Collect all defined names for fuzzy matching
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                        all_defined_symbols.add(node.name)
                    elif isinstance(node, ast.Assign):
                        for target in node.targets:
                            if isinstance(target, ast.Name):
                                all_defined_symbols.add(target.id)
                            elif isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name):
                                # Could be a class variable or instance variable, simple approach for now
                                all_defined_symbols.add(f"{target.value.id}.{target.attr}")


                    # Check for the specific symbol definition
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == symbol_name:
                        definition_info = {
                            "type": "Function",
                            "name": node.name,
                            "file_path": py_file,
                            "line_number": node.lineno,
                            "docstring": ast.get_docstring(node),
                            "comments": get_preceding_comments(source_code, node.lineno)
                        }
                        break  # Found the primary definition
                    elif isinstance(node, ast.ClassDef) and node.name == symbol_name:
                        definition_info = {
                            "type": "Class",
                            "name": node.name,
                            "file_path": py_file,
                            "line_number": node.lineno,
                            "docstring": ast.get_docstring(node),
                            "comments": get_preceding_comments(source_code, node.lineno)
                        }
                        break  # Found the primary definition
                    elif isinstance(node, ast.Assign):
                        for target in node.targets:
                            if isinstance(target, ast.Name) and target.id == symbol_name:
                                definition_info = {
                                    "type": "Variable",
                                    "name": target.id,
                                    "file_path": py_file,
                                    "line_number": node.lineno,
                                    "docstring": None, # Variables don't have docstrings in the same way
                                    "comments": get_preceding_comments(source_code, node.lineno)
                                }
                                break # Found the primary definition
                        if definition_info and definition_info["name"] == symbol_name: # ensure we break outer loop if var found
                            break
            if definition_info and definition_info["name"] == symbol_name: # ensure we break outer loop if symbol found
                break
        except Exception as e:
            print(f"Error parsing {py_file}: {e}")
            continue

    unique_usages = set() # Use a set to store unique usages
    if definition_info: # Only search for usages if a definition was found
        for py_file in python_files:
            try:
                with open(py_file, "r", encoding="utf-8") as source_file:
                    source_code = source_file.read()
                    # Avoid reprocessing the definition file if we only want usages from other files
                    # For now, we'll include usages from the definition file as well.
                    # if py_file == definition_info["file_path"]:
                    #     continue

                    tree = ast.parse(source_code, filename=py_file)
                    lines_with_source = source_code.splitlines()

                    for node in ast.walk(tree):
                        # Skip the definition node itself if it's in the same file
                        # Also ensure the node type is one that would have a lineno and could be a definition
                        if hasattr(node, 'lineno') and py_file == definition_info["file_path"] and node.lineno == definition_info["line_number"]:
                            if (isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.name == symbol_name) or \
                               (isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == symbol_name for t in node.targets)):
                                continue

                        # Check for ast.Name nodes (variables, function calls)
                        if isinstance(node, ast.Name) and node.id == symbol_name:
                            unique_usages.add((py_file, node.lineno, lines_with_source[node.lineno-1].strip()))
                        # Check for ast.Attribute nodes (e.g., object.symbol_name)
                        elif isinstance(node, ast.Attribute) and node.attr == symbol_name:
                            unique_usages.add((py_file, node.lineno, lines_with_source[node.lineno-1].strip()))
                        # Potentially extend to ast.Call if symbol_name is a function being called
                        # For ast.Call, node.func could be ast.Name or ast.Attribute
                        elif isinstance(node, ast.Call):
                            func_node = node.func
                            if isinstance(func_node, ast.Name) and func_node.id == symbol_name:
                                unique_usages.add((py_file, node.lineno, lines_with_source[node.lineno-1].strip()))
                            elif isinstance(func_node, ast.Attribute) and func_node.attr == symbol_name:
                                unique_usages.add((py_file, node.lineno, lines_with_source[node.lineno-1].strip()))
            except Exception as e:
                print(f"Error parsing {py_file} for usages: {e}")
                continue

    # Convert set of tuples to list of dictionaries, sorted for consistency
    usages = [{"file_path": u[0], "line_number": u[1], "code_line": u[2]} for u in sorted(list(unique_usages))]

    fuzzy_matches = []
    if not definition_info and all_defined_symbols:
        # Use difflib to find close matches for the symbol name
        # The list `all_defined_symbols` was populated during the definition search pass
        fuzzy_matches = difflib.get_close_matches(symbol_name, list(all_defined_symbols), n=5, cutoff=0.6)

    return {"definition": definition_info, "usages": usages, "fuzzy_matches": fuzzy_matches, "all_defined_symbols": list(all_defined_symbols)}


def get_preceding_comments(source_code, line_number):
    """
    Extracts comments immediately preceding the given line number.
    AST nodes don't directly store all comments, so we read the source.
    """
    lines = source_code.splitlines()
    comments = []
    # line_number is 1-indexed, list is 0-indexed
    current_line_index = line_number - 2
    while current_line_index >= 0:
        line = lines[current_line_index].strip()
        if line.startswith("#"):
            comments.insert(0, line) # Insert at the beginning to maintain order
        elif not line: # Skip empty lines
            pass
        else: # Stop if it's not a comment or an empty line
            break
        current_line_index -= 1
    return "\n".join(comments) if comments else None


def display_results(results):
    """
    Displays the found context in a user-friendly format.
    """
    definition = results.get("definition")
    usages = results.get("usages")
    fuzzy_matches = results.get("fuzzy_matches")

    if definition:
        print("\n--- Definition ---")
        print(f"  Symbol: {definition['name']} ({definition['type']})")
        print(f"  File:   {definition['file_path']}")
        print(f"  Line:   {definition['line_number']}")
        if definition.get("comments"):
            print("  Comments:")
            for comment_line in definition["comments"].splitlines():
                print(f"    {comment_line}")
        if definition.get("docstring"):
            print("  Docstring:")
            for ds_line in definition["docstring"].strip().splitlines():
                print(f"    {ds_line}")
        else:
            print("  Docstring: Not found.")

        if usages:
            print("\n--- Usages ---")
            # Group usages by file for better readability
            usages_by_file = {}
            for usage in usages:
                if usage['file_path'] not in usages_by_file:
                    usages_by_file[usage['file_path']] = []
                usages_by_file[usage['file_path']].append(usage)

            for file_path, file_usages in usages_by_file.items():
                print(f"\n  In File: {file_path}")
                for usage in file_usages:
                    print(f"    L{usage['line_number']}: {usage['code_line']}")
        else:
            print("\n--- Usages ---")
            print("  No usages found (outside of its own definition).")

    elif fuzzy_matches:
        print(f"\nSymbol '{results.get('searched_symbol_name', 'UNKNOWN')}' not found.")
        print("\nDid you mean one of these?")
        for match in fuzzy_matches:
            print(f"  - {match}")
    else:
        print(f"\nSymbol '{results.get('searched_symbol_name', 'UNKNOWN')}' not found and no similar symbols detected.")


if __name__ == "__main__":
    main()
