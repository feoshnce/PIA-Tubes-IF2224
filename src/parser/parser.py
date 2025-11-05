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

    def parse_const_declarations(self) -> list[ConstDeclaration]:
        """
        Parse constant declarations.

        Grammar:
            const-declaration -> KEYWORD(konstanta) (IDENTIFIER = constant SEMICOLON)+

        Returns:
            List of ConstDeclaration nodes
        """
        self.expect(TokenType.KEYWORD, "konstanta")
        declarations = []

        while self.match(TokenType.IDENTIFIER):
            name = self.expect(TokenType.IDENTIFIER).value
            self.expect(TokenType.RELATIONAL_OPERATOR, "=")

            # Parse constant value (number, string, char, boolean, or identifier)
            value = self.parse_constant_value()

            self.expect(TokenType.SEMICOLON)

            declarations.append(ConstDeclaration(identifier=name, value=value))

        return declarations

    def parse_constant_value(self):
        """
        Parse a constant value.

        Returns:
            The constant value (number, string, char, or boolean)
        """
        if self.match(TokenType.NUMBER):
            token = self.advance()
            # Try to parse as int, otherwise float
            try:
                return int(token.value)
            except ValueError:
                return float(token.value)
        elif self.match(TokenType.STRING_LITERAL):
            return self.advance().value
        elif self.match(TokenType.CHAR_LITERAL):
            return self.advance().value
        elif self.match(TokenType.IDENTIFIER):
            # Could be a boolean or another constant reference
            token = self.advance()
            if token.value.lower() in ("true", "false"):
                return token.value.lower() == "true"
            return token.value
        elif self.match(TokenType.ARITHMETIC_OPERATOR):
            # Handle negative numbers
            op = self.advance().value
            if op in ("+", "-"):
                num_token = self.expect(TokenType.NUMBER)
                try:
                    num = int(num_token.value)
                except ValueError:
                    num = float(num_token.value)
                return -num if op == "-" else num
        else:
            self.error("Expected constant value")

    def parse_type_declarations(self) -> list[TypeDeclaration]:
        """
        Parse type declarations.

        Grammar:
            type-declaration -> KEYWORD(tipe) (IDENTIFIER = type-definition SEMICOLON)+

        Returns:
            List of TypeDeclaration nodes
        """
        self.expect(TokenType.KEYWORD, "tipe")
        declarations = []

        while self.match(TokenType.IDENTIFIER):
            name = self.expect(TokenType.IDENTIFIER).value
            self.expect(TokenType.RELATIONAL_OPERATOR, "=")

            type_spec = self.parse_type()

            self.expect(TokenType.SEMICOLON)

            declarations.append(TypeDeclaration(
                identifier=name, type_spec=type_spec))

        return declarations

    def parse_var_declarations(self) -> list[VarDeclaration]:
        """
        Parse variable declarations.

        Grammar:
            var-declaration -> KEYWORD(variabel) (identifier-list COLON type SEMICOLON)+

        Returns:
            List of VarDeclaration nodes
        """
        self.expect(TokenType.KEYWORD, "variabel")
        declarations = []

        while self.match(TokenType.IDENTIFIER):
            identifiers = self.parse_identifier_list()
            self.expect(TokenType.COLON)
            type_spec = self.parse_type()
            self.expect(TokenType.SEMICOLON)

            declarations.append(VarDeclaration(
                identifiers=identifiers, type_spec=type_spec))

        return declarations

    def parse_identifier_list(self) -> list[str]:
        """
        Parse a comma-separated list of identifiers.

        Grammar:
            identifier-list -> IDENTIFIER (COMMA IDENTIFIER)*

        Returns:
            List of identifier strings
        """
        identifiers = [self.expect(TokenType.IDENTIFIER).value]

        while self.match(TokenType.COMMA):
            self.advance()  # consume comma
            identifiers.append(self.expect(TokenType.IDENTIFIER).value)

        return identifiers

    def parse_type(self) -> TypeSpec:
        """
        Parse a type specification.

        Grammar:
            type -> simple-type | array-type | record-type

        Returns:
            TypeSpec AST node
        """
        if self.match(TokenType.KEYWORD, "larik"):
            return self.parse_array_type()
        elif self.match(TokenType.KEYWORD, "rekaman"):
            return self.parse_record_type()
        else:
            return self.parse_simple_type()

    def parse_simple_type(self) -> SimpleType:
        """
        Parse a simple type (integer, real, boolean, char, or custom type).

        Grammar:
            simple-type -> IDENTIFIER | KEYWORD (for built-in types)

        Returns:
            SimpleType AST node
        """
        # Accept both IDENTIFIER (custom types) and KEYWORD (built-in types)
        if self.match(TokenType.IDENTIFIER):
            type_name = self.advance().value
        elif self.match(TokenType.KEYWORD):
            # Built-in types (integer, real, boolean, char)
            type_name = self.advance().value
        else:
            self.error("Expected type name")

        return SimpleType(name=type_name)

    def parse_array_type(self) -> ArrayType:
        """
        Parse an array type.

        Grammar:
            array-type -> KEYWORD(larik) LBRACKET range RBRACKET KEYWORD(dari) type

        Returns:
            ArrayType AST node
        """
        self.expect(TokenType.KEYWORD, "larik")
        self.expect(TokenType.LBRACKET)

        # Parse range (e.g., 1..10)
        start_expr = self.parse_simple_expression()
        self.expect(TokenType.RANGE_OPERATOR)
        end_expr = self.parse_simple_expression()

        self.expect(TokenType.RBRACKET)
        self.expect(TokenType.KEYWORD, "dari")

        element_type = self.parse_type()

        return ArrayType(index_type=(start_expr, end_expr), element_type=element_type)

    def parse_record_type(self) -> RecordType:
        """
        Parse a record type.

        Grammar:
            record-type -> KEYWORD(rekaman) field-list KEYWORD(selesai)

        Returns:
            RecordType AST node
        """
        self.expect(TokenType.KEYWORD, "rekaman")

        fields = []
        while not self.match(TokenType.KEYWORD, "selesai"):
            identifiers = self.parse_identifier_list()
            self.expect(TokenType.COLON)
            type_spec = self.parse_type()
            self.expect(TokenType.SEMICOLON)

            fields.append(VarDeclaration(
                identifiers=identifiers, type_spec=type_spec))

        self.expect(TokenType.KEYWORD, "selesai")

        return RecordType(fields=fields)

    def parse_subprogram_declaration(self):
        """
        Parse a procedure or function declaration.

        Returns:
            ProcedureDeclaration or FunctionDeclaration AST node
        """
        if self.match(TokenType.KEYWORD, "prosedur"):
            return self.parse_procedure_declaration()
        elif self.match(TokenType.KEYWORD, "fungsi"):
            return self.parse_function_declaration()
        else:
            self.error("Expected 'prosedur' or 'fungsi'")

    def parse_procedure_declaration(self) -> ProcedureDeclaration:
        """
        Parse a procedure declaration.

        Grammar:
            procedure-declaration -> KEYWORD(prosedur) IDENTIFIER
                                    (LPARENTHESIS formal-parameter-list RPARENTHESIS)?
                                    SEMICOLON block SEMICOLON

        Returns:
            ProcedureDeclaration AST node
        """
        self.expect(TokenType.KEYWORD, "prosedur")
        name = self.expect(TokenType.IDENTIFIER).value

        parameters = []
        if self.match(TokenType.LPARENTHESIS):
            self.advance()
            if not self.match(TokenType.RPARENTHESIS):
                parameters = self.parse_formal_parameter_list()
            self.expect(TokenType.RPARENTHESIS)

        self.expect(TokenType.SEMICOLON)

        block = self.parse_block()

        self.expect(TokenType.SEMICOLON)

        return ProcedureDeclaration(name=name, parameters=parameters, block=block)

    def parse_function_declaration(self) -> FunctionDeclaration:
        """
        Parse a function declaration.

        Grammar:
            function-declaration -> KEYWORD(fungsi) IDENTIFIER
                                   (LPARENTHESIS formal-parameter-list RPARENTHESIS)?
                                   COLON type SEMICOLON block SEMICOLON

        Returns:
            FunctionDeclaration AST node
        """
        self.expect(TokenType.KEYWORD, "fungsi")
        name = self.expect(TokenType.IDENTIFIER).value

        parameters = []
        if self.match(TokenType.LPARENTHESIS):
            self.advance()
            if not self.match(TokenType.RPARENTHESIS):
                parameters = self.parse_formal_parameter_list()
            self.expect(TokenType.RPARENTHESIS)

        self.expect(TokenType.COLON)
        return_type = self.parse_type()

        self.expect(TokenType.SEMICOLON)

        block = self.parse_block()

        self.expect(TokenType.SEMICOLON)

        return FunctionDeclaration(
            name=name,
            parameters=parameters,
            return_type=return_type,
            block=block
        )

    def parse_formal_parameter_list(self) -> list[Parameter]:
        """
        Parse formal parameter list.

        Grammar:
            formal-parameter-list -> parameter-group (SEMICOLON parameter-group)*
            parameter-group -> identifier-list COLON type

        Returns:
            List of Parameter nodes
        """
        parameters = []

        # Parse first parameter group
        identifiers = self.parse_identifier_list()
        self.expect(TokenType.COLON)
        type_spec = self.parse_type()
        parameters.append(
            Parameter(identifiers=identifiers, type_spec=type_spec))

        # Parse remaining parameter groups
        while self.match(TokenType.SEMICOLON):
            self.advance()
            identifiers = self.parse_identifier_list()
            self.expect(TokenType.COLON)
            type_spec = self.parse_type()
            parameters.append(
                Parameter(identifiers=identifiers, type_spec=type_spec))

        return parameters