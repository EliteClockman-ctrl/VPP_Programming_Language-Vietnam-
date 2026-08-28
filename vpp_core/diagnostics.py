"""
================================================================================
  V++ Programming Language — Smart Error Diagnostic Engine
  Hệ thống chẩn đoán lỗi thông minh định dạng chuẩn tiếng Việt có dấu
================================================================================
"""

import sys
import re
import difflib
from typing import Optional, List
from .tokens import KEYWORDS

def suggest_keyword(word: str) -> Optional[str]:
    """Gợi ý từ khóa V++ gần nhất nếu gõ sai chính tả"""
    matches = difflib.get_close_matches(word.lower(), KEYWORDS.keys(), n=1, cutoff=0.6)
    return matches[0] if matches else None

def format_diagnostic_error(
    error_type: str,
    message: str,
    filename: str,
    source_code: Optional[str] = None,
    line: int = 1,
    column: int = 1,
    length: int = 1,
    suggestion: Optional[str] = None
) -> str:
    """Định dạng thông báo lỗi cú pháp / từ vựng trực quan tiếng Việt có dấu"""
    border = "═" * 60
    header = f"╔{border}╗\n║ [LỖI {error_type.upper()}] Tệp: {filename:<43} ║\n╚{border}╝"
    
    location = f"  👉 Vị trí: Dòng {line}, Cột {column}"
    lines_out = [header, location, f"  ❌ Chi tiết: {message}"]
    
    if source_code:
        source_lines = source_code.splitlines()
        if 1 <= line <= len(source_lines):
            code_line = source_lines[line - 1]
            line_str = f"  {line:4d} | "
            lines_out.append("\n" + line_str + code_line)
            
            # Pointer ^^^
            col_offset = max(0, column - 1)
            pointer_len = max(1, length)
            pointer_str = " " * len(line_str) + " " * col_offset + "^" * pointer_len
            lines_out.append(pointer_str)
            
            # Extract suggestion if not given
            if not suggestion:
                try:
                    raw_sub = code_line[col_offset:].strip()
                    word = raw_sub.split()[0].strip(";(),{}[]+-*/=")
                    if word:
                        guess = suggest_keyword(word)
                        if guess and guess != word:
                            suggestion = f"Có phải bạn muốn viết từ khóa '{guess}'?"
                except Exception:
                    pass

    if suggestion:
        lines_out.append(f"\n  💡 Gợi ý: {suggestion}")
        
    lines_out.append("═" * 62 + "\n")
    return "\n".join(lines_out)

def format_runtime_error(ex: Exception, filename: str, source_code: Optional[str] = None) -> str:
    """Dịch và định dạng lỗi thực thi (Runtime Error) sang tiếng Việt có dấu rõ ràng"""
    ex_type = type(ex).__name__
    raw_msg = str(ex)
    
    # Vietnamese translations for common runtime errors
    vn_type = "THỰC THI"
    vn_msg = raw_msg
    suggestion = None

    if isinstance(ex, ZeroDivisionError) or "division by zero" in raw_msg:
        vn_type = "PHÉP TOÁN"
        vn_msg = "Không thể thực hiện phép chia cho số 0."
        suggestion = "Kiểm tra lại mẫu số hoặc thêm điều kiện kiểm tra trước khi chia."
    elif isinstance(ex, NameError) or "is not defined" in raw_msg:
        vn_type = "TÊN BIẾN / HÀM"
        # Extract name: name 'xyz' is not defined
        m = re.search(r"name '([^']+)' is not defined", raw_msg)
        if m:
            var_name = m.group(1).replace("_vpp_", "")
            vn_msg = f"Biến hoặc hàm '{var_name}' chưa được khai báo trước khi sử dụng."
            guess = suggest_keyword(var_name)
            if guess:
                suggestion = f"Có phải bạn muốn gõ '{guess}'?"
            else:
                suggestion = f"Hãy gán giá trị trước: {var_name} = ... hoặc kiểm tra lại tên."
        else:
            vn_msg = f"Định danh chưa được định nghĩa: {raw_msg}"
    elif isinstance(ex, IndexError) or "list index out of range" in raw_msg:
        vn_type = "CHỈ SỐ DANH SÁCH"
        vn_msg = "Chỉ số truy cập vượt quá độ dài của danh sách (Index out of range)."
        suggestion = "Dùng hàm độ_dài(danh_sách) để kiểm tra số lượng phần tử trước khi truy cập."
    elif isinstance(ex, KeyError):
        vn_type = "TỪ ĐIỂN (KEY)"
        vn_msg = f"Khóa {raw_msg} không tồn tại trong bảng từ điển."
        suggestion = "Kiểm tra lại tên khóa hoặc dùng 'chứa(từ_điển, khóa)' để kiểm tra."
    elif isinstance(ex, TypeError):
        vn_type = "KIỂU DỮ LIỆU"
        vn_msg = f"Không thể thực hiện phép tính giữa các kiểu dữ liệu không tương thích: {raw_msg}"
        suggestion = "Dùng hàm chuỗi(...) hoặc số_nguyên(...) để chuyển đổi kiểu dữ liệu phù hợp."
    elif isinstance(ex, ValueError):
        vn_type = "GIÁ TRỊ"
        vn_msg = f"Giá trị truyền vào không hợp lệ: {raw_msg}"
    elif isinstance(ex, RecursionError):
        vn_type = "ĐỆ QUY VÔ TẬN"
        vn_msg = "Hàm đệ quy gọi lại chính nó quá nhiều lần gây tràn ngăn xếp bộ nhớ."
        suggestion = "Kiểm tra lại điều kiện dừng của hàm đệ quy."
    elif isinstance(ex, FileNotFoundError):
        vn_type = "TỆP TIN"
        vn_msg = f"Không tìm thấy tệp tin chỉ định: {raw_msg}"
        suggestion = "Kiểm tra lại đường dẫn tệp tin có chính xác không."

    border = "═" * 60
    header = f"╔{border}╗\n║ [LỖI {vn_type.upper()}] Tệp: {filename:<43} ║\n╚{border}╝"
    lines_out = [header, f"  ❌ Chi tiết lỗi: {vn_msg}"]
    
    if suggestion:
        lines_out.append(f"  💡 Gợi ý khắc phục: {suggestion}")
        
    lines_out.append("═" * 62 + "\n")
    return "\n".join(lines_out)
