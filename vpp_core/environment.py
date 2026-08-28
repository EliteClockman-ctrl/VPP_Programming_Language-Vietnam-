"""
V++ Programming Language - Environment & Scoping
"""

from typing import Dict, Set, Optional, Any
from .objects import VppObject, VppRuntimeError

class Environment:
    def __init__(self, parent: Optional['Environment'] = None):
        self.parent = parent
        self.values: Dict[str, VppObject] = {}
        self.constants: Set[str] = set()

    def define(self, name: str, value: VppObject, is_const: bool = False):
        self.values[name] = value
        if is_const:
            self.constants.add(name)
        else:
            self.constants.discard(name)

    def assign(self, name: str, value: VppObject, line: int = 0, column: int = 0):
        if name in self.values:
            if name in self.constants:
                raise VppRuntimeError(f"Không thể gán lại giá trị cho hằng số '{name}'", line, column)
            self.values[name] = value
            return
        if self.parent is not None:
            if self.parent.contains(name):
                self.parent.assign(name, value, line, column)
                return
        self.define(name, value, is_const=False)

    def get(self, name: str, line: int = 0, column: int = 0) -> VppObject:
        if name in self.values:
            return self.values[name]
        if self.parent is not None:
            return self.parent.get(name, line, column)
        raise VppRuntimeError(f"Bien hoac ham '{name}' chua duoc dinh nghia", line, column)

    def contains(self, name: str) -> bool:
        if name in self.values:
            return True
        if self.parent is not None:
            return self.parent.contains(name)
        return False
