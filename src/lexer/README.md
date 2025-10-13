# Lexer Module

Lexical analysis for the Pascal-like language compiler.

## Usage

### Lexer

Tokenizes source code using DFA-based pattern matching.

```python
from lexer import Lexer

# Create lexer with default config
lexer = Lexer()

# Tokenize source code
tokens = lexer.tokenize("program Hello; begin end.")

# Process tokens
for token in tokens:
    print(f"{token.type.name}: {token.value}")
```

**Output:**
```
KEYWORD: program
WHITESPACE:
IDENTIFIER: Hello
SEMICOLON: ;
WHITESPACE:
KEYWORD: begin
WHITESPACE:
KEYWORD: end
DOT: .
```

## Configuration

The lexer uses a DFA configuration file at `config/dfa_rules.json` that defines:
- State transitions
- Token types
- Keywords and reserved words
- Character classes
