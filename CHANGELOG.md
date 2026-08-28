# 📝 V++ Programming Language — Changelog

All notable changes, features, and improvements for the **V++ (Vietnamese Plus Plus)** programming language are documented in this file.

---

## 🚀 [1.0.0] - Official First Release

### 🌟 1. Native Vietnamese Syntax & Flexible Writing Style
- Full support for **100% Vietnamese syntax** (both unaccented and accented):
  - **Variable & Constant Declarations**: `bien` / `biến`, `hang` / `hằng`, or direct assignment `x = 10`.
  - **Conditional Branching**: `neu` / `nếu` (`if`), `khong_thi_neu` / `hoac_neu` / `hoặc_nếu` (`elif`), `khong_thi` / `không_thì` / `nguoc_lai` (`else`).
  - **Natural Loops**: `lap` / `lặp` ... `trong` (`for...in`), `lap` / `lặp` ... `lan` / `lần` (repeat $N$ times), `lap ... tu ... den ...` (range loops), `khi` / `lap_khi` (`while`).
  - **Loop Controls**: `dung` / `ngat` / `ngắt` (`break`), `tiep_tuc` / `tiếp_tục` (`continue`).
  - **Function Declarations**: `ham` / `hàm` (`def`/`func`), `tra_ve` / `trả_về` (`return`).
  - **Boolean & Null Values**: `dung` / `đúng` (`true`), `sai` (`false`), `rong` / `rỗng` / `null` (`None`/`null`).
  - **Logical Operators**: `va` / `và` / `&&` (`AND`), `hoac` / `hoặc` / `||` (`OR`), `phu_dinh` / `phủ_định` / `!` (`NOT`).

---

### ⚡ 2. Dual Execution Engines
- **High-Speed Python 3 Transpiler**:
  - Automatically transpiles V++ source code into highly optimized Python 3 runtime code (up to 10x faster for array operations and recursion).
  - Supports direct export to pure Python files via `vpp bien_dich file.vpp -o output.py`.
- **AST Tree-Walking Interpreter**:
  - Direct interpreter for instant evaluation, unit testing, and dynamic execution.
- **Diagnostics & Error Reporting System**:
  - Comprehensive, localized error messages indicating exact line, column, and actionable suggestions.

---

### 🏛️ 3. Full Object-Oriented Programming (OOP)
- Class declarations: `lop` / `lớp` (`class`).
- Inheritance: `ke_thua` / `kế_thừa` (`extends`/`inheritance`).
- Constructors: `khoi_tao` / `khởi_tạo` (`__init__`/`constructor`).
- Instance reference: `ban_than` / `bản_thân` (`this`/`self`).
- Full support for polymorphism, encapsulation, and method overriding.

---

### 📚 4. Rich Built-in Standard Library
- **Text & String Processing**:
  - `chu_hoa` / `chữ_hoa` (uppercase), `chu_thuong` / `chữ_thường` (lowercase), `viet_hoa_dau` / `viết_hoa_đầu` (title case).
  - `dem_tu` / `đếm_từ` (word count), `dao_nguoc` / `đảo_ngược` (reverse), `cat_chuoi` / `cắt_chuỗi` (split), `noi_chuoi` / `nối_chuỗi` (join), `thay_the` / `thay_thế` (replace).
- **Mathematics & Statistics**:
  - `can` / `căn` (square root), `luy_thua` / `lũy_thừa` (power), `lam_tron` / `làm_tròn` (round).
  - `tong` / `tổng` (sum), `trung_binh` / `trung_bình` (average), `lon_nhat` / `lớn_nhất` (`ln`/max), `nho_nhat` / `nhỏ_nhất` (`nn`/min).
- **Arrays & Collections**:
  - `them` / `thêm` (append), `chen` / `chèn` (insert), `xoa` / `xóa` (remove), `sap_xep` / `sắp_xếp` (sort), `chon_ngau_nhien` / `chọn_ngẫu_nhiên` (random choice).
- **File System & OS I/O**:
  - `doc_tep` / `đọc_tệp` (read file), `ghi_tep` / `ghi_tệp` (write file), `xoa_tep` / `xóa_tệp` (delete file), `danh_sach_tep` / `danh_sách_tệp` (list files).
  - `lenh` / `lệnh` (safe shell command execution with timeout management).
- **Networking & Fullstack Web Server**:
  - `tao_may_chu_web` / `tạo_máy_chủ_web`: Built-in HTTP REST API engine with HTML5/CSS3 static file serving.
  - `tai_trang_web` / `tải_trang_web`: Fetch web content and remote APIs.
  - `chuyen_json` / `chuyển_json`, `giai_ma_json` / `giải_mã_json` (JSON serialization & parsing).

---

### 🛠️ 5. Tooling & Developer Ecosystem
- **Standalone Windows Binary (`vpp.exe`)**:
  - Self-contained executable with zero dependencies (no Python installation required).
- **1-Click Auto Installer (`dist/installer.bat`)**:
  - Automatically sets up the system PATH and registers `.vpp` file association.
- **VS Code Extension (`vpp-language-support`)**:
  - Full syntax highlighting, snippet autocompletion, and file icon support.
- **Interactive REPL Shell**:
  - Live interactive coding directly in the terminal.
