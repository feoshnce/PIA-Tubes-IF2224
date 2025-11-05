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

    def error(self, message: str) -> None:
        """
        Raise a syntax error with the given message.

        Args:
            message: The error message

        Raises:
            SyntaxError: Always raises a syntax error
        """
        raise SyntaxError(message, self.current_token)

    def peek(self, offset: int = 0) -> Optional[Token]:
        """
        Look ahead at a token without consuming it.

        Args:
            offset: Number of tokens to look ahead (0 = current token)

        Returns:
            The token at the given offset, or None if out of bounds
        """
        index = self.current_index + offset
        if 0 <= index < len(self.tokens):
            return self.tokens[index]
        return None

    def advance(self) -> Token:
        """
        Move to the next token.

        Returns:
            The token that was current before advancing

        Raises:
            UnexpectedEOFError: If already at end of tokens
        """
        if self.current_token is None:
            raise UnexpectedEOFError("more tokens")

        old_token = self.current_token
        self.current_index += 1
        if self.current_index < len(self.tokens):
            self.current_token = self.tokens[self.current_index]
        else:
            self.current_token = None
        return old_token

    def expect(self, token_type: TokenType, value: str = None) -> Token:
        """
        Expect a specific token type and optionally a specific value.

        Args:
            token_type: The expected token type
            value: The expected token value (optional, case-insensitive for keywords)

        Returns:
            The consumed token

        Raises:
            UnexpectedTokenError: If the current token doesn't match
            UnexpectedEOFError: If at end of tokens
        """
        if self.current_token is None:
            expected_desc = f"{token_type.name}"
            if value:
                expected_desc += f" '{value}'"
            raise UnexpectedEOFError(expected_desc)

        if self.current_token.type != token_type:
            expected_desc = f"{token_type.name}"
            if value:
                expected_desc += f" '{value}'"
            raise UnexpectedTokenError(expected_desc, self.current_token)

        if value is not None and self.current_token.value.lower() != value.lower():
            raise UnexpectedTokenError(
                f"{token_type.name} '{value}'", self.current_token)

        return self.advance()

    def match(self, token_type: TokenType, value: str = None) -> bool:
        """
        Check if the current token matches the given type and value.

        Args:
            token_type: The token type to match
            value: The token value to match (optional, case-insensitive for keywords)

        Returns:
            True if the current token matches, False otherwise
        """
        if self.current_token is None:
            return False

        if self.current_token.type != token_type:
            return False

        if value is not None and self.current_token.value.lower() != value.lower():
            return False

        return True

    # =========================================================================
    # Grammar Rules Implementation
    # =========================================================================

    def parse(self) -> Program:
        """
        Parse the entire program.

        Grammar:
            program -> program-header declaration-part compound-statement DOT

        Returns:
            Program AST node
        """
        program_node = self.parse_program()
        if self.current_token is not None:
            self.error("Expected end of file")
        return program_node

    def parse_program(self) -> Program:
        """
        Parse program structure.

        Grammar:
            program -> KEYWORD(program) IDENTIFIER SEMICOLON block DOT

        Returns:
            Program AST node
        """
        self.expect(TokenType.KEYWORD, "program")
        name_token = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.SEMICOLON)

        block = self.parse_block()

        self.expect(TokenType.DOT)

        return Program(name=name_token.value, block=block)

    def parse_block(self) -> Block:
        """
        Parse a block (declarations + compound statement).

        Grammar:
            block -> declaration-part compound-statement

        Returns:
            Block AST node
        """
        declarations = self.parse_declaration_part()
        compound_stmt = self.parse_compound_statement()

        return Block(declarations=declarations, compound_statement=compound_stmt)

    def parse_declaration_part(self) -> list:
        """
        Parse declaration part (const, type, var, procedure, function).

        Grammar:
            declaration-part -> (const-declaration)* (type-declaration)*
                               (var-declaration)* (subprogram-declaration)*

        Returns:
            List of declaration AST nodes
        """
        declarations = []

        # Parse constant declarations
        while self.match(TokenType.KEYWORD, "konstanta"):
            declarations.extend(self.parse_const_declarations())

        # Parse type declarations
        while self.match(TokenType.KEYWORD, "tipe"):
            declarations.extend(self.parse_type_declarations())

        # Parse variable declarations
        while self.match(TokenType.KEYWORD, "variabel"):
            declarations.extend(self.parse_var_declarations())

        # Parse subprogram declarations (procedures and functions)
        while self.match(TokenType.KEYWORD, "prosedur") or self.match(TokenType.KEYWORD, "fungsi"):
            declarations.append(self.parse_subprogram_declaration())

        return declarations