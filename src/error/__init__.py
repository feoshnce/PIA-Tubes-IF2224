from .base import ErrorBase
from .lexical_error import LexicalError
from .syntax_error import SyntaxError, UnexpectedTokenError, UnexpectedEOFError
from .semantic_error import (
    SemanticError,
    UndeclaredIdentifierError,
    DuplicateDeclarationError,
    TypeMismatchError,
    InvalidOperationError,
    InvalidArrayIndexError,
    InvalidRecordAccessError,
    InvalidFunctionCallError
)

__all__ = [
    "ErrorBase",
    "LexicalError",
    "SyntaxError",
    "UnexpectedTokenError",
    "UnexpectedEOFError",
    "SemanticError",
    "UndeclaredIdentifierError",
    "DuplicateDeclarationError",
    "TypeMismatchError",
    "InvalidOperationError",
    "InvalidArrayIndexError",
    "InvalidRecordAccessError",
    "InvalidFunctionCallError"
]
