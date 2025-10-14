from __future__ import annotations
from syntax import Token, TokenType


def merge_negative_numbers(tokens: list[Token]) -> list[Token]:
    """Merge unary minus operators with following numbers to create negative number literals."""
    result = []
    i = 0

    while i < len(tokens):
        # Skip whitespace and comments when checking patterns
        if tokens[i].type in (TokenType.WHITESPACE, TokenType.COMMENT):
            result.append(tokens[i])
            i += 1
            continue

        # Check if current token is a minus operator
        if (tokens[i].type == TokenType.ARITHMETIC_OPERATOR and
            tokens[i].value == "-"):

            # Look ahead to find the next non-whitespace/comment token
            j = i + 1
            while j < len(tokens) and tokens[j].type in (TokenType.WHITESPACE, TokenType.COMMENT):
                j += 1

            # Check if next meaningful token is a number
            if j < len(tokens) and tokens[j].type == TokenType.NUMBER:
                # Check if minus should be treated as unary (negative number)
                # by examining the previous non-whitespace/comment token
                prev_idx = len(result) - 1
                while prev_idx >= 0 and result[prev_idx].type in (TokenType.WHITESPACE, TokenType.COMMENT):
                    prev_idx -= 1

                is_unary = False
                if prev_idx < 0:
                    # Minus at the beginning
                    is_unary = True
                else:
                    prev_token = result[prev_idx]
                    # Contexts where minus is unary
                    unary_contexts = {
                        TokenType.ASSIGN_OPERATOR,
                        TokenType.RELATIONAL_OPERATOR,
                        TokenType.ARITHMETIC_OPERATOR,
                        TokenType.LOGICAL_OPERATOR,
                        TokenType.LPARENTHESIS,
                        TokenType.LBRACKET,
                        TokenType.COMMA,
                        TokenType.COLON,
                        TokenType.RANGE_OPERATOR,
                    }

                    if prev_token.type in unary_contexts:
                        is_unary = True
                    elif prev_token.type == TokenType.KEYWORD:
                        # After keywords like 'then', 'else', 'do', 'of', etc.
                        if prev_token.value.lower() in {'then', 'else', 'do', 'of', 'to', 'downto'}:
                            is_unary = True

                if is_unary:
                    # Merge minus with number, including any whitespace between them
                    merged_token = Token(
                        type=TokenType.NUMBER,
                        value="-" + tokens[j].value,
                        start=tokens[i].start,
                        end=tokens[j].end,
                    )
                    result.append(merged_token)
                    # Skip past the number and any whitespace between
                    i = j + 1
                    continue

        # No merge needed, add token as-is
        result.append(tokens[i])
        i += 1

    return result
