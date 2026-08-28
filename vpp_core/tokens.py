"""
V++ Programming Language - Token Definitions
Keywords in Vietnamese without accents (tieng Viet khong dau)
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Any, Optional

class TokenType(Enum):
    # Literals
    INT = auto()
    FLOAT = auto()
    STRING = auto()
    IDENTIFIER = auto()
    
    # Boolean & Null literals
    DUNG = auto()       # dung (true)
    SAI = auto()        # sai (false)
    RONG = auto()       # rong / null (null/nil)
    
    # Variable / Constant declarations
    BIEN = auto()       # bien (var/let)
    HANG = auto()       # hang (const)
    
    # Control flow
    NEU = auto()             # neu (if)
    KHONG_THI_NEU = auto()   # khong_thi_neu / hoac_neu (elif / else if)
    KHONG_THI = auto()       # khong_thi / nguoc_lai (else)
    KHI = auto()             # khi / lap_khi (while)
    LAP = auto()             # lap / cho (for)
    TRONG = auto()           # trong (in)
    LAN = auto()             # lan / lần (times)
    TU = auto()              # tu / từ (from)
    DEN = auto()             # den / đến (to)
    DUNG_LAP = auto()        # dung_lap / ngat / dung (break)
    TIEP_TUC = auto()        # tiep_tuc (continue)
    TRA_VE = auto()          # tra_ve (return)
    
    # Functions & OOP
    HAM = auto()             # ham (def / function)
    LOP = auto()             # lop (class)
    KE_THUA = auto()         # ke_thua (inherits / extends)
    KHOI_TAO = auto()        # khoi_tao (constructor / __init__)
    BAN_THAN = auto()        # ban_than (this / self)
    
    # Exception handling
    THU = auto()             # thu (try)
    BAT_LOI = auto()         # bat_loi (catch / except)
    CUOI_CUNG = auto()       # cuoi_cung (finally)
    NEM_LOI = auto()         # nem_loi (throw / raise)
    
    # Modules
    DUNG_THU_VIEN = auto()   # dung_thu_vien / nhap_thu_vien / tai (import)
    
    # Logical Operators (keywords)
    VA = auto()              # va (and)
    HOAC = auto()            # hoac (or)
    PHU_DINH = auto()        # phu_dinh (not)
    
    # Arithmetic & Assignment Operators
    PLUS = auto()            # +
    MINUS = auto()           # -
    STAR = auto()            # *
    SLASH = auto()           # /
    PERCENT = auto()         # %
    POWER = auto()           # ^ or **
    
    PLUS_PLUS = auto()       # ++
    MINUS_MINUS = auto()     # --
    
    ASSIGN = auto()          # =
    PLUS_ASSIGN = auto()     # +=
    MINUS_ASSIGN = auto()    # -=
    STAR_ASSIGN = auto()     # *=
    SLASH_ASSIGN = auto()    # /=
    PERCENT_ASSIGN = auto()  # %=
    
    # Comparison Operators
    EQ = auto()              # ==
    NOT_EQ = auto()          # !=
    LT = auto()              # <
    GT = auto()              # >
    LTE = auto()             # <=
    GTE = auto()             # >=
    
    # Logical symbol operators
    AND = auto()             # &&
    OR = auto()              # ||
    NOT = auto()             # !
    
    # Arrow
    ARROW = auto()           # -> or =>
    
    # Delimiters
    LPAREN = auto()          # (
    RPAREN = auto()          # )
    LBRACKET = auto()        # [
    RBRACKET = auto()        # ]
    LBRACE = auto()          # {
    RBRACE = auto()          # }
    COMMA = auto()           # ,
    DOT = auto()             # .
    COLON = auto()           # :
    SEMICOLON = auto()       # ;
    
    # Special
    EOF = auto()
    NEWLINE = auto()

@dataclass
class Token:
    type: TokenType
    value: Any
    line: int
    column: int
    length: int = 1

    def __repr__(self):
        return f"Token({self.type.name}, {repr(self.value)}, l:{self.line}, c:{self.column})"

KEYWORDS = {
    # Variables & Constants
    "bien": TokenType.BIEN,
    "biến": TokenType.BIEN,
    "hang": TokenType.HANG,
    "hằng": TokenType.HANG,
    
    # Conditional branches
    "neu": TokenType.NEU,
    "nếu": TokenType.NEU,
    "khong_thi_neu": TokenType.KHONG_THI_NEU,
    "không_thì_nếu": TokenType.KHONG_THI_NEU,
    "hoac_neu": TokenType.KHONG_THI_NEU,
    "hoặc_nếu": TokenType.KHONG_THI_NEU,
    "khong_thi": TokenType.KHONG_THI,
    "không_thì": TokenType.KHONG_THI,
    "nguoc_lai": TokenType.KHONG_THI,
    "ngược_lại": TokenType.KHONG_THI,
    
    # Loops
    "khi": TokenType.KHI,
    "lap_khi": TokenType.KHI,
    "lặp_khi": TokenType.KHI,
    "lap": TokenType.LAP,
    "lặp": TokenType.LAP,
    "cho": TokenType.LAP,
    "trong": TokenType.TRONG,
    "lan": TokenType.LAN,
    "lần": TokenType.LAN,
    "tu": TokenType.TU,
    "từ": TokenType.TU,
    "den": TokenType.DEN,
    "đến": TokenType.DEN,
    "dung_lap": TokenType.DUNG_LAP,
    "dừng_lặp": TokenType.DUNG_LAP,
    "ngat": TokenType.DUNG_LAP,
    "ngắt": TokenType.DUNG_LAP,
    "dung": TokenType.DUNG_LAP,
    "dừng": TokenType.DUNG_LAP,
    "tiep_tuc": TokenType.TIEP_TUC,
    "tiếp_tục": TokenType.TIEP_TUC,
    "tra_ve": TokenType.TRA_VE,
    "trả_về": TokenType.TRA_VE,
    
    # Functions & OOP
    "ham": TokenType.HAM,
    "hàm": TokenType.HAM,
    "lop": TokenType.LOP,
    "lớp": TokenType.LOP,
    "ke_thua": TokenType.KE_THUA,
    "kế_thừa": TokenType.KE_THUA,
    "khoi_tao": TokenType.KHOI_TAO,
    "khởi_tạo": TokenType.KHOI_TAO,
    "ban_than": TokenType.BAN_THAN,
    "bản_thân": TokenType.BAN_THAN,
    "tao": TokenType.IDENTIFIER,
    "tạo": TokenType.IDENTIFIER,
    
    # Exception handling
    "thu": TokenType.THU,
    "thử": TokenType.THU,
    "bat_loi": TokenType.BAT_LOI,
    "bắt_lỗi": TokenType.BAT_LOI,
    "cuoi_cung": TokenType.CUOI_CUNG,
    "cuối_cùng": TokenType.CUOI_CUNG,
    "nem_loi": TokenType.NEM_LOI,
    "ném_lỗi": TokenType.NEM_LOI,
    
    # Modules & Imports
    "dung_thu_vien": TokenType.DUNG_THU_VIEN,
    "dùng_thư_viện": TokenType.DUNG_THU_VIEN,
    "nhap_thu_vien": TokenType.DUNG_THU_VIEN,
    "nhập_thư_viện": TokenType.DUNG_THU_VIEN,
    "tai": TokenType.DUNG_THU_VIEN,
    "tải": TokenType.DUNG_THU_VIEN,
    
    # Literals
    "dung": TokenType.DUNG,
    "đúng": TokenType.DUNG,
    "true": TokenType.DUNG,
    "sai": TokenType.SAI,
    "false": TokenType.SAI,
    "rong": TokenType.RONG,
    "rỗng": TokenType.RONG,
    "null": TokenType.RONG,
    "none": TokenType.RONG,
    
    # Logical Operators
    "va": TokenType.VA,
    "và": TokenType.VA,
    "hoac": TokenType.HOAC,
    "hoặc": TokenType.HOAC,
    "phu_dinh": TokenType.PHU_DINH,
    "phủ_định": TokenType.PHU_DINH,
    "khong": TokenType.PHU_DINH,
    "không": TokenType.PHU_DINH,
}
