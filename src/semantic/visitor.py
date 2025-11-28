from typing import Any, Optional
from parse_tree import (
    Program, Block, VarDeclaration, ConstDeclaration,
    TypeDeclaration, ProcedureDeclaration, FunctionDeclaration, Parameter,
    SimpleType, ArrayType, RecordType,  CompoundStatement, AssignmentStatement,
    IfStatement, WhileStatement, ForStatement, RepeatStatement, CaseStatement,
    ProcedureCall, EmptyStatement, BinaryOp, UnaryOp, Variable, Number, String, Char,
    Boolean, FunctionCall, ASTNode
)
from .symbol_table import SymbolTable, ObjectKind
from .types import (
    Type, SimpleTypeKind,
    INTEGER_TYPE, REAL_TYPE, BOOLEAN_TYPE, CHAR_TYPE, STRING_TYPE, VOID_TYPE,
    ArrayTypeInfo, RecordTypeInfo
)
from error import (
    UndeclaredIdentifierError,
    DuplicateDeclarationError,
    TypeMismatchError,
    InvalidOperationError,
    InvalidArrayIndexError,
    InvalidRecordAccessError,
    InvalidFunctionCallError
)


from .builtin_definitions import RESERVED_WORDS, STANDARD_LIBRARY

class SemanticVisitor:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.type_map: dict[str, Type] = {
            'integer': INTEGER_TYPE,
            'real': REAL_TYPE,
            'boolean': BOOLEAN_TYPE,
            'char': CHAR_TYPE,
            'string': STRING_TYPE
        }
        self.current_function_type: Optional[Type] = None
        self._init_builtins()

    def visit_program(self, node: Program) -> Any:
        self.symbol_table.enter(
            name=node.name,
            obj_kind=ObjectKind.PROGRAM,
            type=VOID_TYPE,
            level=0,
            ref=0
        )
        self.visit(node.block)
        return node

    def visit_block(self, node: Block) -> Any:
        for decl in node.declarations:
            self.visit(decl)
        self.visit(node.compound_statement)
        return node

    def visit_var_declaration(self, node: VarDeclaration) -> Any:
        type_spec = self.visit(node.type_spec)
        array_ref = type_spec.array_info.ref_index if type_spec.is_array() else 0

        for identifier in node.identifiers:
            if self.symbol_table.lookup_current_scope(identifier) is not None:
                raise DuplicateDeclarationError(identifier)

            tab_idx = self.symbol_table.enter(
                name=identifier,
                obj_kind=ObjectKind.VARIABLE,
                type=type_spec,
                ref=array_ref
            )

            node.tab_index = tab_idx
            node.sym_type = type_spec
            node.sym_level = self.symbol_table.level

        return node

    def visit_const_declaration(self, node: ConstDeclaration) -> Any:
        if self.symbol_table.lookup_current_scope(node.identifier) is not None:
            raise DuplicateDeclarationError(node.identifier)

        const_type = self._infer_const_type(node.value)
        self.symbol_table.enter(
            name=node.identifier,
            obj_kind=ObjectKind.CONSTANT,
            type=const_type
        )

        return node

    def visit_type_declaration(self, node: TypeDeclaration) -> Any:
        if self.symbol_table.lookup_current_scope(node.identifier) is not None:
            raise DuplicateDeclarationError(node.identifier)

        type_spec = self.visit(node.type_spec)
        self.type_map[node.identifier.lower()] = type_spec

        self.symbol_table.enter(
            name=node.identifier,
            obj_kind=ObjectKind.TYPE,
            type=type_spec
        )

        return node

    def visit_procedure_declaration(self, node: ProcedureDeclaration) -> Any:
        if self.symbol_table.lookup_current_scope(node.name) is not None:
            raise DuplicateDeclarationError(node.name)

        self.symbol_table.enter_scope()
        block_idx = self.symbol_table.display[self.symbol_table.level]

        proc_idx = self.symbol_table.tx + 1
        self.symbol_table.enter(
            name=node.name,
            obj_kind=ObjectKind.PROCEDURE,
            type=VOID_TYPE,
            level=self.symbol_table.level - 1,
            ref=block_idx
        )

        entry = self.symbol_table.get_entry(proc_idx)
        entry.level = self.symbol_table.level - 1

        for param in node.parameters:
            self.visit(param)

        self.visit(node.block)
        self.symbol_table.exit_scope()

        return node

    def visit_function_declaration(self, node: FunctionDeclaration) -> Any:
        if self.symbol_table.lookup_current_scope(node.name) is not None:
            raise DuplicateDeclarationError(node.name)

        return_type = self.visit(node.return_type)

        self.symbol_table.enter_scope()
        block_idx = self.symbol_table.display[self.symbol_table.level]

        func_idx = self.symbol_table.tx + 1
        self.symbol_table.enter(
            name=node.name,
            obj_kind=ObjectKind.FUNCTION,
            type=return_type,
            level=self.symbol_table.level - 1,
            ref=block_idx
        )

        entry = self.symbol_table.get_entry(func_idx)
        entry.level = self.symbol_table.level - 1

        old_function_type = self.current_function_type
        self.current_function_type = return_type

        for param in node.parameters:
            self.visit(param)

        self.visit(node.block)
        self.symbol_table.exit_scope()

        self.current_function_type = old_function_type

        return node

    def visit_parameter(self, node: Parameter) -> Any:
        param_type = self.visit(node.type_spec)

        for identifier in node.identifiers:
            if self.symbol_table.lookup_current_scope(identifier) is not None:
                raise DuplicateDeclarationError(identifier)

            self.symbol_table.enter(
                name=identifier,
                obj_kind=ObjectKind.VARIABLE,
                type=param_type,
                normal=True
            )

        return node

    def visit_simple_type(self, node: SimpleType) -> Type:
        type_name = node.name.lower()
        if type_name in self.type_map:
            return self.type_map[type_name]

        idx = self.symbol_table.lookup(node.name)
        if idx is not None:
            entry = self.symbol_table.get_entry(idx)
            if entry.obj_kind == ObjectKind.TYPE:
                return entry.type

        raise UndeclaredIdentifierError(node.name)

    def visit_array_type(self, node: ArrayType) -> Type:
        element_type = self.visit(node.element_type)

        if isinstance(node.index_type, tuple):
            start, end = node.index_type
            low = start if isinstance(
                start, int) else self._evaluate_const_expr(start)
            high = end if isinstance(
                end, int) else self._evaluate_const_expr(end)
            index_type = INTEGER_TYPE
        else:
            index_type = self.visit(node.index_type)
            low = 0
            high = 0

        element_size = self._get_type_size(element_type)
        arr_idx = self.symbol_table.enter_array(
            index_type=index_type,
            element_type=element_type,
            low=low,
            high=high,
            element_size=element_size
        )

        array_type = Type(SimpleTypeKind.INTEGER)
        array_type.array_info = ArrayTypeInfo(
            index_type=index_type,
            element_type=element_type,
            low=low,
            high=high,
            element_size=element_size,
            size=(high - low + 1) * element_size
        )
        array_type.array_info.ref_index = arr_idx

        return array_type

    def visit_record_type(self, node: RecordType) -> Type:
        fields = {}
        offset = 0

        for field_decl in node.fields:
            field_type = self.visit(field_decl.type_spec)
            field_size = self._get_type_size(field_type)

            for field_name in field_decl.identifiers:
                if field_name in fields:
                    raise DuplicateDeclarationError(field_name)
                fields[field_name] = (field_type, offset)
                offset += field_size

        record_type = Type(SimpleTypeKind.INTEGER)
        record_type.record_info = RecordTypeInfo(fields=fields, size=offset)

        return record_type

    def visit_compound_statement(self, node: CompoundStatement) -> Any:
        for stmt in node.statements:
            self.visit(stmt)
        return node

    def visit_assignment_statement(self, node: AssignmentStatement) -> Any:
        var_type = self.visit(node.variable)
        expr_type = self.visit(node.expression)

        if not var_type.compatible_with(expr_type):
            raise TypeMismatchError(
                str(var_type), str(expr_type), "assignment")

        return node

    def visit_if_statement(self, node: IfStatement) -> Any:
        cond_type = self.visit(node.condition)
        if cond_type != BOOLEAN_TYPE:
            raise TypeMismatchError("boolean", str(cond_type), "if condition")

        self.visit(node.then_statement)
        if node.else_statement:
            self.visit(node.else_statement)

        return node

    def visit_while_statement(self, node: WhileStatement) -> Any:
        cond_type = self.visit(node.condition)
        if cond_type != BOOLEAN_TYPE:
            raise TypeMismatchError(
                "boolean", str(cond_type), "while condition")

        self.visit(node.body)
        return node

    def visit_for_statement(self, node: ForStatement) -> Any:
        start_type = self.visit(node.start_expr)
        end_type = self.visit(node.end_expr)

        if not start_type.is_ordinal():
            raise TypeMismatchError(
                "ordinal type", str(start_type), "for start")
        if not end_type.is_ordinal():
            raise TypeMismatchError("ordinal type", str(end_type), "for end")

        if self.symbol_table.lookup_current_scope(node.variable) is None:
            self.symbol_table.enter(
                name=node.variable,
                obj_kind=ObjectKind.VARIABLE,
                type=INTEGER_TYPE
            )

        self.visit(node.body)
        return node

    def visit_repeat_statement(self, node: RepeatStatement) -> Any:
        for stmt in node.statements:
            self.visit(stmt)

        cond_type = self.visit(node.condition)
        if cond_type != BOOLEAN_TYPE:
            raise TypeMismatchError("boolean", str(
                cond_type), "repeat condition")

        return node

    def visit_case_statement(self, node: CaseStatement) -> Any:
        _ = self.visit(node.expression)

        for constants, stmt in node.cases:
            self.visit(stmt)

        return node

    def visit_procedure_call(self, node: ProcedureCall) -> Any:
        idx = self.symbol_table.lookup(node.name)
        if idx is None:
            raise UndeclaredIdentifierError(node.name)

        entry = self.symbol_table.get_entry(idx)
        if entry.obj_kind != ObjectKind.PROCEDURE:
            raise InvalidFunctionCallError(f"'{node.name}' is not a procedure")

        for arg in node.arguments:
            self.visit(arg)

        return node

    def visit_empty_statement(self, node: EmptyStatement) -> Any:
        return node

    def visit_binary_op(self, node: BinaryOp) -> Type:
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        op = node.operator

        result_type = None
        if op in ['+', '-', '*', '/']:
            if not left_type.is_numeric() or not right_type.is_numeric():
                raise InvalidOperationError(
                    op, f"{left_type} and {right_type}")
            if left_type == REAL_TYPE or right_type == REAL_TYPE:
                result_type = REAL_TYPE
            else:
                result_type = INTEGER_TYPE

        elif op in ['div', 'mod', 'bagi']:
            if left_type != INTEGER_TYPE or right_type != INTEGER_TYPE:
                raise InvalidOperationError(
                    op, f"{left_type} and {right_type}")
            result_type = INTEGER_TYPE

        elif op in ['and', 'or', 'dan', 'atau']:
            if left_type != BOOLEAN_TYPE or right_type != BOOLEAN_TYPE:
                raise InvalidOperationError(
                    op, f"{left_type} and {right_type}")
            result_type = BOOLEAN_TYPE

        elif op in ['=', '<>', '<', '<=', '>', '>=']:
            if not left_type.compatible_with(right_type):
                raise TypeMismatchError(str(left_type), str(
                    right_type), f"comparison {op}")
            result_type = BOOLEAN_TYPE
        else:
            raise InvalidOperationError(op, "unknown")

        node.sym_type = result_type
        return result_type

    def visit_unary_op(self, node: UnaryOp) -> Type:
        operand_type = self.visit(node.operand)

        if node.operator in ['+', '-']:
            if not operand_type.is_numeric():
                raise InvalidOperationError(node.operator, str(operand_type))
            return operand_type

        elif node.operator == 'not':
            if operand_type != BOOLEAN_TYPE:
                raise InvalidOperationError(node.operator, str(operand_type))
            return BOOLEAN_TYPE

        raise InvalidOperationError(node.operator, "unknown")

    def visit_variable(self, node: Variable) -> Type:
        def resolve_access(var_node: Variable, current_type: Type, base_name: str) -> Type:
            # Handle array indices (may be multidimensional)
            if var_node.indices:
                for index_expr in var_node.indices:
                    if not current_type.is_array():
                        raise InvalidArrayIndexError(f"'{base_name}' is not an array")

                    index_type = self.visit(index_expr)
                    if not index_type.is_ordinal():
                        raise InvalidArrayIndexError("index must be ordinal type")

                    current_type = current_type.array_info.element_type

            # Handle record field access
            if var_node.field:
                if not current_type.is_record():
                    raise InvalidRecordAccessError(base_name, var_node.field)

                if var_node.field not in current_type.record_info.fields:
                    raise InvalidRecordAccessError(base_name, var_node.field)

                current_type = current_type.record_info.fields[var_node.field][0]

            var_node.sym_type = current_type
            return current_type

        # Resolve the root variable (must have a name)
        idx = self.symbol_table.lookup(node.name)
        if idx is None:
            raise UndeclaredIdentifierError(node.name)

        entry = self.symbol_table.get_entry(idx)
        var_type = entry.type
        base_name = node.name

        node.tab_index = idx
        node.sym_type = var_type
        node.sym_level = entry.level

        # Walk through chained accesses
        current_node = node
        current_type = var_type
        while current_node:
            current_type = resolve_access(current_node, current_type, base_name)
            current_node = current_node.next_access

        return current_type

    def visit_number(self, node: Number) -> Type:
        typ = INTEGER_TYPE if isinstance(node.value, int) else REAL_TYPE
        node.sym_type = typ
        return typ

    def visit_string(self, node: String) -> Type:
        node.sym_type = STRING_TYPE
        return STRING_TYPE

    def visit_char(self, node: Char) -> Type:
        node.sym_type = CHAR_TYPE
        return CHAR_TYPE

    def visit_boolean(self, node: Boolean) -> Type:
        node.sym_type = BOOLEAN_TYPE
        return BOOLEAN_TYPE

    def visit_function_call(self, node: FunctionCall) -> Type:
        idx = self.symbol_table.lookup(node.name)
        if idx is None:
            raise UndeclaredIdentifierError(node.name)

        entry = self.symbol_table.get_entry(idx)
        if entry.obj_kind != ObjectKind.FUNCTION:
            raise InvalidFunctionCallError(f"'{node.name}' is not a function")

        for arg in node.arguments:
            self.visit(arg)

        return entry.type

    def visit(self, node: ASTNode) -> Any:
        if node is None:
            return None
        return node.accept(self)
    
    def __ror__(self, value):
        return self.visit(value)

    def _infer_const_type(self, value: Any) -> Type:
        if isinstance(value, bool):
            return BOOLEAN_TYPE
        elif isinstance(value, int):
            return INTEGER_TYPE
        elif isinstance(value, float):
            return REAL_TYPE
        elif isinstance(value, str):
            if len(value) == 1:
                return CHAR_TYPE
            return STRING_TYPE
        return INTEGER_TYPE

    def _get_type_size(self, type: Type) -> int:
        if type.is_array():
            return type.array_info.size
        if type.is_record():
            return type.record_info.size
        return 1

    def _evaluate_const_expr(self, expr: Any) -> int:
        if isinstance(expr, int):
            return expr
        if hasattr(expr, 'value') and isinstance(expr.value, int):
            return expr.value
        return 0

    def _init_builtins(self):
        # Register all reserved words and standard library functions
        for name, kind, typ in RESERVED_WORDS + STANDARD_LIBRARY:
            self.symbol_table.enter(
                name=name,
                obj_kind=kind,
                type=typ,
                level=0
            )
