# V++ Programming Language (.vpp)
### The First Native Vietnamese Syntax Programming Language

**V++** is an object-oriented and procedural programming language designed with an intuitive, natural, and powerful Vietnamese syntax (supporting both unaccented and accented Vietnamese). V++ fully supports modern language features: variables/constants, first-class functions, recursion, Object-Oriented Programming (classes, inheritance, constructors), exception handling (`try`/`catch`/`finally`), arrays & dictionaries, a rich built-in standard library, an interactive REPL, an instant Tree-Walking Interpreter, and a high-speed Python 3 Transpiler.

---

## 🌟 Key Features

- **Intuitive Vietnamese Syntax**: Easy to read, write, and remember (`bien`/`biến`, `hang`/`hằng`, `neu`/`nếu`, `khong_thi`/`không_thì`, `khi`, `lap`/`lặp`, `ham`/`hàm`, `lop`/`lớp`, `ban_than`/`bản_thân`, etc.).
- **Standard File Extension**: `.vpp` (e.g., `program.vpp`).
- **Flexible Execution Modes**:
  1. **Tree-Walking Interpreter**: Instant evaluation with detailed line/column syntax diagnostics.
  2. **Python 3 Transpiler**: Maximum speed and seamless export to `.py` for integration into existing pipelines.
- **Object-Oriented Programming (OOP)**: Class declarations (`lop`/`lớp`), constructors (`khoi_tao`/`khởi_tạo`), inheritance (`ke_thua`/`kế_thừa`), and instance referencing (`ban_than`/`bản_thân`).
- **Built-in Standard Library**:
  - **Mathematics**: `can`/`căn` (square root), `luy_thua`/`lũy_thừa` (power), `lam_tron`/`làm_tròn` (round), `tong`/`tổng` (sum), `trung_binh`/`trung_bình` (average).
  - **String Manipulation**: `chu_hoa`/`chữ_hoa` (uppercase), `chu_thuong`/`chữ_thường` (lowercase), `viet_hoa_dau`/`viết_hoa_đầu` (title case), `cat_chuoi`/`cắt_chuỗi` (split), `noi_chuoi`/`nối_chuỗi` (join), `dao_nguoc`/`đảo_ngược` (reverse).
  - **Arrays & Collections**: `them`/`thêm` (append), `chen`/`chèn` (insert), `xoa`/`xóa` (remove), `sap_xep`/`sắp_xếp` (sort), `chon_ngau_nhien`/`chọn_ngẫu_nhiên` (random choice).
  - **I/O & File Management**: `doc_tep`/`đọc_tệp` (read file), `ghi_tep`/`ghi_tệp` (write file), `xoa_tep`/`xóa_tệp` (delete file), `danh_sach_tep`/`danh_sách_tệp` (list files).
  - **Networking & Web**: Built-in HTTP server (`tao_may_chu_web`/`tạo_máy_chủ_web`), REST APIs, and HTTP request clients (`tai_trang_web`/`tải_trang_web`).
  - **Time & Utilities**: `cho`/`chờ` / `ngu`/`ngủ` (sleep), `thoi_gian_hien_tai`/`thời_gian_hiện_tại` (current timestamp).
- **Interactive CLI & REPL Environment**: Run source files directly, compile on the fly, or launch the interactive terminal shell.
- **VS Code Extension & GUI Studio**: Full syntax highlighting, snippet autocompletion, and dedicated `vpp_studio` GUI IDE.

---

## 📁 Project Structure

```text
vpp/
├── main.py                     # Master CLI and Runner entry point
├── vpp.exe                     # Standalone Windows Binary (Single file executable)
├── vpp_studio.exe              # Visual Studio-style GUI IDE for V++
├── README.md                   # Project overview & documentation (English)
├── huong_dan_su_dung.md        # Comprehensive Vietnamese language guide
├── vpp_core/                   # Core Language Engine
│   ├── tokens.py               # Token definitions & Keyword table
│   ├── lexer.py                # Lexical Analyzer (Tokenizer)
│   ├── ast_nodes.py            # Abstract Syntax Tree (AST) definitions
│   ├── parser.py               # Syntax Parser
│   ├── objects.py              # Type system & Runtime Object representations
│   ├── environment.py          # Scope & Environment manager
│   ├── builtins.py             # Built-in Standard Library functions
│   ├── evaluator.py            # AST Tree-walking Interpreter
│   ├── transpiler.py           # High-performance Python 3 Transpiler
│   ├── web_framework.py        # Native REST API & Web Server Engine
│   ├── vpp_cli.py              # CLI Argument Handler
│   ├── repl.py                 # Interactive REPL Shell
│   └── vpp_studio.py           # GUI IDE Application
├── dist/                       # Release distribution & auto-installer
│   ├── installer.bat           # 1-Click Windows PATH installer
│   └── README.txt              # End-user release guide
├── examples/                   # Official example programs (.vpp)
│   ├── 01_chao_the_gioi.vpp
│   ├── 02_tinh_toan_va_dieu_kien.vpp
│   ├── 03_vong_lap_va_danh_sach.vpp
│   ├── 04_ham_va_de_quy.vpp
│   ├── 05_huong_doi_tuong.vpp
│   ├── 06_thuat_toan_sap_xep.vpp
│   ├── 07_json_va_web.vpp
│   ├── 08_mini_game_doan_so.vpp
│   ├── 09_vong_lap_sieu_de.vpp
│   ├── 13_fullstack_web_va_backend.vpp
│   └── 16_vpp_sieu_de_sieu_tien_loi.vpp
├── tests/                      # Automated Unit & Integration Test Suite
│   ├── test_all.py
│   ├── test_advanced.py
│   └── run_tests.py
└── vpp-vscode-extension/       # Visual Studio Code Extension
    ├── package.json
    ├── language-configuration.json
    └── syntaxes/vpp.tmLanguage.json
```

