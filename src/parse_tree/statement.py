"""
AST nodes for statements.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional
from .base import ASTNode
from .expression import Expression, Variable


@dataclass
class Statement(ASTNode):
    """Base class for all statement nodes."""
    pass


@dataclass
class CompoundStatement(Statement):
    """
    Represents a compound statement (begin...end block).

    Grammar:
        compound_statement -> 'begin' statement_list 'end'
        statement_list -> statement (';' statement)*
    """

    statements: list[Statement]

    def accept(self, visitor: Any) -> Any:
        return visitor.visit_compound_statement(self)

    def to_dict(self) -> dict:
        return {
            'type': 'CompoundStatement',
            'statements': [stmt.to_dict() for stmt in self.statements]
        }


@dataclass
class AssignmentStatement(Statement):
    """
    Represents an assignment statement.

    Grammar:
        assignment_statement -> variable ':=' expression
    """

    variable: Variable
    expression: Expression

    def accept(self, visitor: Any) -> Any:
        return visitor.visit_assignment_statement(self)

    def to_dict(self) -> dict:
        return {
            'type': 'AssignmentStatement',
            'variable': self.variable.to_dict(),
            'expression': self.expression.to_dict()
        }


@dataclass
class IfStatement(Statement):
    """
    Represents an if statement.

    Grammar:
        if_statement -> 'if' expression 'then' statement ('else' statement)?
    """

    condition: Expression
    then_statement: Statement
    else_statement: Optional[Statement] = None

    def accept(self, visitor: Any) -> Any:
        return visitor.visit_if_statement(self)

    def to_dict(self) -> dict:
        result = {
            'type': 'IfStatement',
            'condition': self.condition.to_dict(),
            'then_statement': self.then_statement.to_dict()
        }
        if self.else_statement:
            result['else_statement'] = self.else_statement.to_dict()
        return result


@dataclass
class WhileStatement(Statement):
    """
    Represents a while statement.

    Grammar:
        while_statement -> 'while' expression 'do' statement
    """

    condition: Expression
    body: Statement

    def accept(self, visitor: Any) -> Any:
        return visitor.visit_while_statement(self)

    def to_dict(self) -> dict:
        return {
            'type': 'WhileStatement',
            'condition': self.condition.to_dict(),
            'body': self.body.to_dict()
        }


@dataclass
class ForStatement(Statement):
    """
    Represents a for statement.

    Grammar:
        for_statement -> 'for' IDENTIFIER ':=' expression ('to'|'downto') expression 'do' statement
    """

    variable: str
    start_expr: Expression
    end_expr: Expression
    direction: str  # 'to' or 'downto'
    body: Statement

    def accept(self, visitor: Any) -> Any:
        return visitor.visit_for_statement(self)

    def to_dict(self) -> dict:
        return {
            'type': 'ForStatement',
            'variable': self.variable,
            'start_expr': self.start_expr.to_dict(),
            'end_expr': self.end_expr.to_dict(),
            'direction': self.direction,
            'body': self.body.to_dict()
        }


@dataclass
class RepeatStatement(Statement):
    """
    Represents a repeat-until statement.

    Grammar:
        repeat_statement -> 'repeat' statement_list 'until' expression
    """

    statements: list[Statement]
    condition: Expression

    def accept(self, visitor: Any) -> Any:
        return visitor.visit_repeat_statement(self)

    def to_dict(self) -> dict:
        return {
            'type': 'RepeatStatement',
            'statements': [stmt.to_dict() for stmt in self.statements],
            'condition': self.condition.to_dict()
        }


@dataclass
class CaseStatement(Statement):
    """
    Represents a case statement.

    Grammar:
        case_statement -> 'case' expression 'of' case_list 'end'
        case_list -> case_item (';' case_item)*
        case_item -> constant (',' constant)* ':' statement
    """

    expression: Expression
    cases: list[tuple[list[Any], Statement]]  # List of (constants, statement) pairs

    def accept(self, visitor: Any) -> Any:
        return visitor.visit_case_statement(self)

    def to_dict(self) -> dict:
        return {
            'type': 'CaseStatement',
            'expression': self.expression.to_dict(),
            'cases': [
                {
                    'constants': constants,
                    'statement': stmt.to_dict()
                }
                for constants, stmt in self.cases
            ]
        }


@dataclass
class ProcedureCall(Statement):
    """
    Represents a procedure call.

    Grammar:
        procedure_call -> IDENTIFIER '(' argument_list? ')'
    """

    name: str
    arguments: list['Expression']

    def accept(self, visitor: Any) -> Any:
        return visitor.visit_procedure_call(self)

    def to_dict(self) -> dict:
        return {
            'type': 'ProcedureCall',
            'name': self.name,
            'arguments': [arg.to_dict() for arg in self.arguments]
        }


@dataclass
class EmptyStatement(Statement):
    """
    Represents an empty statement (used for optional statements).
    """

    def accept(self, visitor: Any) -> Any:
        return visitor.visit_empty_statement(self)

    def to_dict(self) -> dict:
        return {'type': 'EmptyStatement'}
