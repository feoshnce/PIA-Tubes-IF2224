# ParsingIsAllYouNeed

## Identitas Kelompok
Kelompok : PIA - ParsingIsAllYouNeed
| No | NIM      | Nama Lengkap                  |
| -- | -------- | ----------------------------- |
| 1  | 13523021 | Muhammad Raihan Nazhim Oktana |
| 2  | 13523057 | Faqih Muhammad Syuhada        |
| 3  | 13523097 | Shanice Feodora Tjahjono      |
| 4  | 13523105 | Muhammad Fathur Rizky         |

## Deskripsi Program
Tugas Besar Teori Bahasa Formal dan Otomata (IF2224-24) Milestone 1 ini mengimplementasikan tahap pertama dari proses kompilasi, yaitu analisis leksikal (lexical analysis) pada bahasa pemrograman Pascal-S yang merupakan subset dari bahasa Pascal. Melalui pembangunan lexical analyzer (lexer) berbasis Deterministic Finite Automata (DFA), program mampu membaca kode sumber Pascal-S dan mengubahnya menjadi deretan token yang memiliki arti semantik, seperti keyword, identifier, operator, literal, dan simbol-simbol lainnya. Program ini dibuat dengan menggunakan bahasa Python dan hanya dapat berjalan pada CLI (Command Line Interface).

Melanjutkan dari tahap leksikal, Milestone 2 ini mengimplementasikan fase analisis sintaksis (syntax analysis). Program mengambil deretan token yang dihasilkan oleh lexer (Milestone 1) dan memvalidasinya berdasarkan tata bahasa (grammar) Pascal-S. Dengan menggunakan algoritma Recursive Descent, parser ini bertugas membangun Parse Tree yang merepresentasikan struktur hierarkis dari kode sumber. Implementasi ini juga mencakup mekanisme error checking untuk melaporkan kesalahan sintaksis dan telah disesuaikan untuk menangani token-token keyword dalam Bahasa Indonesia sesuai spesifikasi tugas.

Melanjutkan dari tahap sintaks, Milestone 3 ini mengimplementasikan analisis semantik (semantic analysis) untuk memvalidasi makna program di luar kebenaran sintaksisnya. Menggunakan pendekatan Attributed Grammar dan pola Visitor, program menelusuri Parse Tree untuk membangun Abstract Syntax Tree (AST) serta mengelola Symbol Table yang mencakup informasi identifier, tipe data, dan scope. Fokus utama pada tahap ini adalah melakukan type checking dan scope checking untuk memastikan konsistensi logika program, seperti validitas operasi antar tipe data dan deklarasi variabel. Luaran akhirnya berupa Decorated AST yang telah dianotasi dengan informasi semantik yang diperlukan untuk tahapan kompilasi berikutnya.

## Requirements
- Python Version 3.14.1 or newer
- uv Version 0.9.1 or newer

## How To Install
```bash
git clone https://github.com/fathurwithyou/PIA-Tubes-IF2224.git
```

## How To Use
```bash
uv sync
uv run src/main.py test/milestone-1/input/1.pas
uv run src/parser_main.py test/milestone-2/input/test1.pas
uv run src/semantic_main.py test/milestone-3/input/test1.pas
```

Output example:
```bash
KEYWORD(program)
IDENTIFIER(Hello)
SEMICOLON(;)
```

```bash
<program>
├── <program-header>
│   ├── KEYWORD(program)
│   ├── IDENTIFIER(MinimalTest)
│   └── SEMICOLON(;)
├── <compound-statement>
│   ├── KEYWORD(mulai)
│   └── KEYWORD(selesai)
└── DOT(.)
```

