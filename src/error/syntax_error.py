"""
Syntax error handling for the parser.
"""

from .base import ErrorBase
from syntax import Token


class SyntaxError(ErrorBase):
    """
    Exception raised for syntax errors during parsing.
    """

    def __init__(self, message: str, token: Token = None):
        """
        Initialize a syntax error.

        Args:
            message: The error message
            token: The token where the error occurred (optional)
        """
        self.token = token
        super().__init__(message)

    def __str__(self) -> str:
        if self.token:
            return f"SyntaxError at position {self.token.start}: {self.message}"
        return f"SyntaxError: {self.message}"


class UnexpectedTokenError(SyntaxError):
    """
    Exception raised when an unexpected token is encountered.
    """

    def __init__(self, expected: str, got: Token):
        """
        Initialize an unexpected token error.

        Args:
            expected: Description of what was expected
            got: The token that was received instead
        """
        message = f"Expected {expected}, got {got.type.name} '{got.value}'"
        super().__init__(message, got)


class UnexpectedEOFError(SyntaxError):
    """
    Exception raised when end of file is reached unexpectedly.
    """

    def __init__(self, expected: str):
        """
        Initialize an unexpected EOF error.

        Args:
            expected: Description of what was expected
        """
        message = f"Unexpected end of file. Expected {expected}"
        super().__init__(message)
