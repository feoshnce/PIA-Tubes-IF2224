"""
Tree formatter for Parse Tree visualization.

This module provides functionality to format the parse tree
in a hierarchical tree structure with box-drawing characters.
"""

from typing import Any
from parse_tree import (
    ASTNode,
    Program,
    VarDeclaration,
    CompoundStatement,
    AssignmentStatement,
    IfStatement,
    WhileStatement,
    ForStatement,
    ProcedureCall,
    BinaryOp,
    UnaryOp,
    Variable,
    Number,
    String,
    Boolean,
    SimpleType,
    ArrayType,
    FunctionCall,
)
from syntax import Token


class TreeFormatter:
    """
    Formatter for parse tree visualization.

    Converts AST nodes into a tree structure with box-drawing characters.
    """

    def __init__(self, tokens: list[Token]):
        """
        Initialize the tree formatter.

        Args:
            tokens: List of original tokens (for terminal node display)
        """
        self.tokens = tokens
        self.output = []

    def format(self, node: ASTNode) -> str:
        """
        Format an AST node as a tree structure.

        Args:
            node: The root AST node

        Returns:
            String representation of the tree
        """
        self.output = []
        self._format_node(node, "", True)
        return "\n".join(self.output)

    def _format_node(self, node: Any, prefix: str, is_last: bool):
        """
        Recursively format a node and its children.

        Args:
            node: The node to format
            prefix: Current line prefix for indentation
            is_last: Whether this is the last child of its parent
        """
        if node is None:
            return

        # Determine connector
        connector = "└── " if is_last else "├── "

        # Handle wrapper nodes (declaration-part, statement-list, etc.)
        if hasattr(node, '_node_type'):
            node_name = node._node_type
            self.output.append(f"{prefix}{connector}<{node_name}>")

            # Update prefix for children
            child_prefix = prefix + ("    " if is_last else "│   ")

            # Get children
            children = node._children if hasattr(node, '_children') else []
            for i, child in enumerate(children):
                is_last_child = (i == len(children) - 1)
                self._format_node(child, child_prefix, is_last_child)

        # Format current node
        elif isinstance(node, ASTNode):
            # Non-terminal node
            node_name = self._get_node_name(node)
            self.output.append(f"{prefix}{connector}<{node_name}>")

            # Update prefix for children
            child_prefix = prefix + ("    " if is_last else "│   ")

            # Get children
            children = self._get_children(node)
            for i, child in enumerate(children):
                is_last_child = (i == len(children) - 1)
                self._format_node(child, child_prefix, is_last_child)

        elif isinstance(node, str):
            # Terminal node (keyword, operator, etc.)
            self.output.append(f"{prefix}{connector}{node}")

        elif isinstance(node, (int, float, bool)):
            # Literal value
            self.output.append(f"{prefix}{connector}{node}")

    def _get_node_name(self, node: ASTNode) -> str:
        """
        Get the non-terminal name for an AST node.

        Args:
            node: The AST node

        Returns:
            Non-terminal name
        """
        # Map AST node types to non-terminal names
        node_type = type(node).__name__

        mapping = {
            'Program': 'program',
            'Block': 'block',
            'VarDeclaration': 'var-declaration',
            'ConstDeclaration': 'const-declaration',
            'TypeDeclaration': 'type-declaration',
            'ProcedureDeclaration': 'procedure-declaration',
            'FunctionDeclaration': 'function-declaration',
            'Parameter': 'parameter',
            'SimpleType': 'type',
            'ArrayType': 'array-type',
            'RecordType': 'record-type',
            'CompoundStatement': 'compound-statement',
            'AssignmentStatement': 'assignment-statement',
            'IfStatement': 'if-statement',
            'WhileStatement': 'while-statement',
            'ForStatement': 'for-statement',
            'RepeatStatement': 'repeat-statement',
            'CaseStatement': 'case-statement',
            'ProcedureCall': 'procedure-call',
            'BinaryOp': 'expression',
            'UnaryOp': 'expression',
            'Variable': 'variable',
            'Number': 'expression',
            'String': 'expression',
            'Char': 'expression',
            'Boolean': 'expression',
            'FunctionCall': 'function-call',
        }

        return mapping.get(node_type, node_type.lower())

    def _get_children(self, node: ASTNode) -> list:
        """
        Get children nodes to display in the tree.

        Args:
            node: The AST node

        Returns:
            List of children (can be AST nodes or terminal strings)
        """
        children = []

        if isinstance(node, Program):
            children.append(self._format_token('KEYWORD', 'program'))
            children.append(self._format_token('IDENTIFIER', node.name))
            children.append(self._format_token('SEMICOLON', ';'))
            if node.block.declarations:
                children.append(self._create_declaration_part(
                    node.block.declarations))
            children.append(node.block.compound_statement)
            children.append(self._format_token('DOT', '.'))

        elif isinstance(node, VarDeclaration):
            children.append(self._format_token('KEYWORD', 'variabel'))
            children.append(self._create_var_list(node))

        elif isinstance(node, CompoundStatement):
            children.append(self._format_token('KEYWORD', 'mulai'))
            if node.statements:
                children.append(self._create_statement_list(node.statements))
            children.append(self._format_token('KEYWORD', 'selesai'))

        elif isinstance(node, AssignmentStatement):
            children.append(self._format_token(
                'IDENTIFIER', node.variable.name))
            children.append(self._format_token('ASSIGN_OPERATOR', ':='))
            children.append(node.expression)

        elif isinstance(node, IfStatement):
            children.append(self._format_token('KEYWORD', 'jika'))
            children.append(node.condition)
            children.append(self._format_token('KEYWORD', 'maka'))
            children.append(node.then_statement)
            if node.else_statement:
                children.append(self._format_token('KEYWORD', 'selain-itu'))
                children.append(node.else_statement)

        elif isinstance(node, WhileStatement):
            children.append(self._format_token('KEYWORD', 'selama'))
            children.append(node.condition)
            children.append(self._format_token('KEYWORD', 'lakukan'))
            children.append(node.body)

        elif isinstance(node, ForStatement):
            children.append(self._format_token('KEYWORD', 'untuk'))
            children.append(self._format_token('IDENTIFIER', node.variable))
            children.append(self._format_token('ASSIGN_OPERATOR', ':='))
            children.append(node.start_expr)
            children.append(self._format_token('KEYWORD', node.direction))
            children.append(node.end_expr)
            children.append(self._format_token('KEYWORD', 'lakukan'))
            children.append(node.body)

        elif isinstance(node, ProcedureCall):
            children.append(self._format_token('KEYWORD', node.name))
            if node.arguments:
                children.append(self._format_token('LPARENTHESIS', '('))
                children.append(self._create_parameter_list(node.arguments))
                children.append(self._format_token('RPARENTHESIS', ')'))

        elif isinstance(node, BinaryOp):
            children.append(node.left)
            children.append(self._format_operator(node.operator))
            children.append(node.right)

        elif isinstance(node, UnaryOp):
            children.append(self._format_operator(node.operator))
            children.append(node.operand)

        elif isinstance(node, Variable):
            children.append(self._format_token('IDENTIFIER', node.name))
            if node.index:
                children.append(self._format_token('LBRACKET', '['))
                children.append(node.index)
                children.append(self._format_token('RBRACKET', ']'))

        elif isinstance(node, Number):
            children.append(self._format_token('NUMBER', str(node.value)))

        elif isinstance(node, String):
            children.append(self._format_token('STRING_LITERAL', node.value))

        elif isinstance(node, Boolean):
            children.append(self._format_token(
                'IDENTIFIER', str(node.value).lower()))

        elif isinstance(node, SimpleType):
            children.append(self._format_token('KEYWORD', node.name))

        elif isinstance(node, ArrayType):
            children.append(self._format_token('KEYWORD', 'larik'))
            children.append(self._format_token('LBRACKET', '['))
            if isinstance(node.index_type, tuple):
                # Range
                children.append(node.index_type[0])
                children.append(self._format_token('RANGE_OPERATOR', '..'))
                children.append(node.index_type[1])
            else:
                children.append(node.index_type)
            children.append(self._format_token('RBRACKET', ']'))
            children.append(self._format_token('KEYWORD', 'dari'))
            children.append(node.element_type)

        elif isinstance(node, FunctionCall):
            children.append(self._format_token('IDENTIFIER', node.name))
            children.append(self._format_token('LPARENTHESIS', '('))
            if node.arguments:
                children.append(self._create_parameter_list(node.arguments))
            children.append(self._format_token('RPARENTHESIS', ')'))

        # Handle custom wrapper nodes
        elif hasattr(node, '_node_type'):
            if node._node_type == 'declaration-part':
                return node._children
            elif node._node_type == 'statement-list':
                return node._children
            elif node._node_type == 'parameter-list':
                return node._children
            elif node._node_type == 'var-list':
                return node._children
            elif node._node_type == 'identifier-list':
                return node._children

        return children

    def _format_token(self, token_type: str, value: str) -> str:
        """Format a terminal token."""
        return f"{token_type}({value})"

    def _format_operator(self, op: str) -> str:
        """Format an operator token."""
        if op in ('+', '-', '*', '/', 'bagi', 'mod'):
            return self._format_token('ARITHMETIC_OPERATOR', op)
        elif op in ('=', '<>', '<', '<=', '>', '>='):
            return self._format_token('RELATIONAL_OPERATOR', op)
        elif op in ('dan', 'atau', 'tidak'):
            return self._format_token('LOGICAL_OPERATOR', op)
        else:
            return self._format_token('OPERATOR', op)

    def _create_declaration_part(self, declarations: list) -> Any:
        """Create declaration-part wrapper node."""
        class DeclarationPart:
            def __init__(self, children):
                self._node_type = 'declaration-part'
                self._children = children
        return DeclarationPart(declarations)

    def _create_statement_list(self, statements: list) -> Any:
        """Create statement-list wrapper node."""
        class StatementList:
            def __init__(self, children):
                self._node_type = 'statement-list'
                self._children = []
                for i, stmt in enumerate(children):
                    self._children.append(stmt)
                    if i < len(children) - 1:
                        self._children.append('SEMICOLON(;)')
        return StatementList(statements)

    def _create_parameter_list(self, params: list) -> Any:
        """Create parameter-list wrapper node."""
        class ParameterList:
            def __init__(self, children):
                self._node_type = 'parameter-list'
                self._children = []
                for i, param in enumerate(children):
                    self._children.append(param)
                    if i < len(children) - 1:
                        self._children.append('COMMA(,)')
        return ParameterList(params)

    def _create_var_list(self, var_decl: VarDeclaration) -> Any:
        """Create var-list wrapper node."""
        class VarList:
            def __init__(self, var_decl):
                self._node_type = 'var-list'
                self._children = []
                # Add identifier list
                id_list = self._create_identifier_list(var_decl.identifiers)
                self._children.append(id_list)
                # Add colon
                self._children.append('COLON(:)')
                # Add type
                self._children.append(var_decl.type_spec)
                # Add semicolon
                self._children.append('SEMICOLON(;)')

            def _create_identifier_list(self, identifiers: list) -> Any:
                class IdentifierList:
                    def __init__(self, ids):
                        self._node_type = 'identifier-list'
                        self._children = []
                        for i, id_name in enumerate(ids):
                            self._children.append(f'IDENTIFIER({id_name})')
                            if i < len(ids) - 1:
                                self._children.append('COMMA(,)')
                return IdentifierList(identifiers)

        return VarList(var_decl)

    # Make the class instances compatible with isinstance checks
    def __instancecheck__(cls, instance):
        return hasattr(instance, '_node_type')


def format_parse_tree(root: ASTNode, tokens: list[Token] = None) -> str:
    """
    Format a parse tree for display.

    Args:
        root: Root node of the parse tree
        tokens: Original tokens (optional)

    Returns:
        Formatted tree string
    """
    formatter = TreeFormatter(tokens or [])
    return formatter.format(root)
