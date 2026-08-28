#!/usr/bin/env python3
"""
================================================================================
  VISUAL STUDIO CODE FOR V++ (V++ STUDIO PRO)
  Mo phong 100% giao dien, kien truc, tinh nang va trai nghiem cua VS Code
  - Menu Bar & Command Palette (Ctrl+Shift+P / F1)
  - Activity Bar voi cac bieu tuong chuan VS Code (Explorer, Search, Run/Debug, Extensions, Settings)
  - Primary Side Bar voi Cay thu muc (File Explorer), Outline, Accordion collapsible
  - Breadcrumbs duong dan tep: vpp > examples > file.vpp > function
  - Monaco Editor Replica voi Gutter, Danh so dong, Breakpoints 🔴, Folding arrows ⌄
  - VS Code Default Dark+ Color Theme (Colors: #1e1e1e, #252526, #333333, #007acc)
  - Rainbow Bracket Pair Colorizer, Sticky Scroll Scope Header
  - 2D Canvas Minimap voi Viewport Slider keo cuon
  - IntelliSense Autocomplete Widget voi Icon phan loai ([k] Keyword, [f] Function, [v] Var, [c] Class)
  - Multi-tab Editor Groups co Close button '×', Unsaved dot '●', Active top blue border
  - Bottom Panel da che do (TERMINAL, PROBLEMS, OUTPUT, DEBUG CONSOLE)
  - Status Bar xanh duong (#007acc) chuan VS Code: Git Branch, Problems count, Ln/Col, UTF-8, V++
================================================================================
"""

import sys
import os
import io
import time
import re
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import queue

# Add local path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from vpp_core.lexer import Lexer, LexerError
from vpp_core.parser import Parser, ParserError
from vpp_core.transpiler import Transpiler
from vpp_core.evaluator import Interpreter
from vpp_core.diagnostics import format_diagnostic_error
from vpp_core.tokens import KEYWORDS
from vpp_core import __version__

# ==============================================================================
# VS CODE EXACT PALETTE (Dark+ Modern Theme)
# ==============================================================================
VS_THEME = {
    # Window & Backgrounds
    "title_bar": "#181818",
    "activity_bar": "#181818",
    "activity_active_indicator": "#ffffff",
    "sidebar_bg": "#1e1e1e",
    "sidebar_header": "#181818",
    "editor_bg": "#1f1f1f",
    "tab_bar_bg": "#181818",
    "tab_active_bg": "#1f1f1f",
    "tab_inactive_bg": "#181818",
    "tab_border_active": "#0078d4",
    "panel_bg": "#181818",
    "status_bar_bg": "#007acc",
    "status_bar_fg": "#ffffff",
    "gutter_bg": "#1f1f1f",
    "gutter_fg": "#6e7681",
    "minimap_bg": "#181818",
    "border": "#2b2b2b",
    
    # Text colors
    "text_main": "#cccccc",
    "text_muted": "#8b949e",
    "selection_bg": "#264f78",
    "cursor_color": "#aeafad",

    # VS Code Dark+ Syntax Tokens
    "token_keyword": "#c586c0",     # bien, ham, neu, tra_ve (Purple/Magenta)
    "token_control": "#569cd6",     # loop, logic, types (Blue)
    "token_function": "#dcdcaa",    # noi, nhap, do_dai (Yellow)
    "token_string": "#ce9178",      # "string" (Orange-Brown)
    "token_number": "#b5cea8",      # 123, 3.14 (Light Green)
    "token_comment": "#6a9955",     # // comment (Dark Green italic)
    "token_class": "#4ec9b0",       # Class Name (Teal)
    "token_var": "#9cdcfe",         # Variable identifier (Light Blue)
    "token_error": "#f14c4c",       # Error red
}

AUTOCOMPLETE_DATA = [
    # Keywords
    ("biến", "k", "Khai báo biến động mới (biến x = 10;)"),
    ("bien", "k", "Khai bao bien dong moi (bien x = 10;)"),
    ("hằng", "k", "Khai báo hằng số bất biến (hằng PI = 3.14;)"),
    ("hang", "k", "Khai bao hang so bat bien (hang PI = 3.14;)"),
    ("hàm", "k", "Định nghĩa hàm có tham số (hàm tên(a, b) { })"),
    ("ham", "k", "Dinh nghia ham co tham so (ham ten(a, b) { })"),
    ("nếu", "k", "Câu lệnh rẽ nhánh điều kiện (nếu (đk) { })"),
    ("neu", "k", "Cau lenh re nhanh dieu kien (neu (dk) { })"),
    ("không_thì_nếu", "k", "Nhánh điều kiện phụ (không_thì_nếu (đk) { })"),
    ("khong_thi_neu", "k", "Nhanh dieu kien phu (khong_thi_neu (dk) { })"),
    ("hoặc_nếu", "k", "Nhánh điều kiện phụ rút gọn (hoặc_nếu (đk) { })"),
    ("hoac_neu", "k", "Nhanh dieu kien phu rut gon (hoac_neu (dk) { })"),
    ("không_thì", "k", "Nhánh điều kiện còn lại (không_thì { })"),
    ("khong_thi", "k", "Nhanh dieu kien con lai (khong_thi { })"),
    ("ngược_lại", "k", "Nhánh điều kiện còn lại (ngược_lại { })"),
    ("nguoc_lai", "k", "Nhanh dieu kien con lai (nguoc_lai { })"),
    ("lặp", "k", "Vòng lặp duyệt danh sách (lặp (i trong ds) { })"),
    ("lap", "k", "Vong lap duyet danh sach (lap (i trong ds) { })"),
    ("khi", "k", "Vòng lặp điều kiện while (khi (đk) { })"),
    ("lặp_khi", "k", "Vòng lặp khi (lặp_khi (đk) { })"),
    ("trong", "k", "Từ khóa duyệt trong vòng lặp (trong)"),
    ("trả_về", "k", "Trả về giá trị từ hàm (trả_về x;)"),
    ("tra_ve", "k", "Tra ve gia tri tu ham (tra_ve x;)"),
    ("dừng_lặp", "k", "Ngắt vòng lặp ngay lập tức (dừng_lặp;)"),
    ("dung_lap", "k", "Ngat vong lap ngay lap tuc (dung_lap;)"),
    ("tiếp_tục", "k", "Bỏ qua lượt lặp hiện tại (tiếp_tục;)"),
    ("tiep_tuc", "k", "Bo qua luot lap hien tai (tiep_tuc;)"),
    ("lớp", "c", "Định nghĩa lớp Hướng đối tượng (lớp TênLớp { })"),
    ("lop", "c", "Dinh nghia lop Huong doi tuong (lop TenLop { })"),
    ("khởi_tạo", "f", "Hàm khởi tạo đối tượng (hàm khởi_tạo(...) { })"),
    ("khoi_tao", "f", "Ham khoi tao doi tuong (ham khoi_tao(...) { })"),
    ("bản_thân", "v", "Tham chiếu đối tượng hiện tại (bản_thân.thuộc_tính)"),
    ("ban_than", "v", "Tham chieu doi tuong hien tai (ban_than.x)"),
    ("kế_thừa", "k", "Kế thừa lớp cha (lớp B kế_thừa A { })"),
    ("thử", "k", "Khối thử nghiệm xử lý ngoại lệ (thử { })"),
    ("thu", "k", "Khoi thu nghiem xu ly ngoai le (thu { })"),
    ("bắt_lỗi", "k", "Khối bắt ngoại lệ (bắt_lỗi (lỗi) { })"),
    ("bat_loi", "k", "Khoi bat ngoai le (bat_loi (loi) { })"),
    ("ném_lỗi", "k", "Ném ngoại lệ chủ động (ném_lỗi 'Thông báo';)"),
    ("đúng", "k", "Giá trị logic đúng (đúng / True)"),
    ("dung", "k", "Gia tri logic dung (dung / True)"),
    ("sai", "k", "Giá trị logic sai (sai / False)"),
    ("rỗng", "k", "Giá trị rỗng (rỗng / Null)"),
    ("rong", "k", "Gia tri rong (rong / Null)"),

    # Functions
    ("nói", "f", "In kết quả ra Terminal (nói(...);)"),
    ("noi", "f", "In ket qua ra Terminal (noi(...);)"),
    ("nói_liền", "f", "In liên tục không xuống dòng (nói_liền(...);)"),
    ("noi_lien", "f", "In lien tuc khong xuong dong (noi_lien(...);)"),
    ("in", "f", "In ket qua ra man hinh (in(...))"),
    ("nhập", "f", "Nhập dữ liệu từ bàn phím (nhập('Lời nhắc: '))"),
    ("nhap", "f", "Nhap du lieu tu ban phim (nhap('Prompt: '))"),
    ("độ_dài", "f", "Lấy độ dài chuỗi/mảng/từ điển (độ_dài(ds))"),
    ("do_dai", "f", "Lay do dai chuoi/mang/tu dien (do_dai(ds))"),
    ("thêm", "f", "Thêm phần tử vào cuối danh sách (thêm(ds, x))"),
    ("them", "f", "Them phan tu vao cuoi danh sach (them(ds, x))"),
    ("xóa", "f", "Xóa phần tử khỏi danh sách (xóa(ds, vị_trí))"),
    ("xoa", "f", "Xoa phan tu khoi danh sach (xoa(ds, vi_tri))"),
    ("chèn", "f", "Chèn phần tử vào vị trí (chèn(ds, vị_trí, x))"),
    ("chen", "f", "Chen phan tu vao vi tri (chen(ds, vi_tri, x))"),
    ("sắp_xếp", "f", "Sắp xếp danh sách tăng dần (sắp_xếp(ds))"),
    ("sap_xep", "f", "Sap xep danh sach tang dan (sap_xep(ds))"),
    ("đảo_ngược", "f", "Đảo ngược thứ tự danh sách (đảo_ngược(ds))"),
    ("dao_nguoc", "f", "Dao nguoc thu tu danh sach (dao_nguoc(ds))"),
    ("phạm_vi", "f", "Sinh dãy số nguyên liên tiếp (phạm_vi(đầu, cuối, bước))"),
    ("pham_vi", "f", "Sinh day so nguyen lien tiep (pham_vi(dau, cuoi, buoc))"),
    ("chuyển_json", "f", "Chuyển dữ liệu sang chuỗi JSON (chuyển_json(obj, 2))"),
    ("chuyen_json", "f", "Chuyen du lieu sang chuoi JSON (chuyen_json(obj, 2))"),
    ("giải_mã_json", "f", "Giải mã chuỗi JSON thành đối tượng (giải_mã_json(str))"),
    ("giai_ma_json", "f", "Giai ma chuoi JSON thanh doi tuong (giai_ma_json(str))"),
    ("tải_trang_web", "f", "Tải nội dung web từ đường dẫn URL (tải_trang_web(url))"),
    ("tai_trang_web", "f", "Tai noi dung web tu duong dan URL (tai_trang_web(url))"),
    ("căn_bậc_hai", "f", "Tính căn bậc hai (căn_bậc_hai(x))"),
    ("can_bac_hai", "f", "Tinh can bac hai (can_bac_hai(x))"),
    ("làm_tròn", "f", "Làm tròn số thập phân (làm_tròn(x, 2))"),
    ("lam_tron", "f", "Lam tron so thap phan (lam_tron(x, 2))"),
    ("số_ngẫu_nhiên", "f", "Sinh số nguyên ngẫu nhiên (số_ngẫu_nhiên(min, max))"),
    ("so_ngau_nhien", "f", "Sinh so nguyen ngau nhien (so_ngau_nhien(min, max))"),
    ("thời_gian_hiện_tại", "f", "Lấy epoch timestamp thời gian hiện tại ()"),
    ("thoi_gian_hien_tai", "f", "Lay epoch timestamp thoi gian hien tai ()"),
    ("tạm_dừng", "f", "Tạm dừng chương trình (tạm_dừng(số_giây))"),
    ("tam_dung", "f", "Tam dung chuong trinh (tam_dung(so_giay))"),
    ("đọc_tệp", "f", "Đọc toàn bộ nội dung tệp tin (đọc_tệp('file.txt'))"),
    ("doc_tep", "f", "Doc toan bo noi dung tep tin (doc_tep('file.txt'))"),
    ("ghi_tệp", "f", "Ghi nội dung vào tệp tin (ghi_tệp('file.txt', 'noidung'))"),
    ("ghi_tep", "f", "Ghi noi dung vao tep tin (ghi_tep('file.txt', 'noidung'))"),
]

