from syntax import Token, TokenType


HYPHENATED_KEYWORDS = {
    "turun-ke",
    "selain-itu",
}


def merge_hyphenated_keywords(tokens: list[Token]) -> list[Token]:
    """
    Merge tokens to form hyphenated keywords.

    This function looks for patterns like:
        IDENTIFIER('turun') + ARITHMETIC_OPERATOR('-') + KEYWORD('ke')
        or
        IDENTIFIER('selain') + ARITHMETIC_OPERATOR('-') + IDENTIFIER('itu')
    and merges them into a single KEYWORD token.
    """
    result = []
    i = 0

    while i < len(tokens):
        # Check if we can form a hyphenated keyword
        if i + 2 < len(tokens):
            token1 = tokens[i]
            token2 = tokens[i + 1]
            token3 = tokens[i + 2]

            # Check pattern: IDENTIFIER/KEYWORD + '-' + IDENTIFIER/KEYWORD
            if ((token1.type == TokenType.IDENTIFIER or token1.type == TokenType.KEYWORD) and
                token2.type == TokenType.ARITHMETIC_OPERATOR and
                token2.value == "-" and
                    (token3.type == TokenType.IDENTIFIER or token3.type == TokenType.KEYWORD)):

                # Construct potential keyword
                potential_keyword = f"{token1.value}-{token3.value}"

                # Check if it's a valid hyphenated keyword
                if potential_keyword.lower() in HYPHENATED_KEYWORDS:
                    merged_token = Token(
                        type=TokenType.KEYWORD,
                        value=potential_keyword,
                        start=token1.start,
                        end=token3.end
                    )
                    result.append(merged_token)
                    i += 3  # Skip all three tokens
                    continue

        # No merge, just add the current token
        result.append(tokens[i])
        i += 1

    return result
