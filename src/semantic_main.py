import argparse
import json
import sys
import io
from pathlib import Path
from lexer import Lexer
from parser import Parser
from semantic import SemanticVisitor
from semantic.printer import DecoratedASTPrinter
from error import SemanticError
from parse_tree.contract import validate_ast_contract
from semantic.decorated_contract import validate_decorated_ast
import os

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def main():
    parser_cli = argparse.ArgumentParser(
        description="Semantic analyzer for Pascal-S language."
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
        help="Save symbol table to file."
    )
    parser_cli.add_argument(
        "--format",
        choices=["json", "text"],
        default="text",
        help="Output format (default: text)"
    )
    parser_cli.add_argument(
        "--decorated",
        action="store_true",
        help="Print decorated AST with semantic annotations."
    )

    args = parser_cli.parse_args()

    try:
        with open(args.file_path, "r", encoding="utf-8") as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"Error: File not found at '{args.file_path}'", file=sys.stderr)
        sys.exit(1)

    try:
        lexer = Lexer()
        parser = Parser()
        semantic_visitor = SemanticVisitor()

        parse_tree = source_code | lexer | parser
        validate_ast_contract(parse_tree)
        semantic_visitor.visit(parse_tree)
        
        if os.getenv("DEBUG_DECORATED_AST") == "1":
            validate_decorated_ast(parse_tree, strict=False)

        if args.decorated:
            printer = DecoratedASTPrinter()
            print("\nDecorated AST:")
            print("=" * 40)
            print(printer.print(parse_tree))
            print("=" * 40 + "\n")

        output = format_symbol_table(semantic_visitor.symbol_table, args.format)

        if args.output:
            if args.output is True:
                input_file = Path(args.file_path)
                output_dir = input_file.parent.parent / "output"
                output_dir.mkdir(parents=True, exist_ok=True)
                output_file = output_dir / input_file.with_suffix('.symtab' if args.format == 'text' else '.json').name
            else:
                output_file = Path(args.output)
                output_file.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"Symbol table saved to: {output_file}")
        else:
            print(output)

        print("\n[SUCCESS] Semantic analysis completed without errors.")

    except SemanticError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


def format_symbol_table(symtab, format_type):
    if format_type == "json":
        return json.dumps({
            'tab': [
                {
                    'name': entry.name,
                    'kind': entry.obj_kind.name,
                    'type': str(entry.type),
                    'level': entry.level,
                    'address': entry.address,
                    'ref': entry.ref
                }
                for entry in symtab.tab
            ],
            'atab': [
                {
                    'index_type': str(entry.index_type),
                    'element_type': str(entry.element_type),
                    'low': entry.low,
                    'high': entry.high,
                    'element_size': entry.element_size,
                    'size': entry.size
                }
                for entry in symtab.atab
            ],
            'btab': [
                {
                    'last': entry.last,
                    'lpar': entry.lpar,
                    'psze': entry.psze,
                    'vsze': entry.vsze
                }
                for entry in symtab.btab
            ]
        }, indent=2, ensure_ascii=False)
    else:
        lines = []
        lines.append("=" * 80)
        lines.append("SYMBOL TABLE (tab)")
        lines.append("=" * 80)
        lines.append(f"{'Index':<6} {'Name':<20} {'Kind':<12} {'Type':<15} {'Level':<6} {'Addr':<6} {'Ref':<6} {'Link':<6}")
        lines.append("-" * 80)
        for i, entry in enumerate(symtab.tab):
            lines.append(
                f"{i:<6} {entry.name:<20} {entry.obj_kind.name:<12} "
                f"{str(entry.type):<15} {entry.level:<6} {entry.address:<6} "
                f"{entry.ref:<6} {entry.link:<6}"
            )

        if symtab.atab:
            lines.append("\n" + "=" * 88)
            lines.append("ARRAY TABLE (atab)")
            lines.append("=" * 88)
            lines.append(f"{'Index':<6} {'IdxType':<12} {'ElemType':<20} {'Low':<8} {'High':<8} {'ElemSz':<8} {'Size':<8}")
            lines.append("-" * 88)
            for i, entry in enumerate(symtab.atab):
                lines.append(
                    f"{i:<6} {str(entry.index_type):<12} {str(entry.element_type):<20} "
                    f"{entry.low:<8} {entry.high:<8} {entry.element_size:<8} {entry.size:<8}"
                )

        if symtab.btab:
            lines.append("\n" + "=" * 80)
            lines.append("BLOCK TABLE (btab)")
            lines.append("=" * 80)
            lines.append(f"{'Index':<6} {'Last':<8} {'LPar':<8} {'PSize':<8} {'VSize':<8}")
            lines.append("-" * 80)
            for i, entry in enumerate(symtab.btab):
                lines.append(
                    f"{i:<6} {entry.last:<8} {entry.lpar:<8} "
                    f"{entry.psze:<8} {entry.vsze:<8}"
                )

        return "\n".join(lines)


if __name__ == "__main__":
    main()