---

## 🚀 Installation & Getting Started

### 1. Requirements
- **Windows / Linux / macOS** with **Python 3.10+** (or use standalone `vpp.exe` with zero dependencies).

### 2. Basic Commands

```bash
# 1. Run a V++ source file (.vpp)
python3 main.py examples/01_chao_the_gioi.vpp
# or directly if using vpp.exe:
vpp examples/01_chao_the_gioi.vpp

# 2. Run with Transpiler mode (High Performance)
python3 main.py -t examples/06_thuat_toan_sap_xep.vpp

# 3. Execute inline code directly from the command line
python3 main.py -c 'in("Xin chao ngon ngu V++!");'

# 4. Transpile .vpp to standalone Python 3 code
python3 main.py bien_dich examples/05_huong_doi_tuong.vpp -o tai_khoan.py

# 5. Launch the Interactive REPL Shell
python3 main.py

# 6. Launch the V++ Studio Visual IDE
python3 main.py --studio
```

### 3. Run Automated Tests
```bash
python3 tests/run_tests.py
# or
python3 -m unittest discover tests
```

---

## 📖 Keyword Reference Table

| V++ Keyword (Unaccented / Accented) | English Equivalent | Example Syntax |
| :--- | :--- | :--- |
| `bien` / `biến` | Variable declaration | `bien x = 10;` / `x = 10` |
| `hang` / `hằng` | Constant declaration | `hang PI = 3.14;` |
| `neu` / `nếu` | `if` condition | `neu (x > 5) { ... }` |
| `khong_thi_neu` / `hoac_neu` / `hoặc_nếu` | `else if` condition | `hoac_neu (x == 5) { ... }` |
| `khong_thi` / `không_thì` / `nguoc_lai` | `else` block | `khong_thi { ... }` |
| `khi` / `lap_khi` | `while` loop | `khi (i < 10) { i = i + 1; }` |
| `lap` / `lặp` ... `trong` | `for...in` loop | `lap (item trong danh_sach) { ... }` |
| `lap` / `lặp` ... `lan` / `lần` | Repeat loop $N$ times | `lap 5 lan { ... }` |
| `dung_lap` / `dung` / `ngat` / `ngắt` | `break` loop | `ngat;` |
| `tiep_tuc` / `tiếp_tục` | `continue` iteration | `tiep_tuc;` |
| `ham` / `hàm` | Function declaration | `ham tinh_tong(a, b) { tra_ve a + b; }` |
| `tra_ve` / `trả_về` | `return` value | `tra_ve ket_qua;` |
| `lop` / `lớp` | `class` declaration | `lop HocSinh { ... }` |
| `ke_thua` / `kế_thừa` | Inheritance (`extends`) | `lop HocSinh ke_thua Nguoi { ... }` |
| `khoi_tao` / `khởi_tạo` | `constructor` (`__init__`) | `khoi_tao(ten, tuoi) { ... }` |
| `ban_than` / `bản_thân` | Object reference (`this`/`self`) | `ban_than.ten = ten;` |
| `thu` / `thử` | `try` block | `thu { ... }` |
| `bat_loi` / `bắt_lỗi` | `catch` block | `bat_loi (loi) { ... }` |
| `cuoi_cung` / `cuối_cùng` | `finally` block | `cuoi_cung { ... }` |
| `nem_loi` / `ném_lỗi` | `throw` exception | `nem_loi "Mau so bang 0";` |
| `dung` / `đúng` | Boolean `true` | `bien ok = dung;` |
| `sai` | Boolean `false` | `bien loi = sai;` |
| `rong` / `rỗng` / `null` | Null value (`None`) | `bien res = rong;` |
| `va` / `và` / `&&` | Logical `AND` | `neu (a > 0 va b > 0) { ... }` |
| `hoac` / `hoặc` / `||` | Logical `OR` | `neu (a == 0 hoac b == 0) { ... }` |
| `phu_dinh` / `phủ_định` / `!` | Logical `NOT` | `neu (!tim_thay) { ... }` |

---

## 📄 License & Community

V++ is released as **Open Source Software** under the MIT License. Developed and maintained with pride by Vietnamese developers for the global community.
