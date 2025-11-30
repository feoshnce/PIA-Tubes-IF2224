from enum import Enum, auto
from typing import Optional
from .types import Type


class ObjectKind(Enum):
    CONSTANT = auto()
    VARIABLE = auto()
    TYPE = auto()
    PROCEDURE = auto()
    FUNCTION = auto()
    PROGRAM = auto()
    FIELD = auto()


class SymbolEntry:
    def __init__(self, name: str, obj_kind: ObjectKind, type: Type,
                 level: int, address: int, ref: int = 0,
                 normal: bool = True, link: int = 0):
        self.name = name
        self.obj_kind = obj_kind
        self.type = type
        self.level = level
        self.address = address
        self.ref = ref
        self.normal = normal
        self.link = link


class ArrayEntry:
    def __init__(self, index_type: Type, element_type: Type,
                 low: int, high: int, element_size: int):
        self.index_type = index_type
        self.element_type = element_type
        self.low = low
        self.high = high
        self.element_size = element_size
        self.size = (high - low + 1) * element_size


class BlockEntry:
    def __init__(self, last: int = 0, lpar: int = 0, psze: int = 0, vsze: int = 0):
        self.last = last
        self.lpar = lpar
        self.psze = psze
        self.vsze = vsze


class SymbolTable:
    def __init__(self):
        self.tab: list[SymbolEntry] = []
        self.atab: list[ArrayEntry] = []
        self.btab: list[BlockEntry] = [BlockEntry()]
        self.tx = -1
        self.ax = -1
        self.bx = 0
        self.level = 0
        self.display: list[int] = [0] * 10
        self.dx = 0

    def enter(self, name: str, obj_kind: ObjectKind, type: Type,
              level: int = None, ref: int = 0, normal: bool = True, address: int = None) -> int:
        self.tx += 1
        if level is None:
            level = self.level

        block_idx = self.display[level]
        last_idx = self.btab[block_idx].last

        if obj_kind == ObjectKind.VARIABLE:
            link = last_idx if (last_idx != 0 and self.tab[last_idx].obj_kind == ObjectKind.VARIABLE) else 0
            if address is None:
                address = self.dx
                self.dx += 1
            self.btab[block_idx].vsze += 1
        elif obj_kind == ObjectKind.FIELD:
            link = last_idx if (last_idx != 0 and self.tab[last_idx].obj_kind in (ObjectKind.VARIABLE, ObjectKind.FIELD)) else 0
            if address is None:
                address = 0
        else:
            link = last_idx
            if address is None:
                address = 0

        self.btab[block_idx].last = self.tx

        entry = SymbolEntry(
            name=name,
            obj_kind=obj_kind,
            type=type,
            level=level,
            address=address,
            ref=ref,
            normal=normal,
            link=link
        )
        self.tab.append(entry)
        return self.tx

    def enter_array(self, index_type: Type, element_type: Type,
                    low: int, high: int, element_size: int) -> int:
        self.ax += 1
        entry = ArrayEntry(
            index_type=index_type,
            element_type=element_type,
            low=low,
            high=high,
            element_size=element_size
        )
        self.atab.append(entry)
        return self.ax

    def enter_block(self) -> int:
        self.bx += 1
        entry = BlockEntry()
        self.btab.append(entry)
        return self.bx

    def lookup(self, name: str) -> Optional[int]:
        for lev in range(self.level, -1, -1):
            block_idx = self.display[lev]
            i = self.btab[block_idx].last

            while i != 0:
                if self.tab[i].name == name:
                    return i
                i = self.tab[i].link

        for i in range(self.tx, -1, -1):
            if self.tab[i].name == name and self.tab[i].level == 0:
                return i
        return None

    def lookup_current_scope(self, name: str) -> Optional[int]:
        block_idx = self.display[self.level]
        i = self.btab[block_idx].last

        while i != 0:
            if self.tab[i].name == name:
                return i
            i = self.tab[i].link

        return None

    def enter_scope(self):
        self.level += 1
        block_idx = self.enter_block()
        self.display[self.level] = block_idx
        self.dx = 3

    def exit_scope(self):
        if self.level > 0:
            self.level -= 1
            block_idx = self.display[self.level]
            self.dx = self.btab[block_idx].vsze

    def get_entry(self, index: int) -> Optional[SymbolEntry]:
        if 0 <= index < len(self.tab):
            return self.tab[index]
        return None

    def get_array_entry(self, index: int) -> Optional[ArrayEntry]:
        if 0 <= index < len(self.atab):
            return self.atab[index]
        return None

    def get_block_entry(self, index: int) -> Optional[BlockEntry]:
        if 0 <= index < len(self.btab):
            return self.btab[index]
        return None