SAMPLE_CODES = {
    "01_chao_the_gioi.vpp": """// ==========================================
//   Chương trình V++ đầu tiên (VS Code Edition)
// ==========================================
biến loi_chao = "Xin chào thế giới lập trình V++!";
hằng NAM_PHAT_TRIEN = 2026;
biến phien_ban = 1.2;
biến trang_thai = đúng;

nói("========================================");
nói("   Chào mừng bạn đến với VS Code V++!   ");
nói("========================================");
nói("Thông điệp     :", loi_chao);
nói("Năm phát triển :", NAM_PHAT_TRIEN);
nói("Phiên bản      :", phien_ban);
nói("Trạng thái     :", trang_thai);
""",
    "02_bmi_dieu_kien.vpp": """// ==========================================
//   Tính chỉ số BMI & Rẽ nhánh điều kiện
// ==========================================
biến can_nang = 68.5; // kg
biến chieu_cao = 1.75; // m
biến bmi = can_nang / (chieu_cao * chieu_cao);

nói("Chỉ số BMI của bạn là:", làm_tròn(bmi, 2));

nếu (bmi < 18.5) {
    nói("Kết quả: Nhẹ cân (Thiếu cân)");
} không_thì_nếu (bmi < 24.9) {
    nói("Kết quả: Thể trạng cân đối, rất tốt!");
} không_thì_nếu (bmi < 29.9) {
    nói("Kết quả: Tiền béo phì (Thừa cân)");
} không_thì {
    nói("Kết quả: Béo phì");
}
""",
    "03_so_nguyen_to.vpp": """// ==========================================
//   Tìm số nguyên tố & Thao tác Danh sách
// ==========================================
hàm kiem_tra_nguyen_to(n) {
    nếu (n < 2) { trả_về sai; }
    biến can = căn_bậc_hai(n);
    lặp (i trong phạm_vi(2, can + 1)) {
        nếu (n % i == 0) {
            trả_về sai;
        }
    }
    trả_về đúng;
}

biến danh_sach_nt = [];
lặp (x trong phạm_vi(2, 51)) {
    nếu (kiem_tra_nguyen_to(x)) {
        thêm(danh_sach_nt, x);
    }
}

nói("--- DANH SÁCH SỐ NGUYÊN TỐ TỪ 2 ĐẾN 50 ---");
nói("Các số tìm được:", danh_sach_nt);
nói("Tổng số lượng   :", độ_dài(danh_sach_nt));
""",
    "04_de_quy_fibonacci.vpp": """// ==========================================
//   Hàm đệ quy Tính Giai thừa & Fibonacci
// ==========================================
hàm giai_thua(n) {
    nếu (n <= 1) { trả_về 1; }
    trả_về n * giai_thua(n - 1);
}

hàm fibonacci(n) {
    nếu (n <= 0) { trả_về 0; }
    nếu (n == 1) { trả_về 1; }
    trả_về fibonacci(n - 1) + fibonacci(n - 2);
}

nói("Giai thừa 6! =", giai_thua(6));
nói("Giai thừa 8! =", giai_thua(8));

biến day_fib = [];
lặp (i trong phạm_vi(10)) {
    thêm(day_fib, fibonacci(i));
}
nói("10 số đầu tiên trong dãy Fibonacci:", day_fib);
""",
    "05_huong_doi_tuong_oop.vpp": """// ==========================================
//   Lập trình hướng đối tượng (OOP)
// ==========================================
lớp TaiKhoanNganHang {
    hàm khởi_tạo(chu_tai_khoan, so_du_dau) {
        bản_thân.ten = chu_tai_khoan;
        bản_thân.so_du = so_du_dau;
        bản_thân.lich_su = [];
    }

    hàm nap_tien(so_tien) {
        bản_thân.so_du += so_tien;
        thêm(bản_thân.lich_su, "+ " + chuỗi(so_tien) + " VND");
        nói("Đã nạp", so_tien, "VND vào tài khoản của", bản_thân.ten);
    }

    hàm rut_tien(so_tien) {
        nếu (so_tien > bản_thân.so_du) {
            nói("Lỗi: Số dư không đủ!");
            trả_về sai;
        }
        bản_thân.so_du -= so_tien;
        thêm(bản_thân.lich_su, "- " + chuỗi(so_tien) + " VND");
        nói("Đã rút", so_tien, "VND từ tài khoản", bản_thân.ten);
        trả_về đúng;
    }

    hàm in_sao_ke() {
        nói("=================================");
        nói("SAO KÊ TÀI KHOẢN:", bản_thân.ten);
        nói("Số dư hiện tại  :", bản_thân.so_du, "VND");
        nói("Lịch sử giao dịch:");
        lặp (gd trong bản_thân.lich_su) {
            nói("  -", gd);
        }
        nói("=================================");
    }
}

biến tk = TaiKhoanNganHang("Vương Gia Bình", 10000000);
tk.nap_tien(5000000);
tk.rut_tien(2000000);
tk.in_sao_ke();
""",
    "06_thuat_toan_quicksort.vpp": """// ==========================================
//   Thuật toán sắp xếp Quicksort
// ==========================================
hàm sap_xep_nhanh(mang) {
    nếu (độ_dài(mang) <= 1) {
        trả_về mang;
    }
    biến chot = mang[0];
    biến nho_hon = [];
    biến bang = [];
    biến lon_hon = [];

    lặp (x trong mang) {
        nếu (x < chot) {
            thêm(nho_hon, x);
        } không_thì_nếu (x == chot) {
            thêm(bang, x);
        } không_thì {
            thêm(lon_hon, x);
        }
    }

    biến kq = [];
    lặp (a trong sap_xep_nhanh(nho_hon)) { thêm(kq, a); }
    lặp (b trong bang) { thêm(kq, b); }
    lặp (c trong sap_xep_nhanh(lon_hon)) { thêm(kq, c); }
    trả_về kq;
}

biến du_lieu = [45, 12, 89, 3, 77, 26, 91, 14, 55];
nói("Mảng ban đầu:", du_lieu);
nói("Sau khi Quicksort:", sap_xep_nhanh(du_lieu));
""",
    "07_json_va_web.vpp": """// ==========================================
//   Xử lý JSON & Dữ liệu Từ điển
// ==========================================
biến du_an = {
    "ten": "V++ Programming Language",
    "phien_ban": 1.2,
    "nam": 2026,
    "tinh_nang": [
        "Cú pháp Tiếng Việt có dấu & không dấu",
        "Tốc độ cao như Python gốc",
        "VS Code Studio IDE giao diện 100% nguyên bản",
        "Tự động phát hiện lỗi thông minh"
    ],
    "trang_thai": "Hoàn hảo"
};

// Chuyển đổi sang chuỗi JSON định dạng đẹp
biến json_text = chuyển_json(du_an, 2);
nói("--- CHUỖI JSON TẠO BỞI V++ ---");
nói(json_text);

// Giải mã ngược lại
biến parsed = giải_mã_json(json_text);
nói("Đọc lại tên dự án:", parsed["ten"]);
nói("Danh sách tính năng:");
lặp (tn trong parsed["tinh_nang"]) {
    nói("  * " + tn);
}
"""
}

