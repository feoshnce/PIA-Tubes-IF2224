# src/parse_tree/contract.py
from __future__ import annotations

from dataclasses import MISSING, fields, is_dataclass
from typing import Any, Callable, List, Optional, Set, Tuple
import sys

from .base import ASTNode
from .expression import Variable  # for extra invariants


class ASTContractError(ValueError):
    """Raised when AST violates structural contract assumptions."""


WarnFn = Callable[[str], None]


def _default_warn(msg: str) -> None:
    # IMPORTANT: stderr only so stdout outputs/tests remain identical.
    print(f"[ASTContract] {msg}", file=sys.stderr)


def validate_ast_contract(
    root: ASTNode,
    *,
    warn: Optional[WarnFn] = None,
    strict: bool = True,
    max_nodes: int = 200_000,
) -> None:
    """
    Validate AST structural consistency (parser ↔ semantic analyzer contract)
    WITHOUT modifying any node and WITHOUT changing program output.

    - strict=True: raise ASTContractError on violations
    - strict=False: emit warnings (stderr) and continue
    """
    warn_fn = warn or _default_warn

    if not isinstance(root, ASTNode):
        _fail_or_warn(
            strict,
            warn_fn,
            f"Root must be an ASTNode, got {type(root).__name__}.",
        )
        return

    visited: Set[int] = set()
    stack: List[Tuple[ASTNode, str]] = [(root, root.__class__.__name__)]
    node_count = 0

    while stack:
        node, path = stack.pop()
        node_id = id(node)
        if node_id in visited:
            # Cycle detected. AST should be a DAG/tree; cycle indicates a bug.
            _fail_or_warn(strict, warn_fn, f"Cycle detected at {path} ({node.__class__.__name__}).")
            continue
        visited.add(node_id)

        node_count += 1
        if node_count > max_nodes:
            _fail_or_warn(
                strict,
                warn_fn,
                f"AST too large (> {max_nodes} nodes). Possible cycle or runaway structure.",
            )
            return

        # Basic ASTNode sanity (these are in ASTNode.__init__)
        # They can be None; do not enforce values (to avoid logic changes),
        # but we can warn if they are unexpected types.
        if hasattr(node, "tab_index") and node.tab_index is not None and not isinstance(node.tab_index, int):
            _fail_or_warn(strict, warn_fn, f"{path}.tab_index must be int or None, got {type(node.tab_index).__name__}.")
        # sym_type is Any: we don't validate its concrete type here.

        # Dataclass field checks
        if is_dataclass(node):
            for f in fields(node):
                value = getattr(node, f.name)

                required = (f.default is MISSING and f.default_factory is MISSING)

                # Required fields should not be None
                if required and value is None:
                    _fail_or_warn(
                        strict,
                        warn_fn,
                        f"Missing required field: {path}.{f.name} is None.",
                    )
                    continue

                # No None inside lists/tuples (common AST bug)
                if isinstance(value, (list, tuple)):
                    for i, item in enumerate(value):
                        if item is None:
                            _fail_or_warn(
                                strict,
                                warn_fn,
                                f"{path}.{f.name}[{i}] is None (lists should not contain None).",
                            )
                        # Child AST nodes: push for recursion
                        if isinstance(item, ASTNode):
                            stack.append((item, f"{path}.{f.name}[{i}]"))
                else:
                    # Single child AST node
                    if isinstance(value, ASTNode):
                        stack.append((value, f"{path}.{f.name}"))

                # Lightweight string sanity for common identifier-like fields
                if isinstance(value, str) and f.name in {
                    "name", "variable", "operator", "direction", "field"
                }:
                    if value.strip() == "":
                        _fail_or_warn(strict, warn_fn, f"{path}.{f.name} is an empty string.")

        # Class-specific invariants (WARNING/ERROR only; no mutation)
        _check_node_specific_invariants(node, path, strict, warn_fn)


def _check_node_specific_invariants(node: ASTNode, path: str, strict: bool, warn_fn: WarnFn) -> None:
    """
    Add only invariants that are universally true for your AST design,
    and won't change program semantics. Keep conservative.
    """
    # Variable: indices/field/next_access consistency
    if isinstance(node, Variable):
        if not isinstance(node.name, str) or node.name.strip() == "":
            _fail_or_warn(strict, warn_fn, f"{path}.name must be a non-empty string.")

        if node.indices is not None:
            if not isinstance(node.indices, list):
                _fail_or_warn(strict, warn_fn, f"{path}.indices must be a list[Expression] or None.")
            else:
                for i, idx in enumerate(node.indices):
                    if not isinstance(idx, ASTNode):
                        _fail_or_warn(strict, warn_fn, f"{path}.indices[{i}] must be an ASTNode(Expression).")

        if node.field is not None and (not isinstance(node.field, str) or node.field.strip() == ""):
            _fail_or_warn(strict, warn_fn, f"{path}.field must be a non-empty string when present.")

        if node.next_access is not None and not isinstance(node.next_access, Variable):
            _fail_or_warn(strict, warn_fn, f"{path}.next_access must be Variable or None.")

        # Optional: warn if both indices and field exist at same link (can happen, but usually indicates bug)
        if node.indices is not None and node.field is not None:
            warn_fn(
                f"{path}: Variable has both indices and field set on the same access link. "
                f"This is allowed in some designs but often indicates an AST construction bug."
            )

    # Many nodes store operator/direction as strings; basic safe checks:
    # (do NOT enforce full sets, because that could reject valid extensions.)
    if hasattr(node, "direction"):
        direction = getattr(node, "direction")
        if direction is not None and isinstance(direction, str):
            if direction.lower() not in {"to", "downto"}:
                # warning only (do not fail): future extensions may add variants
                warn_fn(f"{path}.direction is {direction!r}; expected 'to' or 'downto'.")

    if hasattr(node, "operator"):
        op = getattr(node, "operator")
        if op is not None and isinstance(op, str) and op.strip() == "":
            _fail_or_warn(strict, warn_fn, f"{path}.operator is empty string.")


def _fail_or_warn(strict: bool, warn_fn: WarnFn, message: str) -> None:
    if strict:
        raise ASTContractError(message)
    warn_fn("WARNING: " + message)
