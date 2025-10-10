# Text Module

Text processing utilities for the compiler/lexer pipeline.

## Usage

### Position

Represents a position in source text.

```python
from src.text import Position

position = Position(index=0, line=1, column=1)
new_pos = position.advance('\n')  # Moves to next line
```

### Reader

Reads and processes character streams.

```python
from src.text import Reader

reader = Reader.from_file("program.pas")

while not reader.eof():
    print(reader.current_char)
    reader.advance()

# Peek ahead without consuming
next_char = reader.peek(1)

# Expect specific character
reader.expect('=')  # Raises LexicalError if not '='
```

### Writer

Outputs tokens and errors.

```python
from src.text import Writer

# Write to console
writer = Writer()
writer.write_tokens([("IDENTIFIER", "x"), ("NUMBER", "10")])

# Write to file
with open("output.txt", "w", encoding="utf-8") as f:
    writer = Writer(stream=f)
    writer.write_tokens([("IDENTIFIER", "x"), ("NUMBER", "10")])
```
