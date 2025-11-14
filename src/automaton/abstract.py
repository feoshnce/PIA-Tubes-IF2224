from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Hashable, Optional, Set, AbstractSet, Iterable

StateT = TypeVar("StateT", bound=Hashable)
SymbolT = TypeVar("SymbolT", bound=Hashable)


class AutomatonABC(ABC, Generic[StateT, SymbolT]):
    """
    Abstract base class for finite(-ish) automata.
    """

    def __init__(self) -> None:
        self._start: Optional[StateT] = None
        self._finals: Set[StateT] = set()

    # --- configuration ---
    def set_start(self, state: StateT) -> None:
        self._start = state

    def add_final(self, state: StateT) -> None:
        self._finals.add(state)

    def is_final(self, state: StateT) -> bool:
        return state in self._finals

    @property
    def start_state(self) -> Optional[StateT]:
        return self._start

    @property
    def final_states(self) -> AbstractSet[StateT]:
        return frozenset(self._finals)

    # --- runtime ---
    @abstractmethod
    def reset(self) -> None:
        """Reset internal runtime state (if any)."""
        ...
