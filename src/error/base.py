from __future__ import annotations
from abc import ABC
from typing import Optional
from text import Position


class ErrorBase(Exception, ABC):
    """Abstract base for all error types in the compiler/lexer pipeline."""

    def __init__(self, message: str, position: Optional[Position] = None):
        super().__init__(message)
        self.message = message
        self.position = position

    def __str__(self) -> str:
        pos_str = f" at {self.position}" if self.position else ""
        return f"[{self.__class__.__name__}] {self.message}{pos_str}"
