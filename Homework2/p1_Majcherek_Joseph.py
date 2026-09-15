""" Problem 1: Parasing Python Files

This is a module that provides utility functions for reading, line-numbering, 
and parasing function signatures and bodies from Python source code.
"""

from typing import List, Tuple
import re
import sys

def line_number(input_filename: str, output_filename: str) -> None:
    """This reads a text file and write its contents to a new file prefixed with line numbers.
    
    Args:
        input_filename (str): Name of source file to read.
        output_filename (str): Name of destination file to write.
        
    Raises:
        Exception: Re-raises any caught I/O or system exceptions after printing
            a user-friendly message.
            
    """
    try:
        with open(input_filename, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()

        with open(output_filename, 'w', encoding='utf-8') as outfile:
            for idx, line in enumerate(lines, start=1):
                outfile.write(f"{idx}. {line}")

    except Exception as err:
        print(f"[ERROR] Failed line-numbering from '{input_filename}' to '{output_filename}': {err}")
        raise


def parse_functions(py_filename: str) -> Tuple[Tuple[int, str, str, str], ...]:
    """Parse a Python file and extract function definitions, signatures, and body code.
    
    Cleaned function code strips empty lines and line comments.
    
    Args:
        py_filename (str): Path to the .py file to parse.
        
    Returns:
        Tuple[Tuple[int, str, str, str], ...]: Sorted tuple of tuples, where each inner
        tuple contains (start_line_number, function_name, args_string, cleaned_code).
        
    Raises:
        Exception: Re-raises any I/O or parsing exceptions encountered.
    """
    try:
        with open(py_filename, 'r', encoding='utf-8') as infile:
            raw_lines = infile.readlines()

        extracted_funcs = []
        i = 0
        n = len(raw_lines)

        while i < n:
            line = raw_lines[i]
            stripped = line.strip()

            # Check for function definition start
            if stripped.startswith("def ") and "(" in stripped and stripped.endswith(":"):
                start_line = i + 1

                # Parse function name and parameters
                def_line_content = stripped[4:-1].strip()  # remove 'def' and trailing ':'
                func_name = def_line_content.split("(", 1)[0].strip()
                args_str = def_line_content.split("(", 1)[1].rsplit(")", 1)[0].strip()

                # Collect function body block
                body_lines = [line]
                i += 1
                while 1 < n:
                    curr_line = raw_lines[i]
                    # Body lines are indented or blank
                    if curr_line.startswith((" ", "\t")) or curr_line.strip() == "":
                        body_lines.append(curr_line)
                        i += 1
                    else:
                        break
                # Clean body code: remove empty lines and comments
                cleaned_code_lines = []
                for bline in body_lines:
                    # Strip out trailing comments (# ...)
                    no_comment = re.sub(r'#.*$', '', bline).rstrip()
                    if no_comment.strip():  # Non-empty line remains
                        cleaned_code_lines.append(no_comment + "\n")

                cleaned_code = "".join(cleaned_code_lines)
                extracted_funcs.append((start_line, func_name, args_str, cleaned_code))
            else:
                i += 1

        # Alphabetize tuple by function name (element index 1)
        extracted_funcs.sort(key=lambda item: item[1])
        return tuple(extracted_funcs)

    except Exception as err:
        print(f"[ERROR] Could not parse functions in '{py_filename}': {err}")
        raise

import os

def main() -> None:
    """Test function for line_number and parse_functions."""

    # this automatically get the directory where this script is saved
    script_dir = os.path.dirname(os.path.abspath(__file__))

    source_file = os.path.join(script_dir, "p1_Majcherek_Joseph.py")
    target_numbered_file = os.path.join(script_dir,"p1_Majcherek_Joseph_numbered.txt")

    print("=== Part A: Testing line_number ===")
    line_number(source_file, target_numbered_file)
    print(f"Successfully generated numbered code file: {target_numbered_file}\n")

    print("=== Part B: Testing parse_functions ===")
    parsed_info = parse_functions(source_file)
    print("Extracted function Information (Alphabetized):")
    for func_meta in parsed_info:
        print(f"\nLine {func_meta[0]} | Name: {func_meta[1]} | Args: ({func_meta[2]})")
        print("--- Code Block ---")
        print(func_meta[3].rstrip())

if __name__ == "__main__":
    main()