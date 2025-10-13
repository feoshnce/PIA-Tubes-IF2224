from __future__ import annotations
import json
from src.automaton import DFA, DFAConfig



class Lexer:
    def __init__(self, dfa_config_path: str = "config/dfa_rules.json"):
        """Init lexer"""
        self.config = self._load_config(dfa_config_path)
        self.dfa = DFA(self.config)
        self.keywords = set(self.config.keywords)
        self.reserved_map = self.config.reserved_map
    
    def _load_config(self, path: str) -> DFAConfig:
        """Load DFAConfig"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"File konfigurasi DFA tidak ditemukan di '{path}'")
        
        return DFAConfig(
            start_state=data['start_state'],
            final_states=data['final_states'],
            char_classes=data['char_classes'],
            transitions=[tuple(t) for t in data['transitions']],
            keywords=data['keywords'],
            reserved_map=data['reserved_map']
        )