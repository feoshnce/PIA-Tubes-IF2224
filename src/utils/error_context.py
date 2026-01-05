# src/utils/error_context.py
from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from typing import Optional, Tuple, Any

from text import Position  # your Position(index,line,column) 


@dataclass(frozen=True)
class SourceLocation:
    """Normalized location for printing context."""
    index: int               # 0-based character index in source
    line: int                # 1-based
    column: int              # 1-based
    span: int = 1            # caret span length


def debug_enabled(flag: str = "DEBUG_ERROR_CONTEXT") -> bool:
    """Enable with: DEBUG_ERROR_CONTEXT=1 ..."""
    return os.getenv(flag) == "1"


def index_to_line_col(source: str, index: int) -> Tuple[int, int]:
    """
    Convert 0-based character index into (line, col), both 1-based.
    Mirrors Reader.set_position logic. 
    """
    if index < 0:
        index = 0
    if index > len(source):
        index = len(source)

    line = 1
    col = 1
    for i in range(index):
        if source[i] == "\n":
            line += 1
            col = 1
        else:
            col += 1
    return line, col


def line_bounds(source: str, line: int) -> Tuple[int, int]:
    """
    Return (start_index, end_index_exclusive) for a 1-based line number.
    """
    if line <= 0:
        return (0, 0)
    lines = source.splitlines(keepends=True)
    if line > len(lines):
        # if file ends without newline, splitlines still returns last line
        return (len(source), len(source))

    start = sum(len(lines[i]) for i in range(line - 1))
    end = start + len(lines[line - 1])
    # Strip trailing newline for nicer printing
    if end > start and source[end - 1] == "\n":
        end -= 1
    return start, end


def extract_location_from_exception(source: str, exc: BaseException) -> Optional[SourceLocation]:
    """
    Try to extract a location from your project error types:

    - LexicalError / ErrorBase: exc.position is Position(index,line,column) 
    - SyntaxError: exc.token.start / exc.token.end are indices 
    """
    # 1) Errors with Position
    pos = getattr(exc, "position", None)
    if isinstance(pos, Position):
        span = 1
        return SourceLocation(index=pos.index, line=pos.line, column=pos.column, span=span)

    # 2) SyntaxError-like errors with token.start/end
    token = getattr(exc, "token", None)
    if token is not None:
        start = getattr(token, "start", None)
        end = getattr(token, "end", None)
        if isinstance(start, int):
            if not isinstance(end, int) or end < start:
                end = start + 1
            line, col = index_to_line_col(source, start)
            span = max(1, end - start)
            return SourceLocation(index=start, line=line, column=col, span=span)

    return None


def format_error_context(
    source: str,
    loc: SourceLocation,
    *,
    window: int = 1,
) -> str:
    """
    Build a multiline context string:
      >  12 |   x := y + ;
                 ^^^
    """
    if not source:
        return ""

    lines = source.splitlines()
    total_lines = len(lines)
    if total_lines == 0:
        return ""

    line = max(1, min(loc.line, total_lines))
    start_line = max(1, line - window)
    end_line = min(total_lines, line + window)

    # Width for line numbers
    width = len(str(end_line))

    out = []
    out.append("[ErrorContext] Source context:")

    for ln in range(start_line, end_line + 1):
        prefix = ">" if ln == line else " "
        text = lines[ln - 1]
        out.append(f"{prefix} {ln:>{width}} | {text}")

        if ln == line:
            # caret position is 1-based column
            caret_pos = max(0, loc.column - 1)
            caret = " " * caret_pos + "^" * max(1, loc.span)
            out.append(f"  {' ' * width} | {caret}")

    return "\n".join(out)


def print_error_context(
    source: str,
    loc: SourceLocation,
    *,
    window: int = 1,
) -> None:
    """
    Print context to stderr (never stdout).
    """
    ctx = format_error_context(source, loc, window=window)
    if ctx:
        print(ctx, file=sys.stderr)


def maybe_print_error_context_from_exception(
    source: str,
    exc: BaseException,
    *,
    window: int = 1,
    flag: str = "DEBUG_ERROR_CONTEXT",
) -> None:
    """
    Debug-only printing of error context extracted from exception.
    Safe: stderr-only, no raising, no mutation.
    """
    if not debug_enabled(flag):
        return

    loc = extract_location_from_exception(source, exc)
    if loc is None:
        # If no position info exists (e.g., your SemanticError), do nothing.
        return
    print_error_context(source, loc, window=window)
