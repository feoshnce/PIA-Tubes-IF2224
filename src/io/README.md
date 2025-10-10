# IO Module Usage

### Reader
```python
from src.io.reader import Reader

reader = Reader.from_file("program.pas")

while not reader.eof():
    print(reader.current_char)
    reader.advance()
````

### Writer (to console)

```python
from src.io.writer import Writer

writer = Writer()
writer.write_tokens([("IDENTIFIER", "x"), ("NUMBER", "10")])
```

### Writer (to txt file)

```python
from src.io.writer import Writer

with open("output.txt", "w", encoding="utf-8") as f:
    writer = Writer(stream=f)
    writer.write_tokens([("IDENTIFIER", "x"), ("NUMBER", "10")])
```
