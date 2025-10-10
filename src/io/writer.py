from __future__ import annotations
from typing import Iterable, TextIO
from src.error.base import ErrorBase


class Writer:
    """Handles token and error output for the lexer."""

    def __init__(self, stream: TextIO | None = None):
        import sys
        self.stream = stream or sys.stdout

    def write_tokens(self, tokens: Iterable[tuple[str, str]]) -> None:
        """Print a list of (token_type, lexeme) pairs."""
        for tok_type, lexeme in tokens:
            print(f"{tok_type:<20} {lexeme}", file=self.stream)

    def write_error(self, err: ErrorBase) -> None:
        """Print a formatted error message."""
        print(str(err), file=self.stream)
