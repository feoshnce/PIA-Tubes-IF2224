import argparse
import io
from itertools import zip_longest
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
    expected_path = input_file.parent.parent / \
        "expected" / input_file.with_suffix('.txt').name
    return str(expected_path)


def get_output_file_path(input_path: str) -> str:
    """
    Derive the output file path from the input file path.
    Converts test/milestone-X/input/Y.pas to test/milestone-X/output/Y.txt
    """
    input_file = Path(input_path)
    # Replace 'input' with 'output' and change extension to .txt
    output_path = input_file.parent.parent / \
        "output" / input_file.with_suffix('.txt').name
    return str(output_path)


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

    differences = [
        (i + 1, exp, act)
        for i, (exp, act) in enumerate(zip_longest(
            expected_lines, actual_lines, fillvalue="<missing>"
        ))
        if exp != act
    ]

    for line_num, expected, actual in differences:
        print(f"Line {line_num}:")
        print(f"  Expected: {expected}")
        print(f"  Actual:   {actual}")


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
    parser.add_argument("--output", nargs="?", const=True, default=None,
                        help="Save output to file. If no path specified, saves to test/milestone-X/output/Y.txt")
    args = parser.parse_args()

    try:
        with open(args.file_path, "r", encoding="utf-8") as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"Error: File not found at '{args.file_path}'")
        return

    lexer = Lexer()
    tokens = lexer.tokenize(source_code)
    token_tuples = list(map(
        lambda token: (token.type.name, token.value),
        filter(lambda token: token.type.name not in ("WHITESPACE", "COMMENT"), tokens)
    ))

    output_stream = io.StringIO()
    writer = Writer(stream=output_stream)
    writer.write_tokens(token_tuples)
    actual_output = output_stream.getvalue()

    if args.check:
        expected_file = get_expected_file_path(args.file_path)
        check_output(actual_output, expected_file)

    if args.output: # Truthy value
        if args.output is True:
            output_file = get_output_file_path(args.file_path)
        else:
            output_file = args.output

        # Create output directory if it doesn't exist
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write output to file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(actual_output)

        print(f"Output saved to: {output_file}")

    if not args.check and not args.output:
        # Normal output to stdout (only if not checking or saving)
        print(actual_output, end="")


if __name__ == "__main__":
    main()
