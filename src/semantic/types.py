from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional


class SimpleTypeKind(Enum):
    INTEGER = auto()
    REAL = auto()
    BOOLEAN = auto()
    CHAR = auto()
    STRING = auto()
    VOID = auto()


@dataclass
class ArrayTypeInfo:
    index_type: 'Type'
    element_type: 'Type'
    low: int
    high: int
    element_size: int
    size: int
    ref_index: Optional[int] = None


@dataclass
class RecordTypeInfo:
    fields: dict[str, tuple['Type', int]]
    size: int
    ref_index: Optional[int] = None


class Type:
    def __init__(self, kind: SimpleTypeKind):
        self.kind = kind
        self.array_info: Optional[ArrayTypeInfo] = None
        self.record_info: Optional[RecordTypeInfo] = None

    def is_simple(self) -> bool:
        return self.array_info is None and self.record_info is None

    def is_array(self) -> bool:
        return self.array_info is not None

    def is_record(self) -> bool:
        return self.record_info is not None

    def is_numeric(self) -> bool:
        return self.kind in (SimpleTypeKind.INTEGER, SimpleTypeKind.REAL)

    def is_ordinal(self) -> bool:
        return self.kind in (SimpleTypeKind.INTEGER, SimpleTypeKind.BOOLEAN, SimpleTypeKind.CHAR)

    def compatible_with(self, other: 'Type') -> bool:
        if self.kind == other.kind:
            if self.is_simple():
                return True
            if self.is_array() and other.is_array():
                return self.array_info.element_type.compatible_with(other.array_info.element_type)

        if self.kind == SimpleTypeKind.REAL and other.kind == SimpleTypeKind.INTEGER:
            return True

        return False

    def __eq__(self, other) -> bool:
        if not isinstance(other, Type):
            return False
        return self.kind == other.kind

    def __repr__(self) -> str:
        if self.is_array():
            return f"array of {self.array_info.element_type}"
        if self.is_record():
            return "record"
        return self.kind.name.lower()


INTEGER_TYPE = Type(SimpleTypeKind.INTEGER)
REAL_TYPE = Type(SimpleTypeKind.REAL)
BOOLEAN_TYPE = Type(SimpleTypeKind.BOOLEAN)
CHAR_TYPE = Type(SimpleTypeKind.CHAR)
STRING_TYPE = Type(SimpleTypeKind.STRING)
VOID_TYPE = Type(SimpleTypeKind.VOID)
