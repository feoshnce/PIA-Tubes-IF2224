# Error Module

Error handling for the compiler/lexer pipeline.

## Usage

### ErrorBase

Abstract base class for all error types.

```python
from src.error.base import ErrorBase
from src.text.position import Position

# All errors inherit from ErrorBase
# ErrorBase requires a message and optional position
```

### LexicalError

Raised when invalid tokens or characters are encountered during lexical analysis.

```python
from src.error.lexical_error import LexicalError
from src.text.position import Position

# Create and raise a lexical error
position = Position(line=1, column=5, filename="test.txt")
raise LexicalError(message="Invalid character '#'", position=position)

# Output: [LexicalError] Invalid character '#' at test.txt:1:5
```

## Creating New Error Types

Extend `ErrorBase` to create new error types:

```python
from dataclasses import dataclass
from src.error.base import ErrorBase
from src.text.position import Position

@dataclass
class SyntaxError(ErrorBase):
    """Raised during syntax analysis."""
    position: Position

    def __str__(self) -> str:
        return f"[SyntaxError] {self.message} at {self.position}"
```
