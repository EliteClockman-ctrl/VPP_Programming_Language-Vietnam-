"""
V++ Programming Language - Runtime Object System
"""

from typing import Any, Dict, List, Optional, Callable

class VppObject:
    def type_name(self) -> str:
        return "doi_tuong"

    def to_string(self) -> str:
        return str(self)

    def is_truthy(self) -> bool:
        return True

    def __repr__(self):
        return self.to_string()

class VppNumber(VppObject):
    def __init__(self, value: float | int):
        self.value = value

    def type_name(self) -> str:
        return "so"

    def to_string(self) -> str:
        if isinstance(self.value, float) and self.value.is_integer():
            return str(int(self.value))
        return str(self.value)

    def is_truthy(self) -> bool:
        return self.value != 0

    def __eq__(self, other):
        if isinstance(other, VppNumber):
            return self.value == other.value
        return False

    def __hash__(self):
        return hash(self.value)

class VppString(VppObject):
    def __init__(self, value: str):
        self.value = value

    def type_name(self) -> str:
        return "chuoi"

    def to_string(self) -> str:
        return self.value

    def is_truthy(self) -> bool:
        return len(self.value) > 0

    def __eq__(self, other):
        if isinstance(other, VppString):
            return self.value == other.value
        return False

    def __hash__(self):
        return hash(self.value)

class VppBoolean(VppObject):
    def __init__(self, value: bool):
        self.value = bool(value)

    def type_name(self) -> str:
        return "dung_sai"

    def to_string(self) -> str:
        return "dung" if self.value else "sai"

    def is_truthy(self) -> bool:
        return self.value

    def __eq__(self, other):
        if isinstance(other, VppBoolean):
            return self.value == other.value
        return False

    def __hash__(self):
        return hash(self.value)

class VppNull(VppObject):
    def type_name(self) -> str:
        return "rong"

    def to_string(self) -> str:
        return "rong"

    def is_truthy(self) -> bool:
        return False

    def __eq__(self, other):
        return isinstance(other, VppNull)

    def __hash__(self):
        return hash(None)

VPP_DUNG = VppBoolean(True)
VPP_SAI = VppBoolean(False)
VPP_RONG = VppNull()

class VppList(VppObject):
    def __init__(self, elements: Optional[List[VppObject]] = None):
        self.elements: List[VppObject] = elements if elements is not None else []

    def type_name(self) -> str:
        return "danh_sach"

    def to_string(self) -> str:
        items_str = ", ".join(elem.to_string() if not isinstance(elem, VppString) else f'"{elem.value}"' for elem in self.elements)
        return f"[{items_str}]"

    def is_truthy(self) -> bool:
        return len(self.elements) > 0

class VppDict(VppObject):
    def __init__(self, pairs: Optional[Dict[Any, VppObject]] = None):
        self.pairs: Dict[Any, VppObject] = pairs if pairs is not None else {}

    def type_name(self) -> str:
        return "tu_dien"

    def to_string(self) -> str:
        items = []
        for k, v in self.pairs.items():
            k_str = f'"{k.value}"' if isinstance(k, VppString) else k.to_string()
            v_str = f'"{v.value}"' if isinstance(v, VppString) else v.to_string()
            items.append(f"{k_str}: {v_str}")
        return "{" + ", ".join(items) + "}"

    def is_truthy(self) -> bool:
        return len(self.pairs) > 0

class VppFunction(VppObject):
    def __init__(self, name: str, params: List[str], body: Any, env: Any):
        self.name = name
        self.params = params
        self.body = body
        self.env = env # Closure environment

    def type_name(self) -> str:
        return "ham"

    def to_string(self) -> str:
        return f"<ham {self.name}({', '.join(self.params)})>"

class VppBuiltinFunction(VppObject):
    def __init__(self, name: str, fn: Callable[..., VppObject]):
        self.name = name
        self.fn = fn

    def type_name(self) -> str:
        return "ham_he_thong"

    def to_string(self) -> str:
        return f"<ham_he_thong {self.name}>"

class VppClass(VppObject):
    def __init__(self, name: str, parent: Optional['VppClass'], methods: Dict[str, VppFunction]):
        self.name = name
        self.parent = parent
        self.methods = methods

    def find_method(self, method_name: str) -> Optional[VppFunction]:
        if method_name in self.methods:
            return self.methods[method_name]
        if self.parent is not None:
            return self.parent.find_method(method_name)
        return None

    def type_name(self) -> str:
        return "lop"

    def to_string(self) -> str:
        return f"<lop {self.name}>"

class VppInstance(VppObject):
    def __init__(self, klass: VppClass):
        self.klass = klass
        self.fields: Dict[str, VppObject] = {}

    def get_property(self, prop_name: str) -> VppObject:
        if prop_name in self.fields:
            return self.fields[prop_name]
        method = self.klass.find_method(prop_name)
        if method is not None:
            return method
        return VPP_RONG

    def set_property(self, prop_name: str, value: VppObject):
        self.fields[prop_name] = value

    def type_name(self) -> str:
        return f"doi_tuong_{self.klass.name}"

    def to_string(self) -> str:
        return f"<doi_tuong {self.klass.name}>"

# Control flow signals
class ReturnSignal(Exception):
    def __init__(self, value: VppObject):
        self.value = value

class BreakSignal(Exception):
    pass

class ContinueSignal(Exception):
    pass

class VppRuntimeError(Exception):
    def __init__(self, message: str, line: int = 0, column: int = 0, traceback: Optional[List[str]] = None):
        loc = f" tai dong {line}, cot {column}" if line > 0 else ""
        super().__init__(f"Loi thuc thi (RuntimeError){loc}: {message}")
        self.message = message
        self.line = line
        self.column = column
        self.traceback = traceback or []
