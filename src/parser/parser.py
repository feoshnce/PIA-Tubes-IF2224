"""
Recursive Descent Parser for Pascal-S.
"""

from typing import Optional
from syntax import Token, TokenType
from error import SyntaxError, UnexpectedTokenError, UnexpectedEOFError
from parse_tree import (
    Program, Block,
    VarDeclaration, ConstDeclaration, TypeDeclaration,
    ProcedureDeclaration, FunctionDeclaration, Parameter,
    SimpleType, ArrayType, RecordType, TypeSpec,
    CompoundStatement, AssignmentStatement, IfStatement,
    WhileStatement, ForStatement, RepeatStatement, CaseStatement,
    ProcedureCall, Statement,
    Expression, BinaryOp, UnaryOp, Variable, Number,
    String, Char, Boolean, FunctionCall
)


class Parser:
    """
    Recursive Descent Parser for Pascal-S.

    Implements syntax analysis using recursive descent parsing algorithm
    to build a parse tree from a list of tokens.
    """

    def __init__(self, tokens: list[Token]):
        """
        Initialize the parser with a list of tokens.

        Args:
            tokens: List of tokens from the lexer (excluding WHITESPACE and COMMENT)
        """
        self.tokens = tokens
        self.current_index = 0
        self.current_token = tokens[0] if tokens else None