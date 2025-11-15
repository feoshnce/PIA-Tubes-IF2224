"""
Tree formatter for Parse Tree visualization.

This module provides functionality to format the parse tree
in a hierarchical tree structure with box-drawing characters.
"""

from typing import Any
from parse_tree import (
    ASTNode,
    Program,
    Block,
    VarDeclaration,
    ConstDeclaration,
    TypeDeclaration,
    ProcedureDeclaration,
    FunctionDeclaration,
    Parameter,
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
    ParenthesizedExpression,
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
        self._format_node(node, "", True, is_root=True)
        return "\n".join(self.output)

    def _format_node(self, node: Any, prefix: str, is_last: bool, is_root: bool = False):
        """
        Recursively format a node and its children.

        Args:
            node: The node to format
            prefix: Current line prefix for indentation
            is_last: Whether this is the last child of its parent
            is_root: Whether this is the root node
        """
        if node is None:
            return

        # Determine connector (root node has no connector)
        if is_root:
            connector = ""
        else:
            connector = "└── " if is_last else "├── "

        # Handle wrapper nodes (declaration-part, statement-list, etc.)
        if hasattr(node, '_node_type'):
            node_name = node._node_type
            self.output.append(f"{prefix}{connector}<{node_name}>")

            # Update prefix for children (root children have no prefix)
            if is_root:
                child_prefix = ""
            else:
                child_prefix = prefix + ("    " if is_last else "│   ")

            # Get children
            children = node._children if hasattr(node, '_children') else []
            for i, child in enumerate(children):
                is_last_child = (i == len(children) - 1)
                self._format_node(child, child_prefix, is_last_child)

        # Format current node
        elif isinstance(node, ASTNode):
            # Special handling for ParenthesizedExpression - don't create a wrapper node
            if isinstance(node, ParenthesizedExpression):
                # Just format the children directly without creating a node
                children = self._get_children(node)
                for i, child in enumerate(children):
                    is_last_child = (i == len(children) - 1)
                    self._format_node(child, prefix, is_last if i == len(children) - 1 else False)
                return

            # Non-terminal node
            node_name = self._get_node_name(node)
            self.output.append(f"{prefix}{connector}<{node_name}>")

            # Update prefix for children (root children have no prefix)
            if is_root:
                child_prefix = ""
            else:
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
            'Parameter': 'parameter-group',
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
            'ProcedureCall': 'procedure/function-call',
            'BinaryOp': 'expression',
            'UnaryOp': 'expression',
            'Variable': 'variable',
            'Number': 'expression',
            'String': 'expression',
            'Char': 'expression',
            'Boolean': 'expression',
            'FunctionCall': 'procedure/function-call',
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
            children.append(self._create_program_header(node.name))
            if node.block.declarations:
                children.append(self._create_declaration_part(
                    node.block.declarations))
            children.append(node.block.compound_statement)
            children.append(self._format_token('DOT', '.'))

        elif isinstance(node, VarDeclaration):
            # For individual var declaration groups
            children.append(self._create_identifier_list(node.identifiers))
            children.append(self._format_token('COLON', ':'))
            # SimpleType already maps to 'type', so don't wrap it
            # ArrayType/RecordType need wrapping
            if isinstance(node.type_spec, SimpleType):
                children.append(node.type_spec)
            else:
                children.append(self._create_type_wrapper(node.type_spec))
            children.append(self._format_token('SEMICOLON', ';'))

        elif isinstance(node, ConstDeclaration):
            # For individual const declaration
            children.append(self._format_token('IDENTIFIER', node.identifier))
            children.append(self._format_token('ASSIGN_OPERATOR', '='))
            # Format the value based on its type
            if isinstance(node.value, (int, float)):
                children.append(self._format_token('NUMBER', str(node.value)))
            elif isinstance(node.value, str):
                children.append(self._format_token('STRING_LITERAL', node.value))
            elif isinstance(node.value, bool):
                children.append(self._format_token('IDENTIFIER', str(node.value).lower()))
            else:
                children.append(self._format_token('IDENTIFIER', str(node.value)))
            children.append(self._format_token('SEMICOLON', ';'))

        elif isinstance(node, TypeDeclaration):
            # For individual type declaration
            children.append(self._format_token('IDENTIFIER', node.identifier))
            children.append(self._format_token('ASSIGN_OPERATOR', '='))
            children.append(node.type_spec)
            children.append(self._format_token('SEMICOLON', ';'))

        elif isinstance(node, CompoundStatement):
            children.append(self._format_token('KEYWORD', 'mulai'))
            if node.statements:
                children.append(self._create_statement_list(node.statements))
            children.append(self._format_token('KEYWORD', 'selesai'))

        elif isinstance(node, Block):
            if node.declarations:
                children.append(self._create_declaration_part(node.declarations))
            children.append(node.compound_statement)

        elif isinstance(node, ProcedureDeclaration):
            children.append(self._format_token('KEYWORD', 'prosedur'))
            children.append(self._format_token('IDENTIFIER', node.name))
            if node.parameters:
                children.append(self._create_formal_parameter_list(node.parameters))
            children.append(self._format_token('SEMICOLON', ';'))
            children.append(node.block)
            children.append(self._format_token('SEMICOLON', ';'))

        elif isinstance(node, FunctionDeclaration):
            children.append(self._format_token('KEYWORD', 'fungsi'))
            children.append(self._format_token('IDENTIFIER', node.name))
            if node.parameters:
                children.append(self._create_formal_parameter_list(node.parameters))
            children.append(self._format_token('COLON', ':'))
            children.append(node.return_type)
            children.append(self._format_token('SEMICOLON', ';'))
            children.append(node.block)
            children.append(self._format_token('SEMICOLON', ';'))

        elif isinstance(node, Parameter):
            children.append(self._create_identifier_list(node.identifiers))
            children.append(self._format_token('COLON', ':'))
            children.append(node.type_spec)

        elif isinstance(node, AssignmentStatement):
            # Add variable components directly without <variable> wrapper
            children.append(self._format_token('IDENTIFIER', node.variable.name))
            if node.variable.index:
                children.append(self._format_token('LBRACKET', '['))
                children.append(self._create_expression(node.variable.index))
                children.append(self._format_token('RBRACKET', ']'))
            elif node.variable.field:
                children.append(self._format_token('DOT', '.'))
                children.append(self._format_token('IDENTIFIER', node.variable.field))
            children.append(self._format_token('ASSIGN_OPERATOR', ':='))
            children.append(self._create_expression(node.expression))

        elif isinstance(node, IfStatement):
            children.append(self._format_token('KEYWORD', 'jika'))
            children.append(self._create_expression(node.condition))
            children.append(self._format_token('KEYWORD', 'maka'))
            children.append(node.then_statement)
            if node.else_statement:
                children.append(self._format_token('KEYWORD', 'selain-itu'))
                children.append(node.else_statement)

        elif isinstance(node, WhileStatement):
            children.append(self._format_token('KEYWORD', 'selama'))
            children.append(self._create_expression(node.condition))
            children.append(self._format_token('KEYWORD', 'lakukan'))
            children.append(node.body)

        elif isinstance(node, ForStatement):
            children.append(self._format_token('KEYWORD', 'untuk'))
            children.append(self._format_token('IDENTIFIER', node.variable))
            children.append(self._format_token('ASSIGN_OPERATOR', ':='))
            children.append(self._create_expression(node.start_expr))
            children.append(self._format_token('KEYWORD', node.direction))
            children.append(self._create_expression(node.end_expr))
            children.append(self._format_token('KEYWORD', 'lakukan'))
            children.append(node.body)

        elif isinstance(node, ProcedureCall):
            children.append(self._format_token('IDENTIFIER', node.name))
            children.append(self._format_token('LPARENTHESIS', '('))
            if node.arguments:
                children.append(self._create_parameter_list_with_expressions(node.arguments))
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
                children.append(self._create_expression(node.index))
                children.append(self._format_token('RBRACKET', ']'))

        elif isinstance(node, Number):
            children.append(self._format_token('NUMBER', str(node.value)))

        elif isinstance(node, String):
            children.append(self._format_token('STRING_LITERAL', node.value))

        elif isinstance(node, Boolean):
            children.append(self._format_token(
                'IDENTIFIER', str(node.value).lower()))

        elif isinstance(node, SimpleType):
            # Check if it's a built-in type or custom type
            builtin_types = ('integer', 'real', 'boolean', 'char')
            if node.name.lower() in builtin_types:
                children.append(self._format_token('KEYWORD', node.name))
            else:
                children.append(self._format_token('IDENTIFIER', node.name))

        elif isinstance(node, ArrayType):
            # Check if this is a subrange type (no element_type) or array type
            if node.element_type is None:
                # Subrange type (e.g., 1..100)
                children.append(self._create_range(node.index_type))
            else:
                # Array type
                children.append(self._format_token('KEYWORD', 'larik'))
                children.append(self._format_token('LBRACKET', '['))
                if isinstance(node.index_type, tuple):
                    # Range
                    children.append(self._create_range(node.index_type))
                else:
                    children.append(node.index_type)
                children.append(self._format_token('RBRACKET', ']'))
                children.append(self._format_token('KEYWORD', 'dari'))
                children.append(node.element_type)

        elif isinstance(node, ParenthesizedExpression):
            # ParenthesizedExpression should be transparent - just expand to LPAREN + expr + RPAREN
            # This should not create its own node
            children.append(self._format_token('LPARENTHESIS', '('))
            children.append(self._create_expression(node.expression))
            children.append(self._format_token('RPARENTHESIS', ')'))

        elif isinstance(node, FunctionCall):
            children.append(self._format_token('IDENTIFIER', node.name))
            children.append(self._format_token('LPARENTHESIS', '('))
            if node.arguments:
                children.append(self._create_parameter_list_with_expressions(node.arguments))
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
            elif node._node_type == 'var-declaration':
                return node._children
            elif node._node_type == 'expression':
                return node._children
            elif node._node_type == 'simple-expression':
                return node._children
            elif node._node_type == 'term':
                return node._children
            elif node._node_type == 'factor':
                return node._children
            elif node._node_type == 'relational-operator':
                return node._children
            elif node._node_type == 'additive-operator':
                return node._children
            elif node._node_type == 'multiplicative-operator':
                return node._children
            elif node._node_type == 'formal-parameter-list':
                return node._children
            elif node._node_type == 'subprogram-declaration':
                return node._children
            elif node._node_type == 'range':
                return node._children
            elif node._node_type == 'const-declaration':
                return node._children
            elif node._node_type == 'type-declaration':
                return node._children
            elif node._node_type == 'type':
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

    def _create_range(self, range_tuple) -> Any:
        """Create range wrapper node."""
        class RangeWrapper:
            def __init__(self, range_expr, formatter):
                self._node_type = 'range'
                self._children = []
                if isinstance(range_expr, tuple) and len(range_expr) == 2:
                    self._children.append(formatter._create_expression(range_expr[0]))
                    self._children.append('RANGE_OPERATOR(..)')
                    self._children.append(formatter._create_expression(range_expr[1]))
        return RangeWrapper(range_tuple, self)

    def _create_program_header(self, name: str) -> Any:
        """Create program-header wrapper node."""
        class ProgramHeader:
            def __init__(self, name):
                self._node_type = 'program-header'
                self._children = [
                    'KEYWORD(program)',
                    f'IDENTIFIER({name})',
                    'SEMICOLON(;)'
                ]
        return ProgramHeader(name)

    def _create_type_wrapper(self, type_spec) -> Any:
        """Create <type> wrapper node."""
        class TypeWrapper:
            def __init__(self, type_node):
                self._node_type = 'type'
                self._children = [type_node]
        return TypeWrapper(type_spec)

    def _create_identifier_list(self, identifiers: list) -> Any:
        """Create identifier-list wrapper node."""
        class IdentifierList:
            def __init__(self, ids):
                self._node_type = 'identifier-list'
                self._children = []
                for i, id_name in enumerate(ids):
                    self._children.append(f'IDENTIFIER({id_name})')
                    if i < len(ids) - 1:
                        self._children.append('COMMA(,)')
        return IdentifierList(identifiers)

    def _create_expression(self, expr_node) -> Any:
        """Create expression wrapper with proper hierarchy."""
        from parse_tree import BinaryOp

        class ExpressionWrapper:
            def __init__(self, expr, formatter):
                self._node_type = 'expression'
                self._children = []

                # Check if it's a relational expression
                if isinstance(expr, BinaryOp) and expr.operator in ('=', '<>', '<', '<=', '>', '>='):
                    # Left side
                    self._children.append(formatter._create_simple_expression(expr.left))
                    # Relational operator
                    self._children.append(formatter._create_relational_operator(expr.operator))
                    # Right side
                    self._children.append(formatter._create_simple_expression(expr.right))
                else:
                    # Just wrap in simple-expression
                    self._children.append(formatter._create_simple_expression(expr))

        return ExpressionWrapper(expr_node, self)

    def _create_simple_expression(self, expr_node) -> Any:
        """Create simple-expression wrapper."""
        from parse_tree import BinaryOp

        class SimpleExpressionWrapper:
            def __init__(self, expr, formatter):
                self._node_type = 'simple-expression'
                self._children = []

                # Check if it's a binary operation with additive operator
                if isinstance(expr, BinaryOp) and expr.operator in ('+', '-', 'atau'):
                    # Left side - recursively handle if also additive BinaryOp
                    if isinstance(expr.left, BinaryOp) and expr.left.operator in ('+', '-', 'atau'):
                        # Flatten: simple-expression contains multiple term/operator pairs
                        left_simple = formatter._create_simple_expression(expr.left)
                        # Extract children from left simple-expression and add to current
                        if hasattr(left_simple, '_children'):
                            self._children.extend(left_simple._children)
                    else:
                        self._children.append(formatter._create_term(expr.left))
                    # Operator
                    self._children.append(formatter._create_additive_operator(expr.operator))
                    # Right side - always a term
                    self._children.append(formatter._create_term(expr.right))
                else:
                    # Just wrap in term
                    self._children.append(formatter._create_term(expr))

        return SimpleExpressionWrapper(expr_node, self)

    def _create_term(self, expr_node) -> Any:
        """Create term wrapper."""
        from parse_tree import BinaryOp

        class TermWrapper:
            def __init__(self, expr, formatter):
                self._node_type = 'term'
                self._children = []

                # Check if it's a binary operation with multiplicative operator
                if isinstance(expr, BinaryOp) and expr.operator in ('*', '/', 'bagi', 'mod', 'dan'):
                    # Left side - recursively handle if also multiplicative BinaryOp
                    if isinstance(expr.left, BinaryOp) and expr.left.operator in ('*', '/', 'bagi', 'mod', 'dan'):
                        # Flatten: term contains multiple factor/operator pairs
                        left_term = formatter._create_term(expr.left)
                        # Extract children from left term and add to current term
                        if hasattr(left_term, '_children'):
                            self._children.extend(left_term._children)
                    else:
                        self._children.append(formatter._create_factor(expr.left))
                    # Operator
                    self._children.append(formatter._create_multiplicative_operator(expr.operator))
                    # Right side - always a factor
                    self._children.append(formatter._create_factor(expr.right))
                else:
                    # Just wrap in factor
                    self._children.append(formatter._create_factor(expr))

        return TermWrapper(expr_node, self)

    def _create_factor(self, expr_node) -> Any:
        """Create factor wrapper."""
        from parse_tree import Number, Variable, String, Char, Boolean, FunctionCall, ParenthesizedExpression, UnaryOp

        class FactorWrapper:
            def __init__(self, expr, formatter):
                self._node_type = 'factor'
                self._children = []

                # Terminal nodes should be formatted as tokens
                if isinstance(expr, Number):
                    self._children.append(f'NUMBER({expr.value})')
                elif isinstance(expr, Variable):
                    if expr.index:
                        # Variable with array index
                        self._children.append(f'IDENTIFIER({expr.name})')
                        self._children.append('LBRACKET([)')
                        self._children.append(formatter._create_expression(expr.index))
                        self._children.append('RBRACKET(])')
                    else:
                        self._children.append(f'IDENTIFIER({expr.name})')
                elif isinstance(expr, String):
                    self._children.append(f'STRING_LITERAL({expr.value})')
                elif isinstance(expr, Char):
                    self._children.append(f'CHAR_LITERAL({expr.value})')
                elif isinstance(expr, Boolean):
                    self._children.append(f'IDENTIFIER({str(expr.value).lower()})')
                elif isinstance(expr, ParenthesizedExpression):
                    # Parenthesized expression
                    self._children.append('LPARENTHESIS(()')
                    self._children.append(formatter._create_expression(expr.expression))
                    self._children.append('RPARENTHESIS())')
                elif isinstance(expr, UnaryOp):
                    # Unary operator (e.g., "tidak factor" or "+/- factor")
                    self._children.append(formatter._format_operator(expr.operator))
                    self._children.append(formatter._create_factor(expr.operand))
                elif isinstance(expr, FunctionCall):
                    # Function call in factor
                    self._children.append(expr)
                else:
                    # For other expression types, pass through
                    self._children.append(expr)

        return FactorWrapper(expr_node, self)

    def _create_relational_operator(self, op: str) -> Any:
        """Create relational-operator wrapper."""
        class RelationalOperatorWrapper:
            def __init__(self, operator):
                self._node_type = 'relational-operator'
                self._children = [f'RELATIONAL_OPERATOR({operator})']
        return RelationalOperatorWrapper(op)

    def _create_additive_operator(self, op: str) -> Any:
        """Create additive-operator wrapper."""
        class AdditiveOperatorWrapper:
            def __init__(self, operator):
                self._node_type = 'additive-operator'
                if operator in ('+', '-'):
                    self._children = [f'ARITHMETIC_OPERATOR({operator})']
                elif operator == 'atau':
                    self._children = [f'LOGICAL_OPERATOR({operator})']
        return AdditiveOperatorWrapper(op)

    def _create_multiplicative_operator(self, op: str) -> Any:
        """Create multiplicative-operator wrapper."""
        class MultiplicativeOperatorWrapper:
            def __init__(self, operator):
                self._node_type = 'multiplicative-operator'
                if operator in ('*', '/', 'bagi', 'mod'):
                    self._children = [f'ARITHMETIC_OPERATOR({operator})']
                elif operator == 'dan':
                    self._children = [f'LOGICAL_OPERATOR({operator})']
        return MultiplicativeOperatorWrapper(op)

    def _create_formal_parameter_list(self, parameters: list) -> Any:
        """Create formal-parameter-list wrapper."""
        class FormalParameterList:
            def __init__(self, params):
                self._node_type = 'formal-parameter-list'
                self._children = ['LPARENTHESIS(()']
                # Add all parameter groups
                for param in params:
                    self._children.append(param)
                self._children.append('RPARENTHESIS())')
        return FormalParameterList(parameters)

    def _create_declaration_part(self, declarations: list) -> Any:
        """Create declaration-part wrapper node."""
        formatter = self  # Capture formatter instance

        class DeclarationPart:
            def __init__(self, children):
                self._node_type = 'declaration-part'
                self._children = []

                # Group different declaration types
                i = 0
                while i < len(children):
                    child_class = children[i].__class__.__name__ if hasattr(children[i], '__class__') else None

                    if child_class == 'ConstDeclaration':
                        # Collect all consecutive ConstDeclarations
                        const_decls = []
                        while i < len(children) and hasattr(children[i], '__class__') and children[i].__class__.__name__ == 'ConstDeclaration':
                            const_decls.append(children[i])
                            i += 1
                        # Create wrapper for all const declarations
                        self._children.append(self._create_const_declaration_wrapper(const_decls))

                    elif child_class == 'TypeDeclaration':
                        # Collect all consecutive TypeDeclarations
                        type_decls = []
                        while i < len(children) and hasattr(children[i], '__class__') and children[i].__class__.__name__ == 'TypeDeclaration':
                            type_decls.append(children[i])
                            i += 1
                        # Create wrapper for all type declarations
                        self._children.append(self._create_type_declaration_wrapper(type_decls))

                    elif child_class == 'VarDeclaration':
                        # Collect all consecutive VarDeclarations
                        var_decls = []
                        while i < len(children) and hasattr(children[i], '__class__') and children[i].__class__.__name__ == 'VarDeclaration':
                            var_decls.append(children[i])
                            i += 1
                        # Create wrapper for all var declarations
                        self._children.append(self._create_var_declaration_wrapper(var_decls))

                    elif child_class in ('ProcedureDeclaration', 'FunctionDeclaration'):
                        # Wrap in subprogram-declaration
                        self._children.append(self._create_subprogram_declaration_wrapper(children[i]))
                        i += 1

                    else:
                        self._children.append(children[i])
                        i += 1

            def _create_const_declaration_wrapper(self, const_decls: list) -> Any:
                """Create const-declaration wrapper for multiple ConstDeclaration nodes."""
                class ConstDeclarationWrapper:
                    def __init__(self, decls):
                        self._node_type = 'const-declaration'
                        self._children = ['KEYWORD(konstanta)']
                        # Flatten all const declarations
                        for decl in decls:
                            self._children.append(f'IDENTIFIER({decl.identifier})')
                            self._children.append('ASSIGN_OPERATOR(=)')
                            # Format value
                            if isinstance(decl.value, (int, float)):
                                self._children.append(f'NUMBER({decl.value})')
                            elif isinstance(decl.value, str):
                                self._children.append(f'STRING_LITERAL({decl.value})')
                            elif isinstance(decl.value, bool):
                                self._children.append(f'IDENTIFIER({str(decl.value).lower()})')
                            else:
                                self._children.append(f'IDENTIFIER({decl.value})')
                            self._children.append('SEMICOLON(;)')
                return ConstDeclarationWrapper(const_decls)

            def _create_type_declaration_wrapper(self, type_decls: list) -> Any:
                """Create type-declaration wrapper for multiple TypeDeclaration nodes."""
                class TypeDeclarationWrapper:
                    def __init__(self, decls):
                        self._node_type = 'type-declaration'
                        self._children = ['KEYWORD(tipe)']
                        # Flatten all type declarations
                        for decl in decls:
                            self._children.append(f'IDENTIFIER({decl.identifier})')
                            self._children.append('ASSIGN_OPERATOR(=)')
                            # Wrap type_spec in <type> node
                            self._children.append(formatter._create_type_wrapper(decl.type_spec))
                            self._children.append('SEMICOLON(;)')
                return TypeDeclarationWrapper(type_decls)

            def _create_var_declaration_wrapper(self, var_decls: list) -> Any:
                """Create var-declaration wrapper for multiple VarDeclaration nodes."""
                class VarDeclarationWrapper:
                    def __init__(self, decls):
                        self._node_type = 'var-declaration'
                        self._children = ['KEYWORD(variabel)']
                        # Flatten all var declaration groups - add their contents directly
                        for decl in decls:
                            # Add identifier list
                            self._children.append(formatter._create_identifier_list(decl.identifiers))
                            # Add colon
                            self._children.append('COLON(:)')
                            # Add type - SimpleType already maps to 'type', so don't wrap
                            # ArrayType/RecordType need wrapping
                            if isinstance(decl.type_spec, SimpleType):
                                self._children.append(decl.type_spec)
                            else:
                                self._children.append(formatter._create_type_wrapper(decl.type_spec))
                            # Add semicolon
                            self._children.append('SEMICOLON(;)')
                return VarDeclarationWrapper(var_decls)

            def _create_subprogram_declaration_wrapper(self, subprogram) -> Any:
                """Create subprogram-declaration wrapper."""
                class SubprogramDeclarationWrapper:
                    def __init__(self, subprog):
                        self._node_type = 'subprogram-declaration'
                        self._children = [subprog]
                return SubprogramDeclarationWrapper(subprogram)

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
        """Create parameter-list wrapper node for formal parameters."""
        class ParameterList:
            def __init__(self, children):
                self._node_type = 'parameter-list'
                self._children = []
                for i, param in enumerate(children):
                    self._children.append(param)
                    if i < len(children) - 1:
                        self._children.append('COMMA(,)')
        return ParameterList(params)

    def _create_parameter_list_with_expressions(self, exprs: list) -> Any:
        """Create parameter-list wrapper for actual parameters (expressions)."""
        class ParameterListExpressions:
            def __init__(self, expressions, formatter):
                self._node_type = 'parameter-list'
                self._children = []
                for i, expr in enumerate(expressions):
                    self._children.append(formatter._create_expression(expr))
                    if i < len(expressions) - 1:
                        self._children.append('COMMA(,)')
        return ParameterListExpressions(exprs, self)


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