```bash
Decorated AST:
========================================
ProgramNode(name: 'RecordBasic')
└─ Block → block_index:0, lev:0
   ├─ Declarations
   │  ├─ TypeDecl('Person')
   │  │  └─ RecordType
   │  │     ├─ VarDecl('age')
   │  │     └─ VarDecl('height')
   │  └─ VarDecl('p') → tab_index:47, type:record, lev:0
   └─ CompoundStmt
      ├─ Assign → type:void, lev:0
      │  ├─ VarAccess('.age') → tab_index:47, type:integer, lev:0
      │  └─ Number(25) → type:integer
      └─ Assign → type:void, lev:0
         ├─ VarAccess('.height') → tab_index:47, type:real, lev:0
         └─ Number(175.5) → type:real
========================================

================================================================================
SYMBOL TABLE (tab)
================================================================================
Index  Name                 Kind         Type            Level  Addr   Ref    Link
--------------------------------------------------------------------------------
0      salah                CONSTANT     boolean         0      0      0      0
1      benar                CONSTANT     boolean         0      0      0      0
2      integer              TYPE         integer         0      0      0      1
3      real                 TYPE         real            0      0      0      2
4      boolean              TYPE         boolean         0      0      0      3
5      char                 TYPE         char            0      0      0      4
6      string               TYPE         string          0      0      0      5
7      dan                  PROCEDURE    void            0      0      0      6
8      atau                 PROCEDURE    void            0      0      0      7
9      tidak                PROCEDURE    void            0      0      0      8
10     bagi                 PROCEDURE    void            0      0      0      9
11     mod                  PROCEDURE    void            0      0      0      10
12     program              PROCEDURE    void            0      0      0      11
13     variabel             PROCEDURE    void            0      0      0      12
14     konstanta            PROCEDURE    void            0      0      0      13
15     tipe                 PROCEDURE    void            0      0      0      14
16     prosedur             PROCEDURE    void            0      0      0      15
17     fungsi               PROCEDURE    void            0      0      0      16
18     mulai                PROCEDURE    void            0      0      0      17
19     selesai              PROCEDURE    void            0      0      0      18
20     jika                 PROCEDURE    void            0      0      0      19
21     maka                 PROCEDURE    void            0      0      0      20
22     selain-itu           PROCEDURE    void            0      0      0      21
23     selama               PROCEDURE    void            0      0      0      22
24     lakukan              PROCEDURE    void            0      0      0      23
25     untuk                PROCEDURE    void            0      0      0      24
26     ke                   PROCEDURE    void            0      0      0      25
27     turun-ke             PROCEDURE    void            0      0      0      26
28     larik                PROCEDURE    void            0      0      0      27
29     write                PROCEDURE    void            0      0      0      28
30     writeln              PROCEDURE    void            0      0      0      29
31     read                 PROCEDURE    void            0      0      0      30
32     readln               PROCEDURE    void            0      0      0      31
33     abs                  FUNCTION     integer         0      0      0      32
34     sqr                  FUNCTION     integer         0      0      0      33
35     sqrt                 FUNCTION     real            0      0      0      34
36     sin                  FUNCTION     real            0      0      0      35
37     cos                  FUNCTION     real            0      0      0      36
38     exp                  FUNCTION     real            0      0      0      37
39     ln                   FUNCTION     real            0      0      0      38
40     odd                  FUNCTION     boolean         0      0      0      39
41     ord                  FUNCTION     integer         0      0      0      40
42     chr                  FUNCTION     char            0      0      0      41
43     succ                 FUNCTION     integer         0      0      0      42
44     pred                 FUNCTION     integer         0      0      0      43
45     RecordBasic          PROGRAM      void            0      0      0      44
46     Person               TYPE         record          0      0      0      45
47     p                    VARIABLE     record          0      0      0      0

================================================================================
BLOCK TABLE (btab)
================================================================================
Index  Last     LPar     PSize    VSize
--------------------------------------------------------------------------------
0      47       0        0        1
```

### Check Mode
Compare lexer / parser output with expected output:
```bash
uv run src/main.py test/milestone-1/input/1.pas --check
uv run src/parser_main.py test/milestone-2/input/test1.pas --check
uv run src/semantic_main.py test/milestone-3/input/test1.pas --decorated
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
# Automatically saves to test/milestone-2/output/test1.txt
uv run src/parser_main.py test/milestone-2/input/test1.pas --output
# Automatically saves to test/milestone-3/output/test1.symtab
uv run src/semantic_main.py test/milestone-3/input/test1.pas --output
```

**Save to custom path:**
```bash
# Save to specific file
uv run python src/main.py test/milestone-1/input/1.pas --output my_output.txt
uv run src/parser_main.py test/milestone-2/input/test1.pas --output my_output.txt
uv run src/semantic_main.py test/milestone-3/input/test1.pas --output my_output.txt
```

**Combine with check mode:**
```bash
# Check against expected output AND save to file
uv run python src/main.py test/milestone-1/input/1.pas --check --output
uv run src/parser_main.py test/milestone-2/input/test1.pas --check --output
uv run src/semantic_main.py test/milestone-3/input/test1.pas --decorated --output
```

