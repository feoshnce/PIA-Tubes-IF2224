from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    KEYWORD = auto()
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING_LITERAL = auto()
    CHAR_LITERAL = auto()
    ARITHMETIC_OPERATOR = auto()
    RELATIONAL_OPERATOR = auto()
    LOGICAL_OPERATOR = auto()
    ASSIGN_OPERATOR = auto()
    SEMICOLON = auto()
    COMMA = auto()
    COLON = auto()
    DOT = auto()
    LPARENTHESIS = auto()
    RPARENTHESIS = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    RANGE_OPERATOR = auto()
    COMMENT = auto()
    WHITESPACE = auto()
    UNKNOWN = auto()


@dataclass(frozen=True)
class Token:
    type: TokenType
    value: str
    start: int
    end: int
