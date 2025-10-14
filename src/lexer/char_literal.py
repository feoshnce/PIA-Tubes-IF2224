from __future__ import annotations
from syntax import Token, TokenType


def fix_char_literals(tokens: list[Token]) -> list[Token]:
    """Convert single-character STRING_LITERAL tokens to CHAR_LITERAL."""
    result = []

    for token in tokens:
        if token.type == TokenType.STRING_LITERAL:
            # Check if the string content (excluding quotes) is exactly 1 character
            # The token value includes the quotes, e.g., "'A'"
            if len(token.value) == 3:  # 'X' = 3 characters (quote, char, quote)
                # Convert to CHAR_LITERAL
                result.append(Token(
                    type=TokenType.CHAR_LITERAL,
                    value=token.value,
                    start=token.start,
                    end=token.end,
                ))
            else:
                result.append(token)
        else:
            result.append(token)

    return result
