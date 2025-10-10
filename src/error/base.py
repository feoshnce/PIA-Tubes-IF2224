from __future__ import annotations
from dataclasses import dataclass
from abc import ABC
from typing import Optional
from src.io.position import Position


@dataclass
class ErrorBase(Exception, ABC):
    """Abstract base for all error types in the compiler/lexer pipeline."""
    message: str
    position: Optional[Position] = None

    def __str__(self) -> str:
        pos_str = f" at {self.position}" if self.position else ""
        return f"[{self.__class__.__name__}] {self.message}{pos_str}"
