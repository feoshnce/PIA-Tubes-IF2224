from __future__ import annotations
from dataclasses import dataclass
from src.text import Position
from .base import ErrorBase


@dataclass
class LexicalError(ErrorBase):
    """Raised during lexical analysis when invalid token or character is found."""
    position: Position

    def __str__(self) -> str:
        return f"[LexicalError] {self.message} at {self.position}"