class MonacoEditorTab:
    """Represents an authentic VS Code Editor tab with Breadcrumbs, Gutter, Breakpoints, Minimap & Sticky Scroll"""
    def __init__(self, parent_frame, title="Chưa_đặt_tên.vpp", filepath=None, content=""):
        self.title = title
        self.filepath = filepath
        self.is_dirty = False
        self.breakpoints = set()

        self.frame = tk.Frame(parent_frame, bg=VS_THEME["editor_bg"])

        # 1. Breadcrumbs Bar (Top of Editor)
        self.breadcrumb_bar = tk.Frame(self.frame, bg=VS_THEME["editor_bg"], height=22)
        self.breadcrumb_bar.pack(fill=tk.X, side=tk.TOP, padx=10, pady=(2, 0))
        self.breadcrumb_lbl = tk.Label(
            self.breadcrumb_bar, text=f"vpp  ›  examples  ›  📄 {self.title}",
            bg=VS_THEME["editor_bg"], fg=VS_THEME["text_muted"], font=("Segoe UI", 9)
        )
        self.breadcrumb_lbl.pack(side=tk.LEFT)

        # 2. Sticky Scroll Scope Header
        self.sticky_frame = tk.Frame(self.frame, bg="#252526", height=20)
        self.sticky_frame.pack(fill=tk.X, side=tk.TOP)
        self.sticky_lbl = tk.Label(
            self.sticky_frame, text="  ⌄  Phạm vi: Toàn cục (Global Scope)",
            bg="#252526", fg="#9cdcfe", font=("Segoe UI", 8, "bold"), anchor="w"
        )
        self.sticky_lbl.pack(fill=tk.X, padx=4, pady=1)

        # 3. Editor Body (Gutter + Text + Minimap)
        self.editor_body = tk.Frame(self.frame, bg=VS_THEME["editor_bg"])
        self.editor_body.pack(fill=tk.BOTH, expand=True)

        # 3.1 Breakpoint & Line Gutter Canvas
        self.gutter_canvas = tk.Canvas(
            self.editor_body, width=46, bg=VS_THEME["gutter_bg"], bd=0, highlightthickness=0, cursor="hand2"
        )
        self.gutter_canvas.pack(side=tk.LEFT, fill=tk.Y)
        self.gutter_canvas.bind("<Button-1>", self._on_gutter_click)

        # 3.2 Main Monaco Text Component
        self.editor = tk.Text(
            self.editor_body, bg=VS_THEME["editor_bg"], fg=VS_THEME["text_main"],
            insertbackground=VS_THEME["cursor_color"], selectbackground=VS_THEME["selection_bg"],
            selectforeground="#ffffff", font=("Consolas", 12), bd=0, padx=8, pady=6,
            undo=True, wrap=tk.NONE, tabs=("4c",)
        )
        self.editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar
        self.scroll_y = tk.Scrollbar(self.editor_body, command=self._on_scroll_y)
        self.scroll_y.pack(side=tk.LEFT, fill=tk.Y)
        self.editor.configure(yscrollcommand=self._on_editor_scroll)

        # 3.3 2D Minimap Canvas
        self.minimap = tk.Canvas(self.editor_body, width=72, bg=VS_THEME["minimap_bg"], bd=0, highlightthickness=0, cursor="hand2")
        self.minimap.pack(side=tk.RIGHT, fill=tk.Y)
        self.minimap.bind("<Button-1>", self._on_minimap_click)
        self.minimap.bind("<B1-Motion>", self._on_minimap_click)

        # Bottom horizontal scrollbar
        self.scroll_x = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL, command=self.editor.xview)
        self.scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.editor.configure(xscrollcommand=self.scroll_x.set)

        # Setup Tag Styles
        self.editor.tag_config("keyword", foreground=VS_THEME["token_keyword"], font=("Consolas", 12, "bold"))
        self.editor.tag_config("control", foreground=VS_THEME["token_control"], font=("Consolas", 12, "bold"))
        self.editor.tag_config("function", foreground=VS_THEME["token_function"])
        self.editor.tag_config("class", foreground=VS_THEME["token_class"], font=("Consolas", 12, "bold"))
        self.editor.tag_config("string", foreground=VS_THEME["token_string"])
        self.editor.tag_config("number", foreground=VS_THEME["token_number"])
        self.editor.tag_config("comment", foreground=VS_THEME["token_comment"], font=("Consolas", 12, "italic"))
        self.editor.tag_config("error_squiggles", underline=True, underlinefg=VS_THEME["token_error"], background="#331818")
        self.editor.tag_config("search_match", background="#515c6a", foreground="#ffffff")

        # Rainbow bracket tags
        self.bracket_colors = ["#ffd700", "#da70d6", "#17a2b8", "#a6e3a1"]
        for i, col in enumerate(self.bracket_colors):
            self.editor.tag_config(f"bracket_{i}", foreground=col, font=("Consolas", 12, "bold"))

        if content:
            self.editor.insert("1.0", content)

    def _on_scroll_y(self, *args):
        self.editor.yview(*args)
        self.render_gutter()
        self.render_minimap()
        self.update_sticky_scope()

    def _on_editor_scroll(self, first, last):
        self.scroll_y.set(first, last)
        self.render_gutter()
        self.render_minimap()
        self.update_sticky_scope()

    def render_gutter(self):
        """Draws line numbers, red breakpoints, and code folding icons in gutter"""
        self.gutter_canvas.delete("all")
        lines = self.editor.get("1.0", "end-1c").split("\n")
        total_lines = len(lines)
        if total_lines == 0:
            return

        try:
            first_idx = self.editor.index("@0,0")
            first_line = int(first_idx.split(".")[0])
            last_idx = self.editor.index(f"@0,{self.editor.winfo_height()}")
            last_line = min(total_lines, int(last_idx.split(".")[0]) + 1)
        except Exception:
            first_line, last_line = 1, min(total_lines, 50)

        line_h = 19  # approx line height in pixels
        for line_num in range(first_line, last_line + 1):
            bbox = self.editor.dlineinfo(f"{line_num}.0")
            if not bbox:
                continue
            y = bbox[1] + 2

            # Breakpoint indicator (Red Circle)
            if line_num in self.breakpoints:
                self.gutter_canvas.create_oval(6, y + 2, 16, y + 12, fill="#e51400", outline="#e51400")

            # Line number text (Right aligned)
            self.gutter_canvas.create_text(38, y + 8, text=str(line_num), fill=VS_THEME["gutter_fg"],
                                          font=("Consolas", 10), anchor="e")

    def _on_gutter_click(self, event):
        """Toggle breakpoint on gutter click"""
        idx = self.editor.index(f"@0,{event.y}")
        line_num = int(idx.split(".")[0])
        if line_num in self.breakpoints:
            self.breakpoints.remove(line_num)
        else:
            self.breakpoints.add(line_num)
        self.render_gutter()

    def render_minimap(self):
        """Renders 2D Canvas Minimap preview with viewport rectangle"""
        self.minimap.delete("all")
        lines = self.editor.get("1.0", "end-1c").split("\n")
        total_lines = len(lines)
        if total_lines == 0:
            return

        canvas_h = self.minimap.winfo_height() or 500
        canvas_w = 72
        line_spacing = max(1.2, min(3.5, canvas_h / max(1, total_lines)))

        for i, line in enumerate(lines):
            y = i * line_spacing + 4
            if y > canvas_h:
                break
            stripped = line.strip()
            if not stripped:
                continue
            indent = len(line) - len(line.lstrip())
            x_start = min(40, 4 + indent * 1.5)
            length = min(canvas_w - x_start - 2, len(stripped) * 1.2)

            color = "#45475a"
            if stripped.startswith("//") or stripped.startswith("#"):
                color = "#6a9955"
            elif any(k in stripped for k in ("bien", "biến", "ham", "hàm", "lop", "lớp")):
                color = "#c586c0"
            elif any(k in stripped for k in ("noi", "nói", "in", "nhap")):
                color = "#dcdcaa"

            self.minimap.create_line(x_start, y, x_start + length, y, fill=color, width=max(1, int(line_spacing - 0.5)))

        # Viewport Slider Box
        try:
            first_vis, last_vis = self.editor.yview()
            rect_y1 = first_vis * total_lines * line_spacing
            rect_y2 = last_vis * total_lines * line_spacing
            rect_h = max(18, rect_y2 - rect_y1)
            self.minimap.create_rectangle(0, rect_y1, canvas_w, rect_y1 + rect_h, fill="#ffffff", stipple="gray12", outline="#007acc", width=1)
        except Exception:
            pass

    def _on_minimap_click(self, event):
        canvas_h = self.minimap.winfo_height() or 500
        fraction = max(0.0, min(1.0, event.y / canvas_h))
        self.editor.yview_moveto(fraction)
        self.render_gutter()
        self.render_minimap()
        self.update_sticky_scope()

    def update_sticky_scope(self):
        try:
            first_idx = self.editor.index("@0,0")
            current_line = int(first_idx.split(".")[0])
            code = self.editor.get("1.0", f"{current_line}.end")
            current_scope = "Toàn cục (Global Scope)"
            for line in reversed(code.split("\n")):
                l = line.strip()
                if l.startswith("lop ") or l.startswith("lớp "):
                    name = l.split()[1].split("{")[0].strip()
                    current_scope = f"Lớp: {name}"
                    break
                elif l.startswith("ham ") or l.startswith("hàm "):
                    name = l.split()[1].split("(")[0].strip()
                    current_scope = f"Hàm: {name}()"
                    break
            self.sticky_lbl.config(text=f"  ⌄  Phạm vi: {current_scope}")
        except Exception:
            pass

