"""
Abstract Syntax Tree (AST) module.
"""

from .base import ASTNode
from .program import Program, Block
from .declaration import (
    VarDeclaration,
    ConstDeclaration,
    TypeDeclaration,
    ProcedureDeclaration,
    FunctionDeclaration,
    Parameter,
    TypeSpec,
    SimpleType,
    ArrayType,
    RecordType,
)
from .statement import (
    Statement,
    CompoundStatement,
    AssignmentStatement,
    IfStatement,
    WhileStatement,
    ForStatement,
    RepeatStatement,
    CaseStatement,
    ProcedureCall,
    EmptyStatement,
)
from .expression import (
    Expression,
    BinaryOp,
    UnaryOp,
    Variable,
    Number,
    String,
    Char,
    Boolean,
    FunctionCall,
)

__all__ = [
    # Base
    "ASTNode",
    # Program
    "Program",
    "Block",
    # Declarations
    "VarDeclaration",
    "ConstDeclaration",
    "TypeDeclaration",
    "ProcedureDeclaration",
    "FunctionDeclaration",
    "Parameter",
    "TypeSpec",
    "SimpleType",
    "ArrayType",
    "RecordType",
    # Statements
    "Statement",
    "CompoundStatement",
    "AssignmentStatement",
    "IfStatement",
    "WhileStatement",
    "ForStatement",
    "RepeatStatement",
    "CaseStatement",
    "ProcedureCall",
    "EmptyStatement",
    # Expressions
    "Expression",
    "BinaryOp",
    "UnaryOp",
    "Variable",
    "Number",
    "String",
    "Char",
    "Boolean",
    "FunctionCall",
]
