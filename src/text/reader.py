from __future__ import annotations
from typing import Optional
from text import Position
from error import LexicalError


class Reader:
    """Character stream reader with position tracking."""

    def __init__(self, text: str) -> None:
        self.text = text
        self.pos = Position(0, 1, 1)
        self.current_char: Optional[str] = self.text[self.pos.index] if self.text else None

    @classmethod
    def from_file(cls, path: str) -> "Reader":
        with open(path, "r", encoding="utf-8") as f:
            return cls(f.read())

    def advance(self) -> None:
        """Move to the next character."""
        if self.current_char is None:
            return
        self.pos = self.pos.advance(self.current_char)
        if self.pos.index >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos.index]

    def peek(self, k: int = 1) -> Optional[str]:
        """Look ahead `k` characters without consuming them."""
        idx = self.pos.index + k
        if 0 <= idx < len(self.text):
            return self.text[idx]
        return None

    def expect(self, expected: str) -> None:
        """Ensure current character equals expected; raise LexicalError otherwise."""
        if self.current_char != expected:
            raise LexicalError(
                f"Expected '{expected}', got '{self.current_char}'", self.pos)

    def eof(self) -> bool:
        return self.current_char is None
