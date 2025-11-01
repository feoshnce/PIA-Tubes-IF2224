"""
Base classes for Abstract Syntax Tree (AST) nodes.
"""

from abc import ABC, abstractmethod
from typing import Any


class ASTNode(ABC):
    """
    Abstract base class for all AST nodes.
    """

    @abstractmethod
    def accept(self, visitor: Any) -> Any:
        """
        Accept a visitor for traversal.

        Args:
            visitor: The visitor object that will process this node

        Returns:
            The result of the visitor's operation
        """
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """
        Convert the AST node to a dictionary representation.

        Returns:
            Dictionary representation of the node
        """
        pass
