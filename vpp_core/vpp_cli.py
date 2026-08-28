#!/usr/bin/env python3
"""
V++ Programming Language - CLI & REPL Interface
Chay tep .vpp, bien dich sang Python, hoac khoi dong REPL tuong tac
"""

import sys
import os
import argparse
from typing import Optional
from vpp_core.lexer import Lexer, LexerError
from vpp_core.parser import Parser, ParserError
from vpp_core.evaluator import Interpreter
from vpp_core.objects import VppRuntimeError, VppNull
from vpp_core.transpiler import Transpiler
from vpp_core import __version__

from vpp_core.diagnostics import format_diagnostic_error, format_runtime_error

def run_file(filepath: str, use_transpiler: bool = True):
    if not os.path.exists(filepath):
        print(f"Loi: Khong tim thay tep '{filepath}'", file=sys.stderr)
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8") as f:
        source_code = f.read()

    base_dir = os.path.dirname(os.path.abspath(filepath))

    try:
        lexer = Lexer(source_code, filename=filepath)
        tokens = lexer.tokenize()
        parser = Parser(tokens, filename=filepath)
        ast = parser.parse()

        if use_transpiler:
            transpiler = Transpiler()
            py_code = transpiler.transpile(ast)
            exec(py_code, {"__name__": "__main__"})
        else:
            interpreter = Interpreter(base_dir=base_dir)
            interpreter.eval(ast)

    except LexerError as le:
        err_msg = format_diagnostic_error("Từ Vựng", le.message, filepath, source_code, le.line, le.column)
        print(err_msg, file=sys.stderr)
        sys.exit(1)
    except ParserError as pe:
        tok = getattr(pe, 'token', None)
        line = tok.line if tok else 1
        col = tok.column if tok else 1
        length = getattr(tok, 'length', 1) if tok else 1
        err_msg = format_diagnostic_error("Cú Pháp", pe.message, filepath, source_code, line, col, length)
        print(err_msg, file=sys.stderr)
        sys.exit(1)
    except Exception as ex:
        err_msg = format_runtime_error(ex, filepath, source_code)
        print(err_msg, file=sys.stderr)
        sys.exit(1)

def run_inline_code(code: str):
    try:
        lexer = Lexer(code, filename="<dong_lenh>")
        tokens = lexer.tokenize()
        parser = Parser(tokens, filename="<dong_lenh>")
        ast = parser.parse()
        transpiler = Transpiler()
        py_code = transpiler.transpile(ast)
        exec(py_code, {"__name__": "__main__"})
    except (LexerError, ParserError) as pe:
        tok = getattr(pe, 'token', None)
        line = getattr(pe, 'line', tok.line if tok else 1)
        col = getattr(pe, 'column', tok.column if tok else 1)
        err_msg = format_diagnostic_error("Cú Pháp", str(pe), "<dòng_lệnh>", code, line, col)
        print(err_msg, file=sys.stderr)
        sys.exit(1)
    except Exception as ex:
        err_msg = format_runtime_error(ex, "<dòng_lệnh>", code)
        print(err_msg, file=sys.stderr)
        sys.exit(1)

def compile_file(input_path: str, output_path: Optional[str] = None):
    if not os.path.exists(input_path):
        print(f"Lỗi: Không tìm thấy tệp '{input_path}'", file=sys.stderr)
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        source = f.read()

    try:
        lexer = Lexer(source, filename=input_path)
        tokens = lexer.tokenize()
        parser = Parser(tokens, filename=input_path)
        ast = parser.parse()
        transpiler = Transpiler()
        py_code = transpiler.transpile(ast)

        if output_path is None:
            if input_path.endswith(".vpp"):
                output_path = input_path[:-4] + ".py"
            else:
                output_path = input_path + ".py"

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(py_code)

        print(f"[V++] Đã biên dịch thành công '{input_path}' -> '{output_path}'")
    except Exception as e:
        print(f"Lỗi biên dịch: {e}", file=sys.stderr)
        sys.exit(1)

def start_repl():
    try:
        from repl import start_repl as run_repl
        run_repl()
    except Exception as e:
        print(f"Lỗi khởi động REPL: {e}", file=sys.stderr)

