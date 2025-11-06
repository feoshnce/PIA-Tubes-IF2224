"""
AST nodes for expressions.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from .base import ASTNode


@dataclass
class Expression(ASTNode):
    """Base class for all expression nodes."""
    pass


@dataclass
class BinaryOp(Expression):
    """
    Represents a binary operation.

    Grammar:
        binary_op -> expression operator expression
    """

    left: Expression
    operator: str
    right: Expression

    def accept(self, visitor: Any) -> Any:
        return visitor.visit_binary_op(self)

    def to_dict(self) -> dict:
        return {
            'type': 'BinaryOp',
            'operator': self.operator,
            'left': self.left.to_dict(),
            'right': self.right.to_dict()
        }


@dataclass
class UnaryOp(Expression):
    """
    Represents a unary operation.

    Grammar:
        unary_op -> operator expression
    """

    operator: str
    operand: Expression

    def accept(self, visitor: Any) -> Any:
        return visitor.visit_unary_op(self)

    def to_dict(self) -> dict:
        return {
            'type': 'UnaryOp',
            'operator': self.operator,
            'operand': self.operand.to_dict()
        }


@dataclass
class Variable(Expression):
    """
    Represents a variable reference.

    Grammar:
        variable -> IDENTIFIER
                  | IDENTIFIER '[' expression ']'
                  | IDENTIFIER '.' IDENTIFIER
    """

    name: str
    index: Expression = None  # For array indexing
    field: str = None  # For record field access

    def accept(self, visitor: Any) -> Any:
        return visitor.visit_variable(self)

    def to_dict(self) -> dict:
        result = {
            'type': 'Variable',
            'name': self.name
        }
        if self.index:
            result['index'] = self.index.to_dict()
        if self.field:
            result['field'] = self.field
        return result


@dataclass
class Number(Expression):
    """
    Represents a numeric literal.

    Grammar:
        number -> INTEGER | REAL
    """

    value: Any  # int or float

    def accept(self, visitor: Any) -> Any:
        return visitor.visit_number(self)

    def to_dict(self) -> dict:
        return {
            'type': 'Number',
            'value': self.value
        }


@dataclass
class String(Expression):
    """
    Represents a string literal.

    Grammar:
        string -> STRING_LITERAL
    """

    value: str

    def accept(self, visitor: Any) -> Any:
        return visitor.visit_string(self)

    def to_dict(self) -> dict:
        return {
            'type': 'String',
            'value': self.value
        }


@dataclass
class Char(Expression):
    """
    Represents a character literal.

    Grammar:
        char -> CHAR_LITERAL
    """

    value: str

    def accept(self, visitor: Any) -> Any:
        return visitor.visit_char(self)

    def to_dict(self) -> dict:
        return {
            'type': 'Char',
            'value': self.value
        }


@dataclass
class Boolean(Expression):
    """
    Represents a boolean literal.

    Grammar:
        boolean -> 'true' | 'false'
    """

    value: bool

    def accept(self, visitor: Any) -> Any:
        return visitor.visit_boolean(self)

    def to_dict(self) -> dict:
        return {
            'type': 'Boolean',
            'value': self.value
        }


@dataclass
class ParenthesizedExpression(Expression):
    """
    Represents a parenthesized expression.

    Grammar:
        parenthesized_expression -> '(' expression ')'
    """

    expression: Expression

    def accept(self, visitor: Any) -> Any:
        return visitor.visit_parenthesized_expression(self)

    def to_dict(self) -> dict:
        return {
            'type': 'ParenthesizedExpression',
            'expression': self.expression.to_dict()
        }


@dataclass
class FunctionCall(Expression):
    """
    Represents a function call.

    Grammar:
        function_call -> IDENTIFIER '(' argument_list? ')'
    """

    name: str
    arguments: list[Expression]

    def accept(self, visitor: Any) -> Any:
        return visitor.visit_function_call(self)

    def to_dict(self) -> dict:
        return {
            'type': 'FunctionCall',
            'name': self.name,
            'arguments': [arg.to_dict() for arg in self.arguments]
        }
