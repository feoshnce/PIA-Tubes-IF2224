"""
AST nodes for program-level structures.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from .base import ASTNode
from .statement import CompoundStatement


@dataclass
class Program(ASTNode):
    """
    Represents a Pascal-S program.

    Grammar:
        program -> 'program' IDENTIFIER ';' block '.'
    """

    name: str
    block: ASTNode  # Block

    def accept(self, visitor: Any) -> Any:
        return visitor.visit_program(self)

    def to_dict(self) -> dict:
        return {
            'type': 'Program',
            'name': self.name,
            'block': self.block.to_dict()
        }


@dataclass
class Block(ASTNode):
    """
    Represents a block in Pascal-S.

    Grammar:
        block -> declarations compound_statement
    """

    declarations: list[ASTNode]
    compound_statement: CompoundStatement

    def accept(self, visitor: Any) -> Any:
        return visitor.visit_block(self)

    def to_dict(self) -> dict:
        return {
            'type': 'Block',
            'declarations': [decl.to_dict() for decl in self.declarations],
            'compound_statement': self.compound_statement.to_dict()
        }
