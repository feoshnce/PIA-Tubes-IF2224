from __future__ import annotations
import json
from automaton import DFA
from automaton.dfa import DFAConfig
from syntax import Token, TokenType
from text import Reader


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
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Config file not found at '{path}'"
            )

        return DFAConfig(
            start_state=data["start_state"],
            final_states=data["final_states"],
            char_classes=data["char_classes"],
            transitions=[tuple(t) for t in data["transitions"]],
            keywords=data["keywords"],
            reserved_map=data["reserved_map"],
        )

    def tokenize(self, source_code: str) -> list[Token]:
        reader = Reader(source_code)
        tokens = []
        while not reader.eof():
            start_pos = reader.pos.index
            lexeme = ""
            self.dfa.reset()
            last_accepted_state = None
            accepted_lexeme = ""

            while not reader.eof() and self.dfa.can_transition(reader.current_char):
                lexeme += reader.current_char
                self.dfa.step(reader.current_char)
                if self.dfa.get_token_type():
                    last_accepted_state = self.dfa.current_state
                    accepted_lexeme = lexeme
                reader.advance()

            if accepted_lexeme:
                token_type_str = self.config.final_states.get(
                    last_accepted_state)
                token_type = TokenType[token_type_str]

                # Check for keywords
                if token_type == TokenType.IDENTIFIER and accepted_lexeme.lower() in self.keywords:
                    token_type = TokenType.KEYWORD
                elif token_type == TokenType.IDENTIFIER and accepted_lexeme in self.reserved_map:
                    token_type = TokenType[self.reserved_map[accepted_lexeme]]

                tokens.append(
                    Token(
                        type=token_type,
                        value=accepted_lexeme,
                        start=start_pos,
                        end=start_pos + len(accepted_lexeme),
                    )
                )
                # Reset reader to the end of the accepted lexeme
                reader = Reader(source_code)
                for _ in range(start_pos + len(accepted_lexeme)):
                    reader.advance()

            elif not reader.eof():
                # Handle unknown characters
                tokens.append(
                    Token(
                        type=TokenType.UNKNOWN,
                        value=reader.current_char,
                        start=reader.pos.index,
                        end=reader.pos.index + 1,
                    )
                )
                reader.advance()

        return tokens
