from dataclasses import dataclass

@dataclass
class Position:
    """Represents a position in source text (line, column, and index)."""
    index: int
    line: int
    column: int

    def advance(self, current_char: str | None) -> "Position":
        if current_char == "\n":
            return Position(self.index + 1, self.line + 1, 1)
        return Position(self.index + 1, self.line, self.column + 1)

    def copy(self) -> "Position":
        return Position(self.index, self.line, self.column)

    def __str__(self) -> str:
        return f"(line {self.line}, col {self.column})"
