import argparse
import io
from pathlib import Path
from lexer import Lexer
from text import Writer


def get_expected_file_path(input_path: str) -> str:
    """
    Derive the expected output file path from the input file path.
    Converts test/milestone-X/input/Y.pas to test/milestone-X/expected/Y.txt
    """
    input_file = Path(input_path)
    # Replace 'input' with 'expected' and change extension to .txt
    expected_path = input_file.parent.parent / "expected" / input_file.with_suffix('.txt').name
    return str(expected_path)


def check_output(actual_output: str, expected_file: str) -> None:
    """
    Compare actual output with expected output and display differences.
    """
    try:
        with open(expected_file, "r", encoding="utf-8") as f:
            expected_output = f.read()
    except FileNotFoundError:
        print(f"Error: Expected output file not found at '{expected_file}'")
        return

    # Normalize line endings and strip trailing whitespace
    actual_lines = actual_output.strip().split('\n')
    expected_lines = expected_output.strip().split('\n')

    if actual_lines == expected_lines:
        print("[PASS] Output matches expected!")
        return

    print("[FAIL] Output differs from expected:")
    print("\nExpected:")
    print("-" * 40)
    print(expected_output)
    print("\nActual:")
    print("-" * 40)
    print(actual_output)
    print("\nDifferences:")
    print("-" * 40)

    # Show line-by-line differences
    max_lines = max(len(actual_lines), len(expected_lines))
    for i in range(max_lines):
        expected_line = expected_lines[i] if i < len(expected_lines) else "<missing>"
        actual_line = actual_lines[i] if i < len(actual_lines) else "<missing>"

        if expected_line != actual_line:
            print(f"Line {i+1}:")
            print(f"  Expected: {expected_line}")
            print(f"  Actual:   {actual_line}")


def main():
    """
    Main function to run the lexer.
    Parses command-line arguments for the input file,
    tokenizes the file content, and prints the tokens.
    """
    parser = argparse.ArgumentParser(
        description="Lexer for Pascal-like language.")
    parser.add_argument("file_path", type=str,
                        help="Path to the source code file.")
    parser.add_argument("--check", action="store_true",
                        help="Compare output with expected output file.")
    args = parser.parse_args()

    try:
        with open(args.file_path, "r", encoding="utf-8") as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"Error: File not found at '{args.file_path}'")
        return

    lexer = Lexer()
    tokens = lexer.tokenize(source_code)

    # Filter out WHITESPACE and COMMENT tokens, then create tuples for the writer
    token_tuples = [
        (token.type.name, token.value)
        for token in tokens
        if token.type.name not in ("WHITESPACE", "COMMENT")
    ]

    if args.check:
        # Capture output to string for comparison
        output_stream = io.StringIO()
        writer = Writer(stream=output_stream)
        writer.write_tokens(token_tuples)
        actual_output = output_stream.getvalue()

        # Get expected file path and check
        expected_file = get_expected_file_path(args.file_path)
        check_output(actual_output, expected_file)
    else:
        # Normal output to stdout
        writer = Writer()
        writer.write_tokens(token_tuples)


if __name__ == "__main__":
    main()