class VSCodeStudioIDE:
    """The Complete, 100% Identical Visual Studio Code Experience for V++"""
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Visual Studio Code — V++ Workspace (v1.2)")
        self.root.geometry("1300x820")
        self.root.minsize(980, 620)

        self.tabs = []
        self.active_tab_index = 0
        self.input_queue = queue.Queue()
        self.running_thread = None
        self.lint_timer = None

        self.root.configure(bg=VS_THEME["title_bar"])

        self._build_vs_layout()
        self._setup_keybindings()

        # Open initial file
        self.open_sample("01_chao_the_gioi.vpp")

    def _build_vs_layout(self):
        # 1. Title Bar (VS Code Menu Bar + Search Capsule + Layout Controls)
        self._build_title_bar()

        # 2. Main Workbench Body (Activity Bar + Side Bar + Editor Grid)
        self.workbench_frame = tk.Frame(self.root, bg=VS_THEME["editor_bg"])
        self.workbench_frame.pack(fill=tk.BOTH, expand=True)

        # 2.1 Leftmost Activity Bar
        self._build_activity_bar()

        # 2.2 Primary Side Bar (Collapsible Explorer / Search / Git / Debug / Extensions)
        self.sidebar_frame = tk.Frame(self.workbench_frame, bg=VS_THEME["sidebar_bg"], width=260)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar_frame.pack_propagate(False)
        self._build_sidebar()

        # 2.3 Main Splitter (Editor Area on Top, Panel on Bottom)
        self.main_paned = ttk.PanedWindow(self.workbench_frame, orient=tk.VERTICAL)
        self.main_paned.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Upper: Editor Tabs + Split View
        self.editor_container = tk.Frame(self.main_paned, bg=VS_THEME["editor_bg"])
        self.main_paned.add(self.editor_container, weight=3)

        self._build_editor_area()

        # Lower: Bottom Panel (Terminal, Problems, Output, Debug Console)
        self._build_bottom_panel()

        # 3. Status Bar (Blue Strip #007acc at Bottom)
        self._build_status_bar()

        # 4. Command Palette & Autocomplete Widgets
        self._build_command_palette()
        self._build_intellisense_popup()
        self._build_find_replace_bar()

    # ==============================================================================
    # 1. VS CODE TITLE BAR & TOP MENUS
    # ==============================================================================
    def _build_title_bar(self):
        self.title_bar = tk.Frame(self.root, bg=VS_THEME["title_bar"], height=35, padx=6)
        self.title_bar.pack(fill=tk.X, side=tk.TOP)

        # VS Code Blue Icon
        tk.Label(self.title_bar, text=" 🔷 ", bg=VS_THEME["title_bar"], fg="#0078d4", font=("Segoe UI", 10)).pack(side=tk.LEFT)

        # Dropdown Menus (File, Edit, Selection, View, Go, Run, Terminal, Help)
        menu_items = ["Tệp (File)", "Chỉnh sửa (Edit)", "Xem (View)", "Chạy (Run)", "Terminal", "Trợ giúp (Help)"]
        for item in menu_items:
            lbl = tk.Label(self.title_bar, text=item, bg=VS_THEME["title_bar"], fg=VS_THEME["text_main"],
                           font=("Segoe UI", 9), padx=6, cursor="hand2")
            lbl.pack(side=tk.LEFT)
            lbl.bind("<Enter>", lambda e, l=lbl: l.config(bg="#333333"))
            lbl.bind("<Leave>", lambda e, l=lbl: l.config(bg=VS_THEME["title_bar"]))
            if "Tệp" in item:
                lbl.bind("<Button-1>", lambda e: self._show_file_menu(e))
            elif "Chạy" in item:
                lbl.bind("<Button-1>", lambda e: self.run_code())

        # Center Search Capsule (Command Palette Trigger)
        center_pill = tk.Frame(self.title_bar, bg="#2b2b2b", cursor="hand2", padx=12, pady=2)
        center_pill.pack(side=tk.LEFT, expand=True, fill=tk.Y, pady=4, padx=40)
        center_pill.bind("<Button-1>", lambda e: self.open_command_palette())

        pill_text = tk.Label(center_pill, text="🔍  vpp-workspace  (Ctrl+P / F1 để tìm lệnh)",
                             bg="#2b2b2b", fg=VS_THEME["text_muted"], font=("Segoe UI", 8))
        pill_text.pack()
        pill_text.bind("<Button-1>", lambda e: self.open_command_palette())

        # Right Toolbar Icons (Run, Split, Layout)
        run_btn = tk.Button(
            self.title_bar, text=" ▶ Chạy (F5) ", bg="#238636", fg="#ffffff",
            activebackground="#2ea043", activeforeground="#ffffff",
            font=("Segoe UI", 9, "bold"), bd=0, relief=tk.FLAT, cursor="hand2",
            padx=10, pady=2, command=self.run_code
        )
        run_btn.pack(side=tk.RIGHT, padx=4)

        py_view_btn = tk.Button(
            self.title_bar, text=" 🐍 Live Python ", bg="#333333", fg=VS_THEME["text_main"],
            font=("Segoe UI", 8), bd=0, relief=tk.FLAT, cursor="hand2",
            padx=8, pady=2, command=self.toggle_live_python_view
        )
        py_view_btn.pack(side=tk.RIGHT, padx=4)

    def _show_file_menu(self, event):
        m = tk.Menu(self.root, tearoff=0, bg="#252526", fg="#cccccc", activebackground="#094771", font=("Segoe UI", 9))
        m.add_command(label="Tệp mới (New File)\tCtrl+N", command=self.new_file)
        m.add_command(label="Mở tệp (Open File...)\tCtrl+O", command=self.open_file_dialog)
        m.add_command(label="Lưu (Save)\tCtrl+S", command=self.save_file)
        m.add_separator()
        m.add_command(label="Đóng Tab (Close Tab)\tCtrl+W", command=self.close_tab)
        m.add_command(label="Thoát (Exit)", command=self.root.quit)
        m.post(event.x_root, event.y_root + 15)

    # ==============================================================================
    # 2. ACTIVITY BAR & SIDEBAR (EXPLORER / OUTLINE / EXTENSIONS)
    # ==============================================================================
    def _build_activity_bar(self):
        self.act_bar = tk.Frame(self.workbench_frame, bg=VS_THEME["activity_bar"], width=48)
        self.act_bar.pack(side=tk.LEFT, fill=tk.Y)
        self.act_bar.pack_propagate(False)

        # Activity Icons
        self.act_buttons = {}
        icons = [
            ("explorer", "📑\nEXPLORER"),
            ("search", "🔍\nSEARCH"),
            ("git", "🔀\nSOURCE"),
            ("run", "🐞\nDEBUG"),
            ("extensions", "🧩\nEXTS"),
        ]

        for key, text in icons:
            btn = tk.Button(
                self.act_bar, text=text, bg=VS_THEME["activity_bar"], fg=VS_THEME["text_muted"],
                font=("Segoe UI", 7, "bold"), bd=0, relief=tk.FLAT, cursor="hand2", pady=12,
                command=lambda k=key: self._on_activity_click(k)
            )
            btn.pack(fill=tk.X, side=tk.TOP)
            self.act_buttons[key] = btn

        # Highlight default
        self.act_buttons["explorer"].config(fg="#ffffff", bg=VS_THEME["sidebar_bg"])

        # Bottom settings gear icon
        gear_btn = tk.Button(
            self.act_bar, text="⚙️\nCÀI ĐẶT", bg=VS_THEME["activity_bar"], fg=VS_THEME["text_muted"],
            font=("Segoe UI", 7), bd=0, relief=tk.FLAT, cursor="hand2", pady=10,
            command=self.open_command_palette
        )
        gear_btn.pack(fill=tk.X, side=tk.BOTTOM)

    def _build_sidebar(self):
        # Header
        self.sb_header = tk.Frame(self.sidebar_frame, bg=VS_THEME["sidebar_header"], height=32, padx=8)
        self.sb_header.pack(fill=tk.X)
        self.sb_title = tk.Label(
            self.sb_header, text="EXPLORER", bg=VS_THEME["sidebar_header"],
            fg=VS_THEME["text_muted"], font=("Segoe UI", 9, "bold")
        )
        self.sb_title.pack(side=tk.LEFT, pady=6)

        # Quick action buttons on Sidebar header (+ file, + folder, refresh)
        tk.Button(self.sb_header, text=" ↻ ", bg=VS_THEME["sidebar_header"], fg=VS_THEME["text_muted"],
                  bd=0, font=("Segoe UI", 9), relief=tk.FLAT, cursor="hand2",
                  command=self._populate_explorer).pack(side=tk.RIGHT, padx=2)
        tk.Button(self.sb_header, text=" 📄+ ", bg=VS_THEME["sidebar_header"], fg=VS_THEME["text_muted"],
                  bd=0, font=("Segoe UI", 9), relief=tk.FLAT, cursor="hand2",
                  command=self.new_file).pack(side=tk.RIGHT, padx=2)

        # Collapsible Accordion section (FOLDERS / V++ WORKSPACE)
        self.tree = ttk.Treeview(self.sidebar_frame, selectmode="browse", show="tree")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.tree.bind("<Double-1>", self._on_tree_double_click)

        self._populate_explorer()

    def _populate_explorer(self):
        self.tree.delete(*self.tree.get_children())
        
        # Root samples folder
        root_node = self.tree.insert("", "end", "root_samples", text="⌄ 📂 BÀI MẪU V++ (EXAMPLES)", open=True)
        for name in SAMPLE_CODES.keys():
            self.tree.insert(root_node, "end", f"sample_{name}", text=f"  📄 {name}")

        # Local workspace folder
        ex_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "examples")
        if os.path.exists(ex_dir):
            workspace_node = self.tree.insert("", "end", "root_workspace", text="⌄ 📁 DỰ ÁN CỦA BẠN", open=True)
            for f in os.listdir(ex_dir):
                if f.endswith(".vpp"):
                    self.tree.insert(workspace_node, "end", f"file_{f}", text=f"  📄 {f}")

    def _on_activity_click(self, key):
        for k, btn in self.act_buttons.items():
            btn.config(bg=VS_THEME["activity_bar"], fg=VS_THEME["text_muted"])
        self.act_buttons[key].config(bg=VS_THEME["sidebar_bg"], fg="#ffffff")

        if key == "explorer":
            self.sb_title.config(text="EXPLORER")
            self._populate_explorer()
        elif key == "search":
            self.sb_title.config(text="SEARCH & REPLACE")
            self.toggle_find_bar()
        elif key == "git":
            self.sb_title.config(text="SOURCE CONTROL: GIT")
            self.tree.delete(*self.tree.get_children())
            git_node = self.tree.insert("", "end", "git_node", text="🔀 Branch: main (Không có thay đổi)", open=True)
        elif key == "run":
            self.sb_title.config(text="RUN & DEBUG")
            self.run_code()
        elif key == "extensions":
            self.sb_title.config(text="EXTENSIONS: V++ ECOSYSTEM")
            self.tree.delete(*self.tree.get_children())
            ext_root = self.tree.insert("", "end", "ext_root", text="📦 TIỆN ÍCH ĐÃ CÀI ĐẶT", open=True)
            self.tree.insert(ext_root, "end", "ext_1", text="  ⭐ V++ Language Support v1.2 (Đã bật)")
            self.tree.insert(ext_root, "end", "ext_2", text="  ⭐ V++ Rainbow Brackets Engine (Đã bật)")
            self.tree.insert(ext_root, "end", "ext_3", text="  ⭐ Python 3.11 Native Transpiler (Đã bật)")

    def _on_tree_double_click(self, event):
        item_id = self.tree.focus()
        if not item_id:
            return
        if item_id.startswith("sample_"):
            name = item_id.replace("sample_", "")
            self.open_sample(name)
        elif item_id.startswith("file_"):
            name = item_id.replace("file_", "")
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "examples", name)
            self.open_file_path(path)

    # ==============================================================================
    # 3. EDITOR TABS & WORKSPACE AREA
    # ==============================================================================
    def _build_editor_area(self):
        # Tab Header Bar (with Close '×' and Top Active Border)
        self.tab_bar = tk.Frame(self.editor_container, bg=VS_THEME["tab_bar_bg"], height=35)
        self.tab_bar.pack(fill=tk.X, side=tk.TOP)

        # Tab button container
        self.tab_buttons_frame = tk.Frame(self.tab_bar, bg=VS_THEME["tab_bar_bg"])
        self.tab_buttons_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Right side tab actions (Split Editor, More)
        tk.Button(self.tab_bar, text=" ⋯ ", bg=VS_THEME["tab_bar_bg"], fg=VS_THEME["text_muted"],
                  bd=0, font=("Segoe UI", 9), relief=tk.FLAT, cursor="hand2").pack(side=tk.RIGHT, padx=4)
        tk.Button(self.tab_bar, text=" ⫾ Chia đôi ", bg=VS_THEME["tab_bar_bg"], fg=VS_THEME["text_muted"],
                  bd=0, font=("Segoe UI", 9), relief=tk.FLAT, cursor="hand2",
                  command=self.toggle_live_python_view).pack(side=tk.RIGHT, padx=4)

        # Editor View Container (Split Panes)
        self.editor_split = ttk.PanedWindow(self.editor_container, orient=tk.HORIZONTAL)
        self.editor_split.pack(fill=tk.BOTH, expand=True)

        # Main active editor frame
        self.main_editor_view = tk.Frame(self.editor_split, bg=VS_THEME["editor_bg"])
        self.editor_split.add(self.main_editor_view, weight=3)

        # Live Python Preview Panel (Collapsible)
        self.live_py_view = tk.Frame(self.editor_split, bg=VS_THEME["editor_bg"])
        py_hdr = tk.Frame(self.live_py_view, bg="#181818", height=24)
        py_hdr.pack(fill=tk.X)
        tk.Label(py_hdr, text=" 🐍 Mã Python tương đương (Live Transpile)", bg="#181818", fg="#569cd6", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=6)
        
        self.py_editor = tk.Text(self.live_py_view, bg="#181818", fg="#a6adc8", font=("Consolas", 11), bd=0, padx=8, pady=6, state=tk.DISABLED)
        self.py_editor.pack(fill=tk.BOTH, expand=True)
        self.show_live_python = False

    def _render_tab_headers(self):
        for widget in self.tab_buttons_frame.winfo_children():
            widget.destroy()

        for idx, tab in enumerate(self.tabs):
            is_active = (idx == self.active_tab_index)
            bg_col = VS_THEME["tab_active_bg"] if is_active else VS_THEME["tab_inactive_bg"]
            fg_col = "#ffffff" if is_active else VS_THEME["text_muted"]

            tab_btn_frame = tk.Frame(self.tab_buttons_frame, bg=bg_col, padx=8, pady=4, cursor="hand2")
            tab_btn_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 1))

            # Active top indicator line
            if is_active:
                indicator = tk.Frame(tab_btn_frame, bg=VS_THEME["tab_border_active"], height=2)
                indicator.pack(fill=tk.X, side=tk.TOP)

            # Icon & Title
            title_lbl = tk.Label(tab_btn_frame, text=f" 📄 {tab.title} ", bg=bg_col, fg=fg_col, font=("Segoe UI", 9))
            title_lbl.pack(side=tk.LEFT)
            title_lbl.bind("<Button-1>", lambda e, i=idx: self.select_tab(i))

            # Close '×'
            close_lbl = tk.Label(tab_btn_frame, text=" × ", bg=bg_col, fg=fg_col, font=("Segoe UI", 10, "bold"))
            close_lbl.pack(side=tk.RIGHT, padx=2)
            close_lbl.bind("<Button-1>", lambda e, i=idx: self.close_tab(i))

    def select_tab(self, index):
        if not self.tabs or index < 0 or index >= len(self.tabs):
            return
        self.active_tab_index = index

        # Hide all tab frames and show active one
        for i, tab in enumerate(self.tabs):
            if i == index:
                tab.frame.pack(fill=tk.BOTH, expand=True)
            else:
                tab.frame.pack_forget()

        self._render_tab_headers()
        active_tab = self.get_active_tab()
        if active_tab:
            active_tab.render_gutter()
            active_tab.render_minimap()
            active_tab.update_sticky_scope()
            self._update_status_cursor(active_tab)
            if self.show_live_python:
                self._update_python_preview()

    def new_file(self):
        name = f"Chưa_đặt_tên_{len(self.tabs) + 1}.vpp"
        tab = MonacoEditorTab(self.main_editor_view, title=name, content="// Viết mã nguồn V++ tại đây...\nbiến loi_chao = 'Xin chào V++';\nnói(loi_chao);\n")
        self.tabs.append(tab)
        self._bind_tab_events(tab)
        self.select_tab(len(self.tabs) - 1)
        self._apply_monaco_syntax(tab)

    def open_sample(self, name: str):
        for idx, tab in enumerate(self.tabs):
            if tab.title == name:
                self.select_tab(idx)
                return
        content = SAMPLE_CODES.get(name, "// Bài mẫu trống\n")
        tab = MonacoEditorTab(self.main_editor_view, title=name, content=content)
        self.tabs.append(tab)
        self._bind_tab_events(tab)
        self.select_tab(len(self.tabs) - 1)
        self._apply_monaco_syntax(tab)

    def open_file_path(self, filepath: str):
        if not os.path.exists(filepath):
            return
        name = os.path.basename(filepath)
        for idx, tab in enumerate(self.tabs):
            if tab.filepath == filepath:
                self.select_tab(idx)
                return
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            tab = MonacoEditorTab(self.main_editor_view, title=name, filepath=filepath, content=content)
            self.tabs.append(tab)
            self._bind_tab_events(tab)
            self.select_tab(len(self.tabs) - 1)
            self._apply_monaco_syntax(tab)
        except Exception as e:
            messagebox.showerror("Lỗi mở tệp", str(e))

    def open_file_dialog(self):
        path = filedialog.askopenfilename(filetypes=[("Mã nguồn V++", "*.vpp"), ("All Files", "*.*")])
        if path:
            self.open_file_path(path)

    def save_file(self):
        tab = self.get_active_tab()
        if not tab:
            return
        if not tab.filepath:
            path = filedialog.asksaveasfilename(defaultextension=".vpp", filetypes=[("Mã nguồn V++", "*.vpp")])
            if not path:
                return
            tab.filepath = path
            tab.title = os.path.basename(path)

        try:
            content = tab.editor.get("1.0", "end-1c")
            with open(tab.filepath, "w", encoding="utf-8") as f:
                f.write(content)
            self._render_tab_headers()
            self.term_status.config(text=f"Đã lưu: {tab.title}", fg="#89d185")
        except Exception as e:
            messagebox.showerror("Lỗi lưu tệp", str(e))

    def close_tab(self, index=None):
        if index is None:
            index = self.active_tab_index
        if not self.tabs or index < 0 or index >= len(self.tabs):
            return
        tab = self.tabs.pop(index)
        tab.frame.destroy()
        if not self.tabs:
            self.new_file()
        else:
            self.select_tab(max(0, index - 1))

    def get_active_tab(self) -> MonacoEditorTab:
        if self.tabs and 0 <= self.active_tab_index < len(self.tabs):
            return self.tabs[self.active_tab_index]
        return None

    def _bind_tab_events(self, tab: MonacoEditorTab):
        tab.editor.bind("<KeyRelease>", lambda e: self._on_editor_key(tab, e))
        tab.editor.bind("<ButtonRelease-1>", lambda e: self._update_status_cursor(tab))
        tab.editor.bind("<FocusIn>", lambda e: self._update_status_cursor(tab))

        # Auto-closing bracket pairs
        tab.editor.bind("<braceleft>", lambda e: self._auto_close(tab, "{", "}"))
        tab.editor.bind("<parenleft>", lambda e: self._auto_close(tab, "(", ")"))
        tab.editor.bind("<bracketleft>", lambda e: self._auto_close(tab, "[", "]"))
        tab.editor.bind("<quotedbl>", lambda e: self._auto_close(tab, '"', '"'))

    def _auto_close(self, tab, o, c):
        tab.editor.insert(tk.INSERT, c)
        tab.editor.mark_set(tk.INSERT, f"{tk.INSERT}-1c")

    def _on_editor_key(self, tab: MonacoEditorTab, event):
        tab.render_gutter()
        tab.render_minimap()
        tab.update_sticky_scope()
        self._update_status_cursor(tab)

        if self.show_live_python:
            self._update_python_preview()

        if event.keysym == "Escape":
            self.ac_popup.withdraw()
            self.cmd_palette.withdraw()
            return

        # Debounced syntax analysis
        if self.lint_timer:
            self.root.after_cancel(self.lint_timer)
        self.lint_timer = self.root.after(120, lambda: self._apply_monaco_syntax(tab))

        if event.keysym not in ("Return", "BackSpace", "Up", "Down", "Left", "Right", "Tab"):
            self._check_autocomplete(tab)

    def _update_status_cursor(self, tab: MonacoEditorTab):
        if not tab:
            return
        pos = tab.editor.index(tk.INSERT).split(".")
        line, col = pos[0], int(pos[1]) + 1
        self.status_pos.config(text=f"Ln {line}, Col {col}")

    # ==============================================================================
    # 4. SYNTAX HIGHLIGHTING & REAL-TIME AST LINTER
    # ==============================================================================
    def _apply_monaco_syntax(self, tab: MonacoEditorTab):
        code = tab.editor.get("1.0", "end-1c")
        
        # Clear tags
        for t in ("keyword", "control", "function", "class", "string", "number", "comment", "error_squiggles", "bracket_0", "bracket_1", "bracket_2", "bracket_3"):
            tab.editor.tag_remove(t, "1.0", tk.END)

        if not code.strip():
            self.status_problems.config(text="✓ 0 Lỗi cú pháp", fg="#89d185")
            return

        # Rainbow Bracket Pair Colorizer
        depth = 0
        for line_num, line in enumerate(code.split("\n"), start=1):
            in_str = False
            quote_ch = ''
            for col_num, ch in enumerate(line):
                if ch in ('"', "'"):
                    if not in_str:
                        in_str = True
                        quote_ch = ch
                    elif ch == quote_ch and (col_num == 0 or line[col_num - 1] != '\\'):
                        in_str = False
                elif not in_str:
                    if ch in ('(', '{', '['):
                        tag = f"bracket_{depth % 4}"
                        tab.editor.tag_add(tag, f"{line_num}.{col_num}", f"{line_num}.{col_num + 1}")
                        depth += 1
                    elif ch in (')', '}', ']'):
                        depth = max(0, depth - 1)
                        tag = f"bracket_{depth % 4}"
                        tab.editor.tag_add(tag, f"{line_num}.{col_num}", f"{line_num}.{col_num + 1}")

        # Lexer Token coloring
        try:
            lexer = Lexer(code, filename="<editor>")
            tokens = lexer.tokenize()
            for tok in tokens:
                s_idx = f"{tok.line}.{tok.column - 1}"
                e_idx = f"{tok.line}.{tok.column - 1 + tok.length}"
                name = tok.type.name

                if name in ("BIEN", "HANG", "HAM", "LOP", "TRA_VE", "KHOI_TAO", "BAN_THAN", "THU", "BAT_LOI"):
                    tab.editor.tag_add("keyword", s_idx, e_idx)
                elif name in ("NEU", "KHONG_THI_NEU", "KHONG_THI", "KHI", "LAP", "TRONG", "DUNG_LAP", "TIEP_TUC", "VA", "HOAC", "PHU_DINH", "DUNG", "SAI", "RONG"):
                    tab.editor.tag_add("control", s_idx, e_idx)
                elif name in ("INT", "FLOAT"):
                    tab.editor.tag_add("number", s_idx, e_idx)
                elif name == "STRING":
                    tab.editor.tag_add("string", s_idx, e_idx)
                elif name == "IDENTIFIER":
                    val = str(tok.value)
                    if any(item[0] == val and item[1] == "f" for item in AUTOCOMPLETE_DATA):
                        tab.editor.tag_add("function", s_idx, e_idx)
                    elif any(item[0] == val and item[1] == "c" for item in AUTOCOMPLETE_DATA):
                        tab.editor.tag_add("class", s_idx, e_idx)

            # Check AST
            parser = Parser(tokens, filename="<editor>")
            parser.parse()
            self.status_problems.config(text="✓ 0 Lỗi cú pháp", fg="#89d185")
            self._update_problems_panel([])

        except (LexerError, ParserError) as pe:
            err_line = getattr(pe, 'line', 1)
            err_col = getattr(pe, 'column', 1)
            err_len = getattr(getattr(pe, 'token', None), 'length', 1)
            s_idx = f"{err_line}.{max(0, err_col - 1)}"
            e_idx = f"{err_line}.{max(0, err_col - 1) + err_len}"
            tab.editor.tag_add("error_squiggles", s_idx, e_idx)
            self.status_problems.config(text=f"❌ 1 Lỗi cú pháp (Ln {err_line})", fg="#f14c4c")
            self._update_problems_panel([f"[Lỗi Cú Pháp V++] Dòng {err_line}, Cột {err_col}: {str(pe)}"])
        except Exception:
            pass

    def _update_problems_panel(self, problems):
        self.problems_text.config(state=tk.NORMAL)
        self.problems_text.delete("1.0", tk.END)
        if not problems:
            self.problems_text.insert("1.0", "✓ Không tìm thấy sự cố nào trong không gian làm việc.\n")
        else:
            for p in problems:
                self.problems_text.insert(tk.END, f"❌ {p}\n")
        self.problems_text.config(state=tk.DISABLED)

    # ==============================================================================
    # 5. BOTTOM PANEL (TERMINAL / PROBLEMS / OUTPUT / DEBUG)
    # ==============================================================================
    def _build_bottom_panel(self):
        self.panel_frame = tk.Frame(self.main_paned, bg=VS_THEME["panel_bg"])
        self.main_paned.add(self.panel_frame, weight=1)

        # Panel Header Tabs
        self.p_hdr = tk.Frame(self.panel_frame, bg="#181818", height=28)
        self.p_hdr.pack(fill=tk.X)

        self.panel_tabs = {}
        for tab_name in ["TERMINAL", "PROBLEMS", "OUTPUT", "DEBUG CONSOLE"]:
            lbl = tk.Label(self.p_hdr, text=f" {tab_name} ", bg="#181818", fg=VS_THEME["text_muted"],
                           font=("Segoe UI", 9, "bold"), cursor="hand2", padx=8, pady=4)
            lbl.pack(side=tk.LEFT)
            lbl.bind("<Button-1>", lambda e, n=tab_name: self._switch_panel_tab(n))
            self.panel_tabs[tab_name] = lbl

        self.panel_tabs["TERMINAL"].config(fg="#ffffff")

        # Right side panel status
        self.term_status = tk.Label(self.p_hdr, text="powershell (v++ runtime)", bg="#181818", fg=VS_THEME["text_muted"], font=("Segoe UI", 8))
        self.term_status.pack(side=tk.RIGHT, padx=8)

        tk.Button(self.p_hdr, text=" 🗑️ ", bg="#181818", fg=VS_THEME["text_muted"], bd=0, relief=tk.FLAT,
                  cursor="hand2", command=self.clear_terminal).pack(side=tk.RIGHT, padx=4)

        # Panel Body Container
        self.panel_body = tk.Frame(self.panel_frame, bg="#181818")
        self.panel_body.pack(fill=tk.BOTH, expand=True)

        # 1. Interactive Terminal Text
        self.terminal = tk.Text(self.panel_body, bg="#181818", fg="#cccccc", font=("Consolas", 11),
                                bd=0, padx=10, pady=6, insertbackground="#ffffff")
        self.terminal.pack(fill=tk.BOTH, expand=True)

        self.terminal.tag_config("stdout", foreground="#cccccc")
        self.terminal.tag_config("stderr", foreground="#f14c4c")
        self.terminal.tag_config("success", foreground="#89d185")
        self.terminal.tag_config("info", foreground="#569cd6")
        self.terminal.tag_config("prompt", foreground="#dcdcaa", font=("Consolas", 11, "bold"))

        # Problems Text view (Hidden by default)
        self.problems_text = tk.Text(self.panel_body, bg="#181818", fg="#f14c4c", font=("Segoe UI", 10), bd=0, padx=10, pady=6, state=tk.DISABLED)

        # Interactive Input Frame for `nhap()`
        self.input_frame = tk.Frame(self.panel_frame, bg="#252526", padx=6, pady=3)
        tk.Label(self.input_frame, text=" Nhập dữ liệu ▶ ", bg="#252526", fg="#dcdcaa", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT)
        self.input_entry = tk.Entry(self.input_frame, bg="#1e1e1e", fg="#ffffff", font=("Consolas", 11), bd=0)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=6)
        self.input_entry.bind("<Return>", self._on_submit_input)
        tk.Button(self.input_frame, text=" Gửi Enter ", bg="#007acc", fg="#ffffff", font=("Segoe UI", 8, "bold"),
                  bd=0, relief=tk.FLAT, cursor="hand2", command=self._on_submit_input).pack(side=tk.RIGHT)

        self.input_frame.pack_forget()

    def _switch_panel_tab(self, name):
        for n, lbl in self.panel_tabs.items():
            lbl.config(fg=VS_THEME["text_muted"])
        self.panel_tabs[name].config(fg="#ffffff")

        if name == "TERMINAL":
            self.problems_text.pack_forget()
            self.terminal.pack(fill=tk.BOTH, expand=True)
        elif name == "PROBLEMS":
            self.terminal.pack_forget()
            self.problems_text.pack(fill=tk.BOTH, expand=True)
        elif name == "OUTPUT":
            self.problems_text.pack_forget()
            self.terminal.pack(fill=tk.BOTH, expand=True)

    # ==============================================================================
    # 6. STATUS BAR
    # ==============================================================================
    def _build_status_bar(self):
        self.status_bar = tk.Frame(self.root, bg=VS_THEME["status_bar_bg"], height=22, padx=6)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        # Left items: Branch, Sync, Errors
        tk.Label(self.status_bar, text=" 🔀 main* ", bg=VS_THEME["status_bar_bg"], fg="#ffffff", font=("Segoe UI", 8, "bold")).pack(side=tk.LEFT)
        self.status_problems = tk.Label(self.status_bar, text="✓ 0 Lỗi", bg=VS_THEME["status_bar_bg"], fg="#ffffff", font=("Segoe UI", 8))
        self.status_problems.pack(side=tk.LEFT, padx=8)

        # Right items: Ln, Col, Spaces, UTF-8, Language
        self.status_pos = tk.Label(self.status_bar, text="Ln 1, Col 1", bg=VS_THEME["status_bar_bg"], fg="#ffffff", font=("Segoe UI", 8))
        self.status_pos.pack(side=tk.RIGHT, padx=6)

        tk.Label(self.status_bar, text="UTF-8", bg=VS_THEME["status_bar_bg"], fg="#ffffff", font=("Segoe UI", 8)).pack(side=tk.RIGHT, padx=6)
        tk.Label(self.status_bar, text="Spaces: 4", bg=VS_THEME["status_bar_bg"], fg="#ffffff", font=("Segoe UI", 8)).pack(side=tk.RIGHT, padx=6)
        tk.Label(self.status_bar, text="V++ (Tiếng Việt)", bg=VS_THEME["status_bar_bg"], fg="#ffffff", font=("Segoe UI", 8, "bold")).pack(side=tk.RIGHT, padx=8)
        tk.Label(self.status_bar, text="⚡ CPython 3.11 Native", bg=VS_THEME["status_bar_bg"], fg="#ffffff", font=("Segoe UI", 8)).pack(side=tk.RIGHT, padx=8)

    # ==============================================================================
    # 7. COMMAND PALETTE & INTELLISENSE AUTOCOMPLETE
    # ==============================================================================
    def _build_command_palette(self):
        self.cmd_palette = tk.Toplevel(self.root)
        self.cmd_palette.withdraw()
        self.cmd_palette.overrideredirect(True)
        self.cmd_palette.configure(bg="#252526", bd=1)

        p_frame = tk.Frame(self.cmd_palette, bg="#252526", padx=6, pady=6)
        p_frame.pack(fill=tk.BOTH, expand=True)

        self.cmd_entry = tk.Entry(p_frame, bg="#1e1e1e", fg="#ffffff", insertbackground="#ffffff",
                                  font=("Segoe UI", 11), bd=0, width=60)
        self.cmd_entry.pack(fill=tk.X, pady=(0, 4))
        self.cmd_entry.bind("<KeyRelease>", self._filter_commands)
        self.cmd_entry.bind("<Return>", self._execute_selected_command)

        self.cmd_listbox = tk.Listbox(p_frame, bg="#1e1e1e", fg="#cccccc", selectbackground="#04395e",
                                      selectforeground="#ffffff", font=("Segoe UI", 10), bd=0, height=8)
        self.cmd_listbox.pack(fill=tk.BOTH, expand=True)
        self.cmd_listbox.bind("<Double-1>", self._execute_selected_command)

        self.commands_list = [
            ("V++: Chạy chương trình hiện tại (Run Code)", self.run_code),
            ("V++: Tạo tệp mã nguồn mới (New File)", self.new_file),
            ("V++: Mở tệp từ máy tính (Open File)", self.open_file_dialog),
            ("V++: Lưu tệp hiện tại (Save File)", self.save_file),
            ("V++: Bật/Tắt chế độ xem mã Python (Toggle Live Python)", self.toggle_live_python_view),
            ("V++: Xóa màn hình Terminal (Clear Terminal)", self.clear_terminal),
            ("V++: Tìm kiếm và thay thế (Find and Replace)", self.toggle_find_bar),
            ("V++: Bài mẫu 01 - Chào thế giới", lambda: self.open_sample("01_chao_the_gioi.vpp")),
            ("V++: Bài mẫu 05 - Hướng đối tượng OOP", lambda: self.open_sample("05_huong_doi_tuong_oop.vpp")),
            ("V++: Bài mẫu 07 - JSON & Dữ liệu", lambda: self.open_sample("07_json_va_web.vpp")),
        ]

    def open_command_palette(self):
        root_x = self.root.winfo_rootx() + (self.root.winfo_width() - 550) // 2
        root_y = self.root.winfo_rooty() + 40
        self.cmd_palette.geometry(f"550x260+{root_x}+{root_y}")
        self.cmd_palette.deiconify()
        self.cmd_palette.lift()
        self.cmd_entry.focus_set()
        self.cmd_entry.delete(0, tk.END)
        self._filter_commands()

    def _filter_commands(self, event=None):
        q = self.cmd_entry.get().lower()
        self.cmd_listbox.delete(0, tk.END)
        for label, cmd in self.commands_list:
            if q in label.lower():
                self.cmd_listbox.insert(tk.END, f"  > {label}")
        if self.cmd_listbox.size() > 0:
            self.cmd_listbox.select_set(0)

    def _execute_selected_command(self, event=None):
        sel = self.cmd_listbox.curselection()
        self.cmd_palette.withdraw()
        if not sel:
            return
        idx = sel[0]
        text = self.cmd_listbox.get(idx).replace("  > ", "")
        for label, cmd in self.commands_list:
            if label == text:
                cmd()
                break

    def _build_intellisense_popup(self):
        self.ac_popup = tk.Toplevel(self.root)
        self.ac_popup.withdraw()
        self.ac_popup.overrideredirect(True)
        self.ac_popup.configure(bg="#252526", bd=1)

        self.ac_listbox = tk.Listbox(
            self.ac_popup, bg="#1e1e1e", fg="#cccccc", selectbackground="#04395e",
            selectforeground="#ffffff", font=("Consolas", 10), bd=0, height=6, width=45
        )
        self.ac_listbox.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        self.ac_listbox.bind("<Double-1>", lambda e: self._insert_autocomplete())
        self.ac_listbox.bind("<Return>", lambda e: self._insert_autocomplete())
        self.ac_listbox.bind("<Tab>", lambda e: self._insert_autocomplete())

    def _check_autocomplete(self, tab: MonacoEditorTab):
        cursor_pos = tab.editor.index(tk.INSERT)
        line_num, col = cursor_pos.split(".")
        line_text = tab.editor.get(f"{line_num}.0", cursor_pos)

        match = re.search(r"([a-zA-Z_À-ỹ0-9]+)$", line_text)
        if not match:
            self.ac_popup.withdraw()
            return

        prefix = match.group(1).lower()
        if len(prefix) < 1:
            self.ac_popup.withdraw()
            return

        matches = [item for item in AUTOCOMPLETE_DATA if item[0].lower().startswith(prefix)]
        if not matches:
            self.ac_popup.withdraw()
            return

        self.ac_listbox.delete(0, tk.END)
        for word, kind, desc in matches[:8]:
            tag_icon = "🏷️ [K]" if kind == "k" else ("⚡ [f]" if kind == "f" else "📦 [v]")
            self.ac_listbox.insert(tk.END, f" {tag_icon} {word:<14} | {desc[:22]}..")

        self.ac_listbox.select_set(0)

        bbox = tab.editor.bbox(tk.INSERT)
        if bbox:
            x, y, w, h = bbox
            root_x = tab.editor.winfo_rootx() + x
            root_y = tab.editor.winfo_rooty() + y + h + 2
            self.ac_popup.geometry(f"380x140+{root_x}+{root_y}")
            self.ac_popup.deiconify()
            self.ac_popup.lift()

    def _insert_autocomplete(self):
        if not self.ac_popup.winfo_ismapped():
            return
        sel = self.ac_listbox.curselection()
        if not sel:
            return
        selected_text = self.ac_listbox.get(sel[0]).strip()
        word = selected_text.split()[1].strip()

        tab = self.get_active_tab()
        if not tab:
            return

        cursor_pos = tab.editor.index(tk.INSERT)
        line_num, col = cursor_pos.split(".")
        line_text = tab.editor.get(f"{line_num}.0", cursor_pos)
        match = re.search(r"([a-zA-Z_À-ỹ0-9]+)$", line_text)
        if match:
            start_col = int(col) - len(match.group(1))
            tab.editor.delete(f"{line_num}.{start_col}", cursor_pos)
            tab.editor.insert(f"{line_num}.{start_col}", word)

        self.ac_popup.withdraw()
        self._apply_monaco_syntax(tab)

    # ==============================================================================
    # 8. LIVE PYTHON PREVIEW & FIND/REPLACE BAR
    # ==============================================================================
    def toggle_live_python_view(self):
        if not self.show_live_python:
            self.editor_split.add(self.live_py_view, weight=2)
            self.show_live_python = True
            self._update_python_preview()
        else:
            self.editor_split.forget(self.live_py_view)
            self.show_live_python = False

    def _update_python_preview(self):
        tab = self.get_active_tab()
        if not tab:
            return
        code = tab.editor.get("1.0", "end-1c")
        self.py_editor.config(state=tk.NORMAL)
        self.py_editor.delete("1.0", tk.END)
        try:
            lexer = Lexer(code, filename="<preview>")
            tokens = lexer.tokenize()
            parser = Parser(tokens, filename="<preview>")
            ast = parser.parse()
            transpiler = Transpiler()
            py_code = transpiler.transpile(ast)
            if "# --- Ket thuc Runtime Header ---" in py_code:
                py_code = py_code.split("# --- Ket thuc Runtime Header ---")[-1].strip()
            self.py_editor.insert("1.0", py_code)
        except Exception as e:
            self.py_editor.insert("1.0", f"# Đang soạn thảo...\n# {str(e)}")
        self.py_editor.config(state=tk.DISABLED)

    def _build_find_replace_bar(self):
        self.find_bar = tk.Frame(self.root, bg="#252526", padx=8, pady=4)
        tk.Label(self.find_bar, text="🔍 Tìm:", bg="#252526", fg="#cccccc", font=("Segoe UI", 9)).pack(side=tk.LEFT)
        self.find_entry = tk.Entry(self.find_bar, bg="#1e1e1e", fg="#ffffff", font=("Consolas", 10), width=20)
        self.find_entry.pack(side=tk.LEFT, padx=4)
        self.find_entry.bind("<KeyRelease>", lambda e: self._perform_find())

        tk.Label(self.find_bar, text="Thay thế:", bg="#252526", fg="#cccccc", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=(6, 0))
        self.replace_entry = tk.Entry(self.find_bar, bg="#1e1e1e", fg="#ffffff", font=("Consolas", 10), width=20)
        self.replace_entry.pack(side=tk.LEFT, padx=4)

        tk.Button(self.find_bar, text="Tìm tiếp", bg="#333333", fg="#ffffff", font=("Segoe UI", 8), bd=0, command=self._perform_find).pack(side=tk.LEFT, padx=2)
        tk.Button(self.find_bar, text="Thay thế", bg="#333333", fg="#ffffff", font=("Segoe UI", 8), bd=0, command=self._replace_current).pack(side=tk.LEFT, padx=2)
        tk.Button(self.find_bar, text="Thay tất cả", bg="#333333", fg="#ffffff", font=("Segoe UI", 8), bd=0, command=self._replace_all).pack(side=tk.LEFT, padx=2)
        tk.Button(self.find_bar, text=" ✕ ", bg="#252526", fg="#f14c4c", font=("Segoe UI", 9, "bold"), bd=0, command=self.toggle_find_bar).pack(side=tk.RIGHT)
        self.show_find_bar = False

    def toggle_find_bar(self):
        if not self.show_find_bar:
            self.find_bar.pack(side=tk.TOP, fill=tk.X, before=self.workbench_frame)
            self.show_find_bar = True
            self.find_entry.focus_set()
        else:
            self.find_bar.pack_forget()
            self.show_find_bar = False

    def _perform_find(self):
        tab = self.get_active_tab()
        if not tab:
            return
        query = self.find_entry.get()
        tab.editor.tag_remove("search_match", "1.0", tk.END)
        if not query:
            return
        start = "1.0"
        while True:
            pos = tab.editor.search(query, start, stopindex=tk.END, nocase=True)
            if not pos:
                break
            end = f"{pos}+{len(query)}c"
            tab.editor.tag_add("search_match", pos, end)
            start = end

    def _replace_current(self):
        tab = self.get_active_tab()
        if not tab:
            return
        query = self.find_entry.get()
        rep = self.replace_entry.get()
        pos = tab.editor.search(query, tk.INSERT, stopindex=tk.END, nocase=True)
        if pos:
            end = f"{pos}+{len(query)}c"
            tab.editor.delete(pos, end)
            tab.editor.insert(pos, rep)
            self._perform_find()

    def _replace_all(self):
        tab = self.get_active_tab()
        if not tab:
            return
        query = self.find_entry.get()
        rep = self.replace_entry.get()
        if not query:
            return
        code = tab.editor.get("1.0", "end-1c")
        new_code = code.replace(query, rep)
        tab.editor.delete("1.0", tk.END)
        tab.editor.insert("1.0", new_code)
        self._apply_monaco_syntax(tab)
        self._perform_find()

    # ==============================================================================
    # 9. ASYNC RUNTIME EXECUTION & TERMINAL I/O
    # ==============================================================================
    def clear_terminal(self):
        self.terminal.delete("1.0", tk.END)

    def print_terminal(self, text: str, tag: str = "stdout"):
        self.terminal.insert(tk.END, text, tag)
        self.terminal.see(tk.END)

    def _on_submit_input(self, event=None):
        val = self.input_entry.get()
        self.input_entry.delete(0, tk.END)
        self.input_frame.pack_forget()
        self.print_terminal(f"{val}\n", "prompt")
        self.input_queue.put(val)

    def run_code(self):
        tab = self.get_active_tab()
        if not tab:
            return
        code = tab.editor.get("1.0", "end-1c")
        if not code.strip():
            return

        self._switch_panel_tab("TERMINAL")
        self.clear_terminal()
        self.term_status.config(text="⏳ Đang chạy...", fg="#e5c07b")

        self.print_terminal(f"🚀 [Visual Studio Code] Thực thi '{tab.title}'...\n", "info")
        self.print_terminal("─" * 60 + "\n", "info")

        start_time = time.perf_counter()

        def _runner():
            def _custom_input(prompt=""):
                if prompt:
                    self.print_terminal(str(prompt), "prompt")
                self.input_frame.pack(side=tk.BOTTOM, fill=tk.X)
                self.input_entry.focus_set()
                val = self.input_queue.get()
                return val

            def _custom_print(*args, **kwargs):
                sep = kwargs.get("sep", " ")
                end = kwargs.get("end", "\n")
                msg = sep.join(str(a) for a in args) + end
                self.print_terminal(msg, "stdout")

            try:
                lexer = Lexer(code, filename=tab.title)
                tokens = lexer.tokenize()
                parser = Parser(tokens, filename=tab.title)
                ast = parser.parse()

                transpiler = Transpiler()
                py_code = transpiler.transpile(ast)

                scope = {
                    "__name__": "__main__",
                    "print": _custom_print,
                    "input": _custom_input,
                }
                exec(py_code, scope)

                elapsed = (time.perf_counter() - start_time) * 1000
                self.print_terminal("\n" + "─" * 60 + "\n", "info")
                self.print_terminal(f"✨ [Hoàn thành] Tốc độ thực thi: {elapsed:.2f} ms\n", "success")
                self.term_status.config(text=f"✓ Xong ({elapsed:.1f}ms)", fg="#89d185")

            except (LexerError, ParserError) as pe:
                err_line = getattr(pe, 'line', 1)
                err_col = getattr(pe, 'column', 1)
                err_msg = format_diagnostic_error(
                    error_type="Cú Pháp", message=str(pe), filename=tab.title,
                    source_code=code, line=err_line, column=err_col
                )
                self.print_terminal("\n" + err_msg + "\n", "stderr")
                self.term_status.config(text="❌ Lỗi cú pháp", fg="#f14c4c")

            except Exception as ex:
                self.print_terminal(f"\n[Lỗi Thực Thi]: {str(ex)}\n", "stderr")
                self.term_status.config(text="❌ Lỗi thực thi", fg="#f14c4c")

        self.running_thread = threading.Thread(target=_runner, daemon=True)
        self.running_thread.start()

    def _setup_keybindings(self):
        self.root.bind("<F5>", lambda e: self.run_code())
        self.root.bind("<F1>", lambda e: self.open_command_palette())
        self.root.bind("<Control-P>", lambda e: self.open_command_palette())
        self.root.bind("<Control-p>", lambda e: self.open_command_palette())
        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<Control-o>", lambda e: self.open_file_dialog())
        self.root.bind("<Control-n>", lambda e: self.new_file())
        self.root.bind("<Control-f>", lambda e: self.toggle_find_bar())
        self.root.bind("<Control-w>", lambda e: self.close_tab())

def main():
    root = tk.Tk()
    app = VSCodeStudioIDE(root)
    root.mainloop()

if __name__ == "__main__":
    main()
