from __future__ import annotations
from ..abstract import AutomatonABC
from typing import Dict, Optional, Tuple, List
import re
from dataclasses import dataclass


@dataclass
class DFAConfig:
    start_state: str
    final_states: Dict[str, str]
    char_classes: Dict[str, str]
    transitions: List[Tuple[str, str, str]]
    keywords: List[str]
    reserved_map: Dict[str, str]


class DFA(AutomatonABC[str, str]):
    """DFA lexical analysis."""

    def __init__(self, config: DFAConfig):
        super().__init__()

        self.config = config
        self.set_start(config.start_state)
        for final_state in config.final_states:
            self.add_final(final_state)

        self.current_state: Optional[str] = self.start_state

        self.char_class_patterns: Dict[str, re.Pattern] = {
            name: re.compile(pattern)
            for name, pattern in config.char_classes.items()
        }

        self.transitions: Dict[Tuple[str, str], str] = {
            (from_state, input_sym): to_state
            for from_state, input_sym, to_state in config.transitions
        }

    def reset(self) -> None:
        """Reset automaton to start state."""
        self.current_state = self.start_state

    def step(self, char: str) -> Optional[str]:
        key = (self.current_state, char)
        if key in self.transitions:
            self.current_state = self.transitions[key]
            return self.current_state

        for (state, input_sym), next_state in self.transitions.items():
            if state == self.current_state and input_sym in self.char_class_patterns:
                if self.char_class_patterns[input_sym].match(char):
                    self.current_state = next_state
                    return self.current_state

        return None

    def get_token_type(self) -> Optional[str]:
        return self.config.final_states.get(self.current_state)

    def can_transition(self, char: str) -> bool:
        key = (self.current_state, char)
        if key in self.transitions:
            return True

        return any(
            state == self.current_state
            and input_sym in self.char_class_patterns
            and self.char_class_patterns[input_sym].match(char)
            for state, input_sym in self.transitions.keys()
        )
