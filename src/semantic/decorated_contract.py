from __future__ import annotations

from dataclasses import fields, is_dataclass
from typing import Callable, List, Optional, Set, Tuple
import sys

from parse_tree.base import ASTNode
from parse_tree.expression import (
    BinaryOp, UnaryOp, Variable, Number, String, Char, Boolean, FunctionCall
)
from parse_tree.statement import (
    AssignmentStatement, ProcedureCall
)
from parse_tree.declaration import VarDeclaration
from parse_tree.program import Block  # Block is in parse_tree/program.py in your repo


class DecoratedASTError(ValueError):
    """Raised when semantic decorations violate expected invariants."""


WarnFn = Callable[[str], None]


def _default_warn(msg: str) -> None:
    # IMPORTANT: stderr only (stdout unchanged)
    print(f"[DecoratedAST] {msg}", file=sys.stderr)


def validate_decorated_ast(
    root: ASTNode,
    *,
    warn: Optional[WarnFn] = None,
    strict: bool = False,
    max_nodes: int = 200_000,
) -> None:
    """
    Validate semantic decorations (decorated AST) AFTER semantic analysis.

    Safe-by-design:
    - Does not mutate any AST node
    - Uses stderr for warnings
    - strict=False by default to avoid breaking existing behavior
    """
    warn_fn = warn or _default_warn

    if not isinstance(root, ASTNode):
        _fail_or_warn(strict, warn_fn, f"Root must be ASTNode, got {type(root).__name__}.")
        return

    visited: Set[int] = set()
    stack: List[Tuple[ASTNode, str]] = [(root, root.__class__.__name__)]
    count = 0

    while stack:
        node, path = stack.pop()
        node_id = id(node)
        if node_id in visited:
            _fail_or_warn(strict, warn_fn, f"Cycle detected at {path} ({node.__class__.__name__}).")
            continue
        visited.add(node_id)

        count += 1
        if count > max_nodes:
            _fail_or_warn(strict, warn_fn, f"AST too large (> {max_nodes}). Possible cycle.")
            return

        # Traverse children via dataclass fields
        if is_dataclass(node):
            for f in fields(node):
                val = getattr(node, f.name)

                if isinstance(val, ASTNode):
                    stack.append((val, f"{path}.{f.name}"))
                elif isinstance(val, list):
                    for i, item in enumerate(val):
                        if isinstance(item, ASTNode):
                            stack.append((item, f"{path}.{f.name}[{i}]"))

        # --- Decoration sanity checks ---
        _check_decorations(node, path, strict, warn_fn)


def _check_decorations(node: ASTNode, path: str, strict: bool, warn_fn: WarnFn) -> None:
    """
    Conservative checks that match CURRENT behavior of SemanticVisitor.

    We only require decorations that are ACTUALLY set in your semantic/visitor.py,
    so this checker won't falsely fail.
    """

    # 1) Nodes that your semantic visitor definitely sets sym_type for:
    must_have_sym_type = (
        Variable, Number, String, Char, Boolean,
        BinaryOp,
        AssignmentStatement,
        ProcedureCall,
        VarDeclaration,
    )
    if isinstance(node, must_have_sym_type):
        if getattr(node, "sym_type", None) is None:
            _fail_or_warn(strict, warn_fn, f"{path}: expected sym_type to be set after semantic pass.")

    # 2) Nodes that your semantic visitor definitely sets tab_index for:
    must_have_tab_index = (Variable, ProcedureCall, VarDeclaration)
    if isinstance(node, must_have_tab_index):
        if getattr(node, "tab_index", None) is None:
            _fail_or_warn(strict, warn_fn, f"{path}: expected tab_index to be set after semantic pass.")

    # 3) Blocks: semantic visitor sets block_index + sym_level
    if isinstance(node, Block):
        if getattr(node, "sym_level", None) is None:
            _fail_or_warn(strict, warn_fn, f"{path}: expected sym_level to be set for Block.")
        if not hasattr(node, "block_index"):
            _fail_or_warn(strict, warn_fn, f"{path}: expected Block to have attribute block_index.")
        else:
            if getattr(node, "block_index") is None:
                _fail_or_warn(strict, warn_fn, f"{path}: expected block_index to be set for Block.")

    # 4) Type checks (non-fatal unless strict)
    if hasattr(node, "sym_level") and getattr(node, "sym_level") is not None:
        if not isinstance(getattr(node, "sym_level"), int):
            _fail_or_warn(strict, warn_fn, f"{path}.sym_level should be int or None.")

    # 5) Nice-to-have decorations (WARN only; do NOT fail by default)
    # Your current visitor does NOT set sym_type for UnaryOp and FunctionCall.
    if isinstance(node, (UnaryOp, FunctionCall)):
        if getattr(node, "sym_type", None) is None:
            warn_fn(
                f"{path}: sym_type is not set (note: current semantic visitor may not decorate this node)."
            )


def _fail_or_warn(strict: bool, warn_fn: WarnFn, message: str) -> None:
    if strict:
        raise DecoratedASTError(message)
    warn_fn("WARNING: " + message)
