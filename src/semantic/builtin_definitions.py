from .symbol_table import ObjectKind
from .types import (
    INTEGER_TYPE, REAL_TYPE, BOOLEAN_TYPE, CHAR_TYPE, STRING_TYPE, VOID_TYPE
)

# Format: (name, kind, type)
RESERVED_WORDS = [
    ('salah', ObjectKind.CONSTANT, BOOLEAN_TYPE),
    ('benar', ObjectKind.CONSTANT, BOOLEAN_TYPE),
    ('integer', ObjectKind.TYPE, INTEGER_TYPE),
    ('real', ObjectKind.TYPE, REAL_TYPE),
    ('boolean', ObjectKind.TYPE, BOOLEAN_TYPE),
    ('char', ObjectKind.TYPE, CHAR_TYPE),
    ('string', ObjectKind.TYPE, STRING_TYPE),
    ('dan', ObjectKind.PROCEDURE, VOID_TYPE),
    ('atau', ObjectKind.PROCEDURE, VOID_TYPE),
    ('tidak', ObjectKind.PROCEDURE, VOID_TYPE),
    ('bagi', ObjectKind.PROCEDURE, VOID_TYPE),
    ('mod', ObjectKind.PROCEDURE, VOID_TYPE),
    ('program', ObjectKind.PROCEDURE, VOID_TYPE),
    ('variabel', ObjectKind.PROCEDURE, VOID_TYPE),
    ('konstanta', ObjectKind.PROCEDURE, VOID_TYPE),
    ('tipe', ObjectKind.PROCEDURE, VOID_TYPE),
    ('prosedur', ObjectKind.PROCEDURE, VOID_TYPE),
    ('fungsi', ObjectKind.PROCEDURE, VOID_TYPE),
    ('mulai', ObjectKind.PROCEDURE, VOID_TYPE),
    ('selesai', ObjectKind.PROCEDURE, VOID_TYPE),
    ('jika', ObjectKind.PROCEDURE, VOID_TYPE),
    ('maka', ObjectKind.PROCEDURE, VOID_TYPE),
    ('selain-itu', ObjectKind.PROCEDURE, VOID_TYPE),
    ('selama', ObjectKind.PROCEDURE, VOID_TYPE),
    ('lakukan', ObjectKind.PROCEDURE, VOID_TYPE),
    ('untuk', ObjectKind.PROCEDURE, VOID_TYPE),
    ('ke', ObjectKind.PROCEDURE, VOID_TYPE),
    ('turun-ke', ObjectKind.PROCEDURE, VOID_TYPE),
    ('larik', ObjectKind.PROCEDURE, VOID_TYPE),
]

STANDARD_LIBRARY = [
    ('write', ObjectKind.PROCEDURE, VOID_TYPE),
    ('writeln', ObjectKind.PROCEDURE, VOID_TYPE),
    ('read', ObjectKind.PROCEDURE, VOID_TYPE),
    ('readln', ObjectKind.PROCEDURE, VOID_TYPE),
    ('abs', ObjectKind.FUNCTION, INTEGER_TYPE),
    ('sqr', ObjectKind.FUNCTION, INTEGER_TYPE),
    ('sqrt', ObjectKind.FUNCTION, REAL_TYPE),
    ('sin', ObjectKind.FUNCTION, REAL_TYPE),
    ('cos', ObjectKind.FUNCTION, REAL_TYPE),
    ('exp', ObjectKind.FUNCTION, REAL_TYPE),
    ('ln', ObjectKind.FUNCTION, REAL_TYPE),
    ('odd', ObjectKind.FUNCTION, BOOLEAN_TYPE),
    ('ord', ObjectKind.FUNCTION, INTEGER_TYPE),
    ('chr', ObjectKind.FUNCTION, CHAR_TYPE),
    ('succ', ObjectKind.FUNCTION, INTEGER_TYPE),
    ('pred', ObjectKind.FUNCTION, INTEGER_TYPE),
]