```mermaid
stateDiagram-v2
    %% === START STATE ===
    [*] --> S0

    %% === IDENTIFIER ===
    S0 --> ID: LETTER
    ID --> ID: LETTER
    ID --> ID: DIGIT

    %% === NUMBER / REAL ===
    S0 --> NUM: DIGIT
    NUM --> NUM: DIGIT
    NUM --> NUM_DOT: DOT_SYMBOL
    NUM_DOT --> NUM_REAL: DIGIT
    NUM_REAL --> NUM_REAL: DIGIT

    %% === WHITESPACE ===
    S0 --> WS: WS
    WS --> WS: WS

    %% === PUNCTUATION / DELIMITERS ===
    S0 --> SC: SEMICOLON
    S0 --> COM: COMMA
    S0 --> OPENP: LPAREN
    OPENP --> CMTP: ASTERISK
    S0 --> RP: RPAREN
    S0 --> LB: LBRACKET
    S0 --> RB: RBRACKET
    S0 --> DOT: DOT_SYMBOL
    DOT --> RANGE: DOT_SYMBOL
    S0 --> COL: COLON_SYMBOL
    COL --> ASSIGN: EQUALS

    %% === OPERATORS ===
    S0 --> PLUS: PLUS
    S0 --> MINUS: MINUS
    S0 --> MUL: ASTERISK
    S0 --> DIV: SLASH
    S0 --> EQ: EQUALS
    S0 --> LT: LESS_THAN
    LT --> LE: EQUALS
    LT --> NE: GREATER_THAN
    S0 --> GT: GREATER_THAN
    GT --> GE: EQUALS

    %% === STRING LITERAL ===
    S0 --> STR: QUOTE
    STR --> STR: NOT_QUOTE
    STR --> STR_END: QUOTE
    STR_END --> STR: QUOTE

    %% === COMMENTS ===
    %% Block comment: { ... }
    S0 --> CMTB: LBRACE
    CMTB --> CMTB: NOT_RBRACE
    CMTB --> CMTB_END: RBRACE

    %% Parenthesis comment: (* ... *)
    CMTP --> CMTP: ANY
    CMTP --> CMTP_STAR: ASTERISK
    CMTP_STAR --> CMTP_END: RPAREN
    CMTP_STAR --> CMTP_STAR: ASTERISK
    CMTP_STAR --> CMTP: ANY

    %% === KEYWORDS & RESERVED MAP (symbolic) ===
    state KW_ARITHOP
    state KW_LOGOP
    state KW

    ID --> KW_ARITHOP
    ID --> KW_LOGOP
    ID --> KW

    %% === NOTES / TOKEN TYPES ===
    note right of ID : IDENTIFIER
    note right of NUM : NUMBER
    note right of NUM_REAL : NUMBER
    note right of WS : WHITESPACE
    note right of SC : SEMICOLON
    note right of COM : COMMA
    note right of DOT : DOT
    note right of RANGE : RANGE_OPERATOR
    note right of OPENP : LPARENTHESIS
    note right of RP : RPARENTHESIS
    note right of LB : LBRACKET
    note right of RB : RBRACKET
    note right of COL : COLON
    note right of ASSIGN : ASSIGN_OPERATOR
    note right of PLUS : ARITHMETIC_OPERATOR
    note right of MINUS : ARITHMETIC_OPERATOR
    note right of MUL : ARITHMETIC_OPERATOR
    note right of DIV : ARITHMETIC_OPERATOR
    note right of EQ : RELATIONAL_OPERATOR
    note right of LT : RELATIONAL_OPERATOR
    note right of LE : RELATIONAL_OPERATOR
    note right of NE : RELATIONAL_OPERATOR
    note right of GT : RELATIONAL_OPERATOR
    note right of GE : RELATIONAL_OPERATOR
    note right of STR_END : STRING_LITERAL
    note right of CMTB_END : COMMENT
    note right of CMTP_END : COMMENT

    note right of KW_ARITHOP : ARITHMETIC_OPERATOR (div, mod)
    note right of KW_LOGOP : LOGICAL_OPERATOR (and, or, not)
    note right of KW : KEYWORD (program, var, begin, end, if, then, else, while, do, for, to, downto, integer, real, boolean, char, array, of, procedure, function, const, type)

    %% === VISUAL CLASSES ===
    classDef loop fill:#fff7ed,stroke:#f59e0b,stroke-width:2px,stroke-dasharray:3 2;
    class ID,NUM,NUM_REAL,WS,STR,CMTB,CMTP,CMTP_STAR loop;

    classDef accept fill:#d1fae5,stroke:#10b981,stroke-width:2px;
    class ID,NUM,NUM_REAL,WS,SC,COM,DOT,RANGE,OPENP,RP,LB,RB,COL,ASSIGN,PLUS,MINUS,MUL,DIV,EQ,LT,LE,NE,GT,GE,STR_END,CMTB_END,CMTP_END,KW,KW_LOGOP,KW_ARITHOP accept;
```

## Pembagian Tugas
| No | NIM      | Nama Lengkap                  | Persentase Pembagian Tugas |
| -- | -------- | ----------------------------- | -------------------------- |
| 1  | 13523021 | Muhammad Raihan Nazhim Oktana | 100%                       |
| 2  | 13523057 | Faqih Muhammad Syuhada        | 100%                       |
| 3  | 13523097 | Shanice Feodora Tjahjono      | 100%                       |
| 4  | 13523105 | Muhammad Fathur Rizky         | 100%                       |
