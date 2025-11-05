"""
Parser module for Pascal-S.

This module provides syntax analysis functionality using Recursive Descent parsing.
"""

from .parser import Parser
from .tree_formatter import format_parse_tree, TreeFormatter

__all__ = ["Parser", "format_parse_tree", "TreeFormatter"]
