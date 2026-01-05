from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Iterable, List, Optional, Set, Tuple
import re
import sys

from .dfa import DFAConfig


class DFAConfigError(ValueError):
    """Raised when DFA configuration is invalid in a way that would break execution."""


WarnFn = Callable[[str], None]


def _default_warn(msg: str) -> None:
    # IMPORTANT: stderr only, so stdout-based tests/output stay unchanged.
    print(f"[DFAConfigValidator] {msg}", file=sys.stderr)


@dataclass(frozen=True)
class ValidationReport:
    states: Set[str]
    reachable_states: Set[str]
    dead_states: Set[str]
    unreachable_states: Set[str]
    char_class_overlaps: List[str]  # human-readable lines


def validate_dfa_config(
    config: DFAConfig,
    *,
    warn: Optional[WarnFn] = None,
    strict: bool = True,
    check_overlap_ascii_range: Tuple[int, int] = (0, 127),
) -> ValidationReport:
    """
    Validate DFAConfig without changing DFA logic.

    - strict=True will raise DFAConfigError for critical issues
    - Warnings are emitted via `warn` (stderr by default)
    - Overlap detection is WARNING-only (does not reorder or fix anything)
    """
    warn_fn = warn or _default_warn

    # --- Basic shape checks ---
    if not isinstance(config.start_state, str) or not config.start_state:
        raise DFAConfigError("start_state must be a non-empty string.")

    if not isinstance(config.final_states, dict) or not config.final_states:
        raise DFAConfigError("final_states must be a non-empty dict mapping state -> token_type string.")

    if not isinstance(config.char_classes, dict):
        raise DFAConfigError("char_classes must be a dict mapping class_name -> regex pattern string.")

    if not isinstance(config.transitions, list) or not config.transitions:
        raise DFAConfigError("transitions must be a non-empty list of (from_state, input_sym, to_state).")

    # Ensure transitions are triples of strings
    normalized_transitions: List[Tuple[str, str, str]] = []
    for i, t in enumerate(config.transitions):
        if not (isinstance(t, tuple) or isinstance(t, list)) or len(t) != 3:
            raise DFAConfigError(f"Transition at index {i} must be a triple: (from_state, input_sym, to_state). Got: {t!r}")
        a, b, c = t
        if not all(isinstance(x, str) and x for x in (a, b, c)):
            raise DFAConfigError(f"Transition at index {i} must contain non-empty strings. Got: {t!r}")
        normalized_transitions.append((a, b, c))

    # --- Infer all states ---
    states = _infer_states(
        start_state=config.start_state,
        final_states=set(config.final_states.keys()),
        transitions=normalized_transitions,
    )

    # --- Critical state existence checks ---
    if config.start_state not in states:
        # This is basically impossible given our inference, but keep it.
        raise DFAConfigError(f"start_state '{config.start_state}' is not included in inferred states.")

    for fs in config.final_states.keys():
        if fs not in states:
            raise DFAConfigError(f"final_state '{fs}' is not included in inferred states.")

    # --- Compile regex patterns (critical) ---
    compiled_classes: Dict[str, re.Pattern] = {}
    for name, pattern in config.char_classes.items():
        if not isinstance(name, str) or not name:
            raise DFAConfigError("char_classes contains an invalid (empty) class name.")
        if not isinstance(pattern, str):
            raise DFAConfigError(f"char_classes['{name}'] pattern must be a string.")
        try:
            compiled_classes[name] = re.compile(pattern)
        except re.error as e:
            raise DFAConfigError(f"Invalid regex for char class '{name}': {pattern!r}. Regex error: {e}") from e

    # --- Validate transitions reference valid states ---
    for i, (from_state, input_sym, to_state) in enumerate(normalized_transitions):
        if from_state not in states:
            raise DFAConfigError(f"Transition {i} references unknown from_state '{from_state}'.")
        if to_state not in states:
            raise DFAConfigError(f"Transition {i} references unknown to_state '{to_state}'.")

        # input_sym can be:
        # - a literal char like "{" or "."
        # - a char class name like "LETTER"
        if input_sym in compiled_classes:
            pass
        else:
            # literal sanity checks: don't fail (to avoid logic changes), just warn
            if len(input_sym) != 1:
                warn_fn(
                    f"Transition {i} uses literal input_sym {input_sym!r} with length != 1 "
                    f"(this is allowed but unusual)."
                )

    # --- Reachability checks (warning-only) ---
    reachable = _reachable_states(config.start_state, normalized_transitions, compiled_classes)
    unreachable = states - reachable
    if unreachable:
        warn_fn(f"Unreachable states detected: {sorted(unreachable)}")

    # --- Dead state checks (warning-only) ---
    dead = _dead_states(states, set(config.final_states.keys()), normalized_transitions)
    if dead:
        warn_fn(f"Dead states (cannot reach any final state) detected: {sorted(dead)}")

    # --- Char class overlap detection (warning-only) ---
    overlaps = _detect_char_class_overlaps(
        compiled_classes,
        ascii_range=check_overlap_ascii_range,
    )
    for line in overlaps:
        warn_fn(line)

    return ValidationReport(
        states=states,
        reachable_states=reachable,
        dead_states=dead,
        unreachable_states=unreachable,
        char_class_overlaps=overlaps,
    )


