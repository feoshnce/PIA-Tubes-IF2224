from typing import Any
from parse_tree import (
    Program, Block, VarDeclaration, ConstDeclaration,
    TypeDeclaration, ProcedureDeclaration, FunctionDeclaration, Parameter,
    SimpleType, ArrayType, RecordType, CompoundStatement, AssignmentStatement,
    IfStatement, WhileStatement, ForStatement, RepeatStatement, CaseStatement,
    ProcedureCall, EmptyStatement, BinaryOp, UnaryOp, Variable, Number, String, Char,
    Boolean, FunctionCall, ASTNode
)

class DecoratedASTPrinter:
    def __init__(self):
        self.lines = []
        self.indent_str = " " * 1
        self.branch = "├─ "
        self.last_branch = "└─ "
        self.pipe = "│  "
        self.empty = "   "

    def print(self, node: ASTNode) -> str:
        self.lines = []
        self.visit(node, "", True)
        return "\n".join(self.lines)

    def visit(self, node: Any, prefix: str, is_last: bool):
        if node is None:
            return

        # Determine node label and attributes
        label = self._get_node_label(node)
        attrs = self._get_node_attrs(node)
        
        connector = self.last_branch if is_last else self.branch
        
        # Root node doesn't have a connector prefix like children
        if not self.lines:
            line = f"{label}{attrs}"
            child_prefix = ""
        else:
            line = f"{prefix}{connector}{label}{attrs}"
            child_prefix = prefix + (self.empty if is_last else self.pipe)

        self.lines.append(line)

        # Visit children
        children = self._get_children(node)
        count = len(children)
        for i, child in enumerate(children):
            self.visit(child, child_prefix, i == count - 1)

    def _get_node_label(self, node: Any) -> str:
        if isinstance(node, Program):
            return f"ProgramNode(name: '{node.name}')"
        elif isinstance(node, Block):
            return "Block"
        elif isinstance(node, VarDeclaration):
            names = ",".join(f"'{n}'" for n in node.identifiers)
            return f"VarDecl({names})"
        elif isinstance(node, ConstDeclaration):
            return f"ConstDecl('{node.identifier}')"
        elif isinstance(node, TypeDeclaration):
            return f"TypeDecl('{node.identifier}')"
        elif isinstance(node, ProcedureDeclaration):
            return f"ProcDecl('{node.name}')"
        elif isinstance(node, FunctionDeclaration):
            return f"FuncDecl('{node.name}')"
        elif isinstance(node, Parameter):
            names = ",".join(f"'{n}'" for n in node.identifiers)
            return f"Param({names})"
        elif isinstance(node, CompoundStatement):
            return "CompoundStmt"
        elif isinstance(node, AssignmentStatement):
            return "Assign"
        elif isinstance(node, IfStatement):
            return "IfStmt"
        elif isinstance(node, WhileStatement):
            return "WhileStmt"
        elif isinstance(node, ForStatement):
            return "ForStmt"
        elif isinstance(node, RepeatStatement):
            return "RepeatStmt"
        elif isinstance(node, CaseStatement):
            return "CaseStmt"
        elif isinstance(node, ProcedureCall):
            return f"ProcCall('{node.name}')"
        elif isinstance(node, FunctionCall):
            return f"FuncCall('{node.name}')"
        elif isinstance(node, BinaryOp):
            return f"BinOp '{node.operator}'"
        elif isinstance(node, UnaryOp):
            return f"UnaryOp '{node.operator}'"
        elif isinstance(node, Variable):
            name = node.name if node.name else "<access>"
            if node.indices:
                return f"VarAccess('{name}'[])"
            if node.field:
                return f"VarAccess('.{node.field}')"
            return f"Variable('{name}')"
        elif isinstance(node, Number):
            return f"Number({node.value})"
        elif isinstance(node, String):
            return f"String('{node.value}')"
        elif isinstance(node, Char):
            return f"Char('{node.value}')"
        elif isinstance(node, Boolean):
            return f"Boolean({node.value})"
        elif isinstance(node, EmptyStatement):
            return "EmptyStmt"
        elif isinstance(node, SimpleType):
            return f"SimpleType('{node.name}')"
        elif isinstance(node, ArrayType):
            return "ArrayType"
        elif isinstance(node, RecordType):
            return "RecordType"
        elif isinstance(node, DecoratedList):
            return node.label
        
        return str(type(node).__name__)

    def _get_node_attrs(self, node: Any) -> str:
        parts = []
        
        # Attributes attached by SemanticVisitor
        if hasattr(node, 'tab_index') and node.tab_index is not None:
            parts.append(f"tab_index:{node.tab_index}")
        
        if hasattr(node, 'block_index') and node.block_index is not None:
            parts.append(f"block_index:{node.block_index}")

        if hasattr(node, 'sym_type') and node.sym_type is not None:
            parts.append(f"type:{node.sym_type}")
        
        if hasattr(node, 'sym_level') and node.sym_level is not None:
            parts.append(f"lev:{node.sym_level}")

        if not parts:
            return ""
        
        return " → " + ", ".join(parts)

    def _get_children(self, node: Any) -> list[Any]:
        children = []
        
        if isinstance(node, Program):
            children = [node.block]
        elif isinstance(node, Block):
            # Combine declarations and compound_statement into one list for visualization
            if node.declarations:
                children.append(DecoratedList("Declarations", node.declarations))
            children.append(node.compound_statement)
        elif isinstance(node, DecoratedList):
             children = node.items
        elif isinstance(node, VarDeclaration):
             # children = [node.type_spec] # Optional: hide type spec details if desired
             pass
        elif isinstance(node, ConstDeclaration):
             pass
        elif isinstance(node, TypeDeclaration):
             children = [node.type_spec]
        elif isinstance(node, ProcedureDeclaration):
             children = node.parameters + [node.block]
        elif isinstance(node, FunctionDeclaration):
             children = node.parameters + [node.return_type, node.block]
        elif isinstance(node, Parameter):
             pass
        elif isinstance(node, CompoundStatement):
             children = node.statements
        elif isinstance(node, AssignmentStatement):
             children = [node.variable, node.expression]
        elif isinstance(node, IfStatement):
             children = [node.condition, node.then_statement]
             if node.else_statement:
                 children.append(node.else_statement)
        elif isinstance(node, WhileStatement):
             children = [node.condition, node.body]
        elif isinstance(node, ForStatement):
             children = [node.start_expr, node.end_expr, node.body]
        elif isinstance(node, RepeatStatement):
             children = node.statements + [node.condition]
        elif isinstance(node, CaseStatement):
             children = [node.expression] + [case[1] for case in node.cases] # Simplifying case display
        elif isinstance(node, ProcedureCall):
             children = node.arguments
        elif isinstance(node, FunctionCall):
             children = node.arguments
        elif isinstance(node, BinaryOp):
             children = [node.left, node.right]
        elif isinstance(node, UnaryOp):
             children = [node.operand]
        elif isinstance(node, Variable):
             children = []
             if node.indices:
                 children.extend(node.indices)
             if node.next_access:
                 children.append(node.next_access)
        elif isinstance(node, ArrayType):
             children = [node.element_type]
             # Index type could be added if needed
        elif isinstance(node, RecordType):
             children = [field for field in node.fields]

        return children

class DecoratedList:
    """Helper class to group list of nodes under a label"""
    def __init__(self, label: str, items: list[Any]):
        self.label = label
        self.items = items
    
    def __repr__(self):
        return self.label

    def _get_node_label(self):
        return self.label
