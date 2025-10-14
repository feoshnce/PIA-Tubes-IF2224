# ParsingIsAllYouNeed

## Usage
```bash
uv sync

uv run src/main.py test/milestone-1/input/1.pas
```

Output example:
```bash
KEYWORD(program)
IDENTIFIER(Hello)
SEMICOLON(;)
```

### Check Mode
Compare lexer output with expected output:
```bash
uv run src/main.py test/milestone-1/input/1.pas --check
```

Output when passing:
```bash
[PASS] Output matches expected!
```

Output when failing:
```bash
[FAIL] Output differs from expected:

Expected:
----------------------------------------
KEYWORD(program)
IDENTIFIER(Test)
...

Actual:
----------------------------------------
KEYWORD(program)
IDENTIFIER(Hello)
...

Differences:
----------------------------------------
Line 2:
  Expected: IDENTIFIER(Test)
  Actual:   IDENTIFIER(Hello)
```

### Save Output to File
Save lexer output to a file:

**Auto-save to milestone output directory:**
```bash
# Automatically saves to test/milestone-1/output/1.txt
uv run python src/main.py test/milestone-1/input/1.pas --output
```

**Save to custom path:**
```bash
# Save to specific file
uv run python src/main.py test/milestone-1/input/1.pas --output my_output.txt
```

**Combine with check mode:**
```bash
# Check against expected output AND save to file
uv run python src/main.py test/milestone-1/input/1.pas --check --output
```