def _infer_states(
    *,
    start_state: str,
    final_states: Set[str],
    transitions: List[Tuple[str, str, str]],
) -> Set[str]:
    states: Set[str] = {start_state}
    states |= set(final_states)
    for a, _sym, c in transitions:
        states.add(a)
        states.add(c)
    return states


def _reachable_states(
    start_state: str,
    transitions: List[Tuple[str, str, str]],
    _compiled_classes: Dict[str, re.Pattern],
) -> Set[str]:
    """
    Reachability is purely graph-based over states.
    (Input symbols / char classes do not affect reachability.)"""
    graph: Dict[str, Set[str]] = {}
    for a, _sym, c in transitions:
        graph.setdefault(a, set()).add(c)

    seen: Set[str] = set()
    stack: List[str] = [start_state]
    while stack:
        s = stack.pop()
        if s in seen:
            continue
        seen.add(s)
        for nxt in graph.get(s, set()):
            if nxt not in seen:
                stack.append(nxt)
    return seen


def _dead_states(
    states: Set[str],
    final_states: Set[str],
    transitions: List[Tuple[str, str, str]],
) -> Set[str]:
    """
    A 'dead' state here means: cannot reach ANY final state in the state graph.
    Warning-only, because it might be intentional (e.g., sink states).
    """
    reverse_graph: Dict[str, Set[str]] = {}
    for a, _sym, c in transitions:
        reverse_graph.setdefault(c, set()).add(a)

    can_reach_final: Set[str] = set()
    stack: List[str] = list(final_states)
    while stack:
        s = stack.pop()
        if s in can_reach_final:
            continue
        can_reach_final.add(s)
        for prev in reverse_graph.get(s, set()):
            if prev not in can_reach_final:
                stack.append(prev)

    # states that are not in can_reach_final are dead
    return set(states) - can_reach_final


def _detect_char_class_overlaps(
    compiled_classes: Dict[str, re.Pattern],
    *,
    ascii_range: Tuple[int, int] = (0, 127),
) -> List[str]:
    """
    WARNING-only: detects overlaps among char class regexes by sampling ASCII.

    This does NOT change ordering or fix anything (so DFA logic remains unchanged).
    """
    if not compiled_classes:
        return []

    lo, hi = ascii_range
    hi = max(hi, lo)

    class_names = sorted(compiled_classes.keys())
    overlaps: Dict[Tuple[str, str], List[str]] = {}

    for code in range(lo, hi + 1):
        ch = chr(code)
        matched = [name for name in class_names if compiled_classes[name].match(ch)]
        if len(matched) > 1:
            # record pairwise overlaps for better readability
            for i in range(len(matched)):
                for j in range(i + 1, len(matched)):
                    a, b = matched[i], matched[j]
                    key = (a, b) if a < b else (b, a)
                    overlaps.setdefault(key, []).append(_pretty_char(ch))

    lines: List[str] = []
    for (a, b), chars in sorted(overlaps.items()):
        sample = ", ".join(chars[:10])
        extra = "" if len(chars) <= 10 else f" (+{len(chars) - 10} more)"
        lines.append(
            f"WARNING: char class overlap between '{a}' and '{b}' on: {sample}{extra}"
        )
    return lines


def _pretty_char(ch: str) -> str:
    # printable representation for warnings
    if ch == "\n":
        return r"'\n'"
    if ch == "\r":
        return r"'\r'"
    if ch == "\t":
        return r"'\t'"
    if ch == " ":
        return r"' '"
    if ch == "'":
        return r"'\''"
    if ch.isprintable():
        return f"'{ch}'"
    return f"'\\x{ord(ch):02x}'"