def print_help_summary():
    print("""
--- CÁC TỪ KHÓA CHÍNH TRONG V++ (CÓ DẤU HOẶC KHÔNG DẤU) ---
  - bien / biến x = 10;            : Khai báo biến động
  - hang / hằng PI = 3.14;         : Khai báo hằng số
  - neu / nếu (dk) { }             : Câu lệnh điều kiện
  - khong_thi_neu / hoặc_nếu (dk)  : Điều kiện phụ (elif)
  - khong_thi / ngược_lại { }      : Trường hợp còn lại (else)
  - khi / lặp_khi (dk) { }         : Vòng lặp while
  - lap / lặp (i trong ds) { }     : Vòng lặp for-in
  - dung_lap / dừng_lặp;           : break
  - tiep_tuc / tiếp_tục;           : continue
  - ham / hàm ten_ham(a, b) { }    : Định nghĩa hàm
  - tra_ve / trả_về gia_tri;       : Trả về từ hàm
  - lop / lớp TenLop { }           : Định nghĩa lớp (OOP)
  - khoi_tao / khởi_tạo() { }      : Hàm tạo (constructor)
  - ban_than / bản_thân            : Tham chiếu đối tượng hiện tại (self)
  - thu / thử { } bat_loi (e) { }  : Xử lý ngoại lệ try/catch

--- CÁC HÀM CÓ SẴN (BUILT-IN) ---
  - noi(...), nói(...)             : In kết quả ra màn hình
  - noi_lien(...), nói_liền(...)   : In không xuống dòng
  - nhap("prompt") / nhập(...)     : Nhập dữ liệu từ bàn phím
  - do_dai(ds) / độ_dài            : Lấy độ dài chuỗi/mảng/từ điển
  - them(ds, pt) / xoa(ds)         : Thêm/xóa phần tử khỏi danh sách
  - chuyen_json(obj) / chuyển_json : Chuyển đổi sang chuỗi JSON
  - giai_ma_json(str) / giải_mã    : Đọc và giải mã chuỗi JSON
  - tai_trang_web(url) / tải       : Tải nội dung web từ internet
  - doc_tep(p) / ghi_tep(p, c)     : Đọc / Ghi tập tin
""")

def launch_studio():
    try:
        from vpp_studio import main as studio_main
        studio_main()
    except Exception as e:
        print(f"Lỗi khởi động V++ Studio: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="V++ - Ngôn ngữ lập trình tiếng Việt (.vpp)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ sử dụng:
  vpp.exe chuong_trinh.vpp          Chạy tệp mã nguồn .vpp (Tốc độ tối đa)
  vpp.exe -c 'nói("Xin chào V++!")' Chạy trực tiếp mã lệnh V++
  vpp.exe bien_dich file.vpp        Biên dịch .vpp sang Python .py
  vpp.exe                           Khởi động REPL tương tác trên Terminal
"""
    )

    parser.add_argument("file", nargs="?", help="Duong dan den tep ma nguon .vpp")
    parser.add_argument("-c", "--code", help="Chay doan ma V++ truyen vao tu dong lenh")
    parser.add_argument("-i", "--interpret", action="store_true", help="Chay voi bo thong dich tung buoc (Tree-walking Interpreter)")
    parser.add_argument("-g", "--gui", action="store_true", help="Mo giao dien do hoa V++ Studio IDE")
    parser.add_argument("-v", "--version", action="version", version=f"V++ Phien ban {__version__}")
    parser.add_argument("command", nargs="?", choices=["bien_dich", "compile", "chay", "run", "studio", "ide"], help="Lenh tuy chon")
    parser.add_argument("-o", "--output", help="Duong dan tep dau ra khi bien dich")

    args, unknown = parser.parse_known_args()

    if args.gui or args.command in ("studio", "ide") or args.file in ("studio", "ide"):
        launch_studio()
        return

    if args.command in ("bien_dich", "compile") or args.file in ("bien_dich", "compile"):
        target_file = (unknown[0] if unknown else None) if args.file in ("bien_dich", "compile") else args.file
        if not target_file:
            print("Loi: Can chi dinh tep .vpp de bien dich", file=sys.stderr)
            sys.exit(1)
        compile_file(target_file, args.output)
        return

    if args.code:
        run_inline_code(args.code)
        return

    if args.file:
        run_file(args.file, use_transpiler=not args.interpret)
        return

    # No arguments -> start REPL
    start_repl()

if __name__ == "__main__":
    main()
