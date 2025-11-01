"""
AST nodes for declarations (var, const, type, procedure, function).
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from .base import ASTNode


@dataclass
class VarDeclaration(ASTNode):
    """
    Represents a variable declaration.

    Grammar:
        var_declaration -> IDENTIFIER (',' IDENTIFIER)* ':' type_spec
    """

    identifiers: list[str]
    type_spec: TypeSpec

    def accept(self, visitor: Any) -> Any:
        return visitor.visit_var_declaration(self)

    def to_dict(self) -> dict:
        return {
            'type': 'VarDeclaration',
            'identifiers': self.identifiers,
            'type_spec': self.type_spec.to_dict()
        }


@dataclass
class ConstDeclaration(ASTNode):
    """
    Represents a constant declaration.

    Grammar:
        const_declaration -> IDENTIFIER '=' constant
    """

    identifier: str
    value: Any  # Could be number, string, or boolean

    def accept(self, visitor: Any) -> Any:
        return visitor.visit_const_declaration(self)

    def to_dict(self) -> dict:
        return {
            'type': 'ConstDeclaration',
            'identifier': self.identifier,
            'value': self.value
        }


@dataclass
class TypeDeclaration(ASTNode):
    """
    Represents a type declaration.

    Grammar:
        type_declaration -> IDENTIFIER '=' type_spec
    """

    identifier: str
    type_spec: TypeSpec

    def accept(self, visitor: Any) -> Any:
        return visitor.visit_type_declaration(self)

    def to_dict(self) -> dict:
        return {
            'type': 'TypeDeclaration',
            'identifier': self.identifier,
            'type_spec': self.type_spec.to_dict()
        }


@dataclass
class ProcedureDeclaration(ASTNode):
    """
    Represents a procedure declaration.

    Grammar:
        procedure_declaration -> 'procedure' IDENTIFIER '(' parameters? ')' ';' block ';'
    """

    name: str
    parameters: list[Parameter]
    block: ASTNode  # Block

    def accept(self, visitor: Any) -> Any:
        return visitor.visit_procedure_declaration(self)

    def to_dict(self) -> dict:
        return {
            'type': 'ProcedureDeclaration',
            'name': self.name,
            'parameters': [param.to_dict() for param in self.parameters],
            'block': self.block.to_dict()
        }


@dataclass
class FunctionDeclaration(ASTNode):
    """
    Represents a function declaration.

    Grammar:
        function_declaration -> 'function' IDENTIFIER '(' parameters? ')' ':' type_spec ';' block ';'
    """

    name: str
    parameters: list[Parameter]
    return_type: TypeSpec
    block: ASTNode  # Block

    def accept(self, visitor: Any) -> Any:
        return visitor.visit_function_declaration(self)

    def to_dict(self) -> dict:
        return {
            'type': 'FunctionDeclaration',
            'name': self.name,
            'parameters': [param.to_dict() for param in self.parameters],
            'return_type': self.return_type.to_dict(),
            'block': self.block.to_dict()
        }


@dataclass
class Parameter(ASTNode):
    """
    Represents a parameter in a procedure/function declaration.

    Grammar:
        parameter -> IDENTIFIER (',' IDENTIFIER)* ':' type_spec
    """

    identifiers: list[str]
    type_spec: TypeSpec

    def accept(self, visitor: Any) -> Any:
        return visitor.visit_parameter(self)

    def to_dict(self) -> dict:
        return {
            'type': 'Parameter',
            'identifiers': self.identifiers,
            'type_spec': self.type_spec.to_dict()
        }


@dataclass
class TypeSpec(ASTNode):
    """
    Represents a type specification.

    Grammar:
        type_spec -> simple_type | array_type | record_type
    """

    pass


@dataclass
class SimpleType(TypeSpec):
    """
    Represents a simple type (integer, real, boolean, char, or identifier).

    Grammar:
        simple_type -> IDENTIFIER
    """

    name: str

    def accept(self, visitor: Any) -> Any:
        return visitor.visit_simple_type(self)

    def to_dict(self) -> dict:
        return {
            'type': 'SimpleType',
            'name': self.name
        }


@dataclass
class ArrayType(TypeSpec):
    """
    Represents an array type.

    Grammar:
        array_type -> 'array' '[' simple_type ']' 'of' type_spec
        OR
        array_type -> 'array' '[' expression '..' expression ']' 'of' type_spec
    """

    index_type: Any  # Could be SimpleType or range (start..end)
    element_type: TypeSpec

    def accept(self, visitor: Any) -> Any:
        return visitor.visit_array_type(self)

    def to_dict(self) -> dict:
        if isinstance(self.index_type, tuple):
            # Range type (start..end)
            start = self.index_type[0].to_dict() if hasattr(
                self.index_type[0], 'to_dict') else self.index_type[0]
            end = self.index_type[1].to_dict() if hasattr(
                self.index_type[1], 'to_dict') else self.index_type[1]
            return {
                'type': 'ArrayType',
                'index_type': {
                    'type': 'Range',
                    'start': start,
                    'end': end
                },
                'element_type': self.element_type.to_dict()
            }
        else:
            return {
                'type': 'ArrayType',
                'index_type': self.index_type.to_dict() if hasattr(self.index_type, 'to_dict') else self.index_type,
                'element_type': self.element_type.to_dict()
            }


@dataclass
class RecordType(TypeSpec):
    """
    Represents a record type.

    Grammar:
        record_type -> 'record' field_list 'end'
    """

    fields: list[VarDeclaration]

    def accept(self, visitor: Any) -> Any:
        return visitor.visit_record_type(self)

    def to_dict(self) -> dict:
        return {
            'type': 'RecordType',
            'fields': [field.to_dict() for field in self.fields]
        }
