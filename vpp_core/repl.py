"""
================================================================================
  V++ Programming Language — REPL Interactive Shell
================================================================================
"""

import sys
from vpp_core.lexer import Lexer, LexerError
from vpp_core.parser import Parser, ParserError
from vpp_core.evaluator import Interpreter
from vpp_core.objects import VppNull, VppRuntimeError
from vpp_core.diagnostics import format_diagnostic_error, format_runtime_error
from vpp_core import __version__

BANNER = f"""
╔════════════════════════════════════════════════════════════════════════╗
║             NGÔN NGỮ LẬP TRÌNH V++ (Phiên bản {__version__})                     ║
║   • Viết mã không dấu hoặc có dấu tùy ý (Ví dụ: bien x = 10 / x = 10)  ║
║   • Nhập 'tro_giup' hoặc 'trợ_giúp' để xem bảng hướng dẫn câu lệnh     ║
║   • Nhập 'thoat' hoặc 'exit' hoặc bấm Ctrl+C để thoát khỏi chương trình║
╚════════════════════════════════════════════════════════════════════════╝
"""

HELP_TEXT = """
┌────────────────────────────────────────────────────────────────────────┐
│                   HƯỚNG DẪN CÚ PHÁP LẬP TRÌNH V++                      │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Khai báo biến & Hằng số:                                            │
│    x = 10                      hoặc: biến x = 10                       │
│    hằng PI = 3.14159           hoặc: hang PI = 3.14159                 │
│                                                                        │
│ 2. In ra màn hình & Nhập dữ liệu:                                      │
│    nói "Xin chào", x           hoặc: noi "Xin chao", x                 │
│    tên = hỏi("Nhập tên: ")     hoặc: ten = hoi("Nhap ten: ")           │
│                                                                        │
│ 3. Cấu trúc rẽ nhánh điều kiện (Dùng '=' hoặc '==' đều được):          │
│    nếu x = 5 { nói "Bằng 5" } không_thì { nói "Khác 5" }               │
│                                                                        │
│ 4. Vòng lặp siêu đơn giản:                                             │
│    lặp 5 lần { nói "Chào bạn!" }                                       │
│    lặp i từ 1 đến 10 { nói "Số:", i }                                  │
│    lặp x trong [10, 20, 30] { nói x }                                  │
│                                                                        │
│ 5. Hàm & Đệ quy:                                                       │
│    hàm tinh_tong(a, b) { trả_về a + b }                                │
│                                                                        │
│ 6. Hàm tiện ích cực nhanh:                                             │
│    ln(10, 50, 30) => 50        (Số lớn nhất)                           │
│    nn(10, 50, 30) => 10        (Số nhỏ nhất)                           │
│    tổng([1, 2, 3, 4]) => 10    (Tính tổng danh sách)                   │
│    ngẫu_nhiên(1, 100)          (Sinh số ngẫu nhiên)                    │
└────────────────────────────────────────────────────────────────────────┘
"""

def start_repl():
    print(BANNER)
    interpreter = Interpreter(base_dir=".")
    buffer = ""

    while True:
        try:
            prompt = "v++ >>> " if not buffer else "...     "
            line = input(prompt)

            if not buffer and line.strip() in ("thoat", "thoát", "exit", "quit", "thoat()", "thoát()"):
                print("\nTạm biệt! Cảm ơn bạn đã sử dụng V++.")
                break

            if not buffer and line.strip() in ("tro_giup", "trợ_giúp", "help", "tro_giup()", "trợ_giúp()"):
                print(HELP_TEXT)
                continue

            buffer += line + "\n"

            # Check balanced brackets
            open_braces = buffer.count("{") - buffer.count("}")
            open_parens = buffer.count("(") - buffer.count(")")
            open_brackets = buffer.count("[") - buffer.count("]")

            if open_braces > 0 or open_parens > 0 or open_brackets > 0:
                continue

            code = buffer.strip()
            buffer = ""

            if not code:
                continue

            lexer = Lexer(code, filename="<repl>")
            tokens = lexer.tokenize()
            parser = Parser(tokens, filename="<repl>")
            ast = parser.parse()
            res = interpreter.eval(ast)
            if not isinstance(res, VppNull):
                print(f"=> {res.to_string()}")

        except (KeyboardInterrupt, EOFError):
            print("\nTạm biệt! Cảm ơn bạn đã sử dụng V++.")
            break
        except LexerError as le:
            err_msg = format_diagnostic_error("Từ Vựng", le.message, "<repl>", code, le.line, le.column)
            print(err_msg, file=sys.stderr)
            buffer = ""
        except ParserError as pe:
            tok = getattr(pe, 'token', None)
            line_no = tok.line if tok else 1
            col_no = tok.column if tok else 1
            err_msg = format_diagnostic_error("Cú Pháp", pe.message, "<repl>", code, line_no, col_no)
            print(err_msg, file=sys.stderr)
            buffer = ""
        except Exception as ex:
            err_msg = format_runtime_error(ex, "<repl>", code)
            print(err_msg, file=sys.stderr)
            buffer = ""

if __name__ == "__main__":
    start_repl()
