import argparse
import json
import sys
import io
from pathlib import Path
from lexer import Lexer
from parser import Parser, format_parse_tree
from error import SyntaxError

# Ensure UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def main():
    """
    Main function to run the parser.

    Parses command-line arguments, tokenizes the input file,
    parses the tokens, and outputs the parse tree.
    """
    parser_cli = argparse.ArgumentParser(
        description="Parser for Pascal-S language."
    )
    parser_cli.add_argument(
        "file_path",
        type=str,
        help="Path to the Pascal-S source code file."
    )
    parser_cli.add_argument(
        "--output",
        nargs="?",
        const=True,
        default=None,
        help="Save parse tree to file. If no path specified, saves to output directory."
    )
    parser_cli.add_argument(
        "--format",
        choices=["json", "tree"],
        default="tree",
        help="Output format: 'json' for JSON representation, 'tree' for tree visualization (default: tree)"
    )
    parser_cli.add_argument(
        "--check",
        action="store_true",
        help="Compare output with expected output file."
    )

    args = parser_cli.parse_args()

    # Read source file
    try:
        with open(args.file_path, "r", encoding="utf-8") as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"Error: File not found at '{args.file_path}'", file=sys.stderr)
        sys.exit(1)

    # Tokenize
    try:
        lexer = Lexer()
        tokens = lexer.tokenize(source_code)

        # Filter out whitespace and comments
        tokens = [
            token for token in tokens
            if token.type.name not in ("WHITESPACE", "COMMENT")
        ]
    except Exception as e:
        print(f"Lexical error: {e}", file=sys.stderr)
        sys.exit(1)

    # Parse
    try:
        parser = Parser(tokens)
        parse_tree = parser.parse()
    except SyntaxError as e:
        print(f"Syntax error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error during parsing: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # Generate output
    if args.format == "json":
        output = json.dumps(parse_tree.to_dict(), indent=2, ensure_ascii=False)
    else:  # tree format
        output = format_parse_tree(parse_tree, tokens)

    # Handle output
    if args.output:
        if args.output is True:
            # Derive output path from input path
            input_file = Path(args.file_path)
            output_dir = input_file.parent.parent / "output"
            output_dir.mkdir(parents=True, exist_ok=True)
            output_file = output_dir / input_file.with_suffix('.json' if args.format == 'json' else '.txt').name
        else:
            output_file = Path(args.output)
            output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Parse tree saved to: {output_file}")
    else:
        print(output)

    if args.check:
        # Compare with expected output
        input_file = Path(args.file_path)
        expected_file = input_file.parent.parent / "expected" / input_file.with_suffix('.json' if args.format == 'json' else '.txt').name

        try:
            with open(expected_file, "r", encoding="utf-8") as f:
                expected_output = f.read()

            if output.strip() == expected_output.strip():
                print("[PASS] Parse tree matches expected!")
            else:
                print("[FAIL] Parse tree differs from expected")
                print(f"\nExpected file: {expected_file}")
        except FileNotFoundError:
            print(f"Warning: Expected output file not found at '{expected_file}'")


if __name__ == "__main__":
    main()
