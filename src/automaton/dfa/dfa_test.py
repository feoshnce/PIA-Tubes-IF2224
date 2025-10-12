from typing import Dict, List, Tuple
from .dfa import DFA, DFAConfig
import json

with open('config/dfa_rules.json', 'r') as file:
    rules = json.load(file)
print("test1") 

# Buat DFAConfig
config = DFAConfig(
    start_state=rules["start_state"],
    final_states=rules["final_states"],
    char_classes=rules["char_classes"],
    transitions=rules["transitions"],
    keywords=rules["keywords"],
    reserved_map=rules["reserved_map"]
)
print("test2")  

dfa = DFA(config)
print("test3")

def test_input(input_str: str, expect: str = None):
    print(f"input:{input_str}")
    chars = list(input_str)
    result = dfa.accepts(chars)
    print(f"result:{result}")
    if result:
        token = dfa.get_token_type()
        print(f"token:{token}")
        if expect:
            print(f"expect:{expect}")
            print(f"match:{token == expect}")
    else:
        print("rejected:True")
    dfa.reset()

print("test4")
test_input("program", "IDENTIFIER") #salah karena cuman dfa
test_input("x1", "IDENTIFIER")
test_input("div", "ARITHMETIC_OPERATOR") #salah karena cuman dfa

print("test5")
test_input("123", "NUMBER")
test_input("12.34", "NUMBER")

print("test6")
test_input(" ", "WHITESPACE")
test_input("\t", "WHITESPACE")

print("test7")
test_input(";", "SEMICOLON")
test_input(":=", "ASSIGN_OPERATOR")
test_input("+", "ARITHMETIC_OPERATOR")
test_input("<=", "RELATIONAL_OPERATOR")
test_input("..", "RANGE_OPERATOR")

print("test8")
test_input("'hello'", "STRING_LITERAL")
test_input("'a'", "STRING_LITERAL")

print("test9")
test_input("{this is a comment}", "COMMENT")
test_input("(*another comment*)", "COMMENT")

print("test10")
test_input("@", None)
test_input("12.", None)
test_input("'unclosed", None)

print("test11")
dfa.reset()
for char in "if":
    next_state = dfa.step(char)
    print(f"state:{next_state}")
print(f"token:{dfa.get_token_type()}")

print("test12")
dfa.reset()
print(f"can_move_a:{dfa.can_transition('a')}")
print(f"can_move_at:{dfa.can_transition('@')}")