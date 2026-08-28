# V++ Programming Language (.vpp)
### Ngôn Ngữ Lập Trình Thuần Cú Pháp Tiếng Việt Không Dấu

**V++** là ngôn ngữ lập trình hướng đối tượng và thủ tục, được thiết kế với cú pháp tiếng Việt không dấu hoàn toàn tự nhiên, thân thiện và mạnh mẽ. V++ hỗ trợ đầy đủ các tính năng hiện đại: biến/hằng, hàm, đệ quy, hướng đối tượng (OOP - class/kế thừa), xử lý ngoại lệ (try/catch), mảng/dict, thư viện chuẩn phong phú, bộ thông dịch trực tiếp (Interpreter) và trình biên dịch tối ưu (Transpiler sang Python 3).

---

## 🚀 Tính Năng Nổi Bật

- **Từ khóa tiếng Việt không dấu**: Dễ đọc, dễ học, dễ nhớ (`bien`, `hang`, `neu`, `khong_thi`, `khi`, `lap`, `ham`, `lop`, `ban_than`,...).
- **Đuôi tệp chuẩn**: `.vpp` (Ví dụ: `chuong_trinh.vpp`).
- **Hai chế độ thực thi linh hoạt**:
  1. **Tree-walking Interpreter**: Chạy tức thì, thông báo lỗi dòng/cột chi tiết.
  2. **Transpiler sang Python 3**: Tối ưu tốc độ cao, hỗ trợ xuất sang `.py` để tích hợp vào các dự án lớn.
- **Lập trình Hướng đối tượng (OOP)**: Khai báo lớp `lop`, hàm khởi tạo `khoi_tao`, kế thừa `ke_thua`, và tham chiếu `ban_than` (this/self).
- **Thư viện hàm chuẩn tích hợp (Built-in)**: Toán học (`can_bac_hai`, `luy_thua`, `lam_tron`), Xử lý chuỗi (`viet_hoa`, `cat_chuoi`, `noi_chuoi`), Mảng & Dictionary, I/O & Tệp tin (`doc_tep`, `ghi_tep`), Thời gian & Ngẫu nhiên.
- **Môi trường dòng lệnh CLI & REPL tương tác**: Chạy mã nguồn trực tiếp hoặc mở terminal gõ code tương tác từng dòng.

---

## 📦 Cấu Trúc Dự Án

```text
vpp/
├── vpp.py                      # Trình chạy chính (Runner)
├── vpp_cli.py                  # Giao diện dòng lệnh CLI & REPL
├── README.md                   # Tài liệu tổng quan
├── huong_dan_su_dung.md        # Hướng dẫn chi tiết cú pháp & ví dụ
├── vpp_core/                   # Lõi ngôn ngữ V++
│   ├── tokens.py               # Định nghĩa Token & Bảng từ khóa
│   ├── lexer.py                # Bộ phân tích từ vựng (Lexer)
│   ├── ast_nodes.py            # Cây cú pháp trừu tượng (AST)
│   ├── parser.py               # Bộ phân tích cú pháp (Parser)
│   ├── objects.py              # Hệ thống kiểu dữ liệu & Runtime Objects
│   ├── environment.py          # Quản lý phạm vi (Scope & Environment)
│   ├── builtins.py             # Thư viện hàm có sẵn (Standard Library)
│   ├── evaluator.py            # Trình thông dịch AST (Interpreter)
│   └── transpiler.py           # Trình biên dịch sang Python 3
├── examples/                   # Các chương trình mẫu (.vpp)
│   ├── 01_chao_the_gioi.vpp
│   ├── 02_tinh_toan_va_dieu_kien.vpp
│   ├── 03_vong_lap_va_danh_sach.vpp
│   ├── 04_ham_va_de_quy.vpp
│   ├── 05_huong_doi_tuong.vpp
│   ├── 06_thuat_toan_sap_xep.vpp
│   ├── 07_xu_ly_loi_va_tep.vpp
│   └── 08_mini_game_doan_so.vpp
└── tests/                      # Bộ kiểm thử tự động (Unit & Integration Tests)
    ├── test_all.py
    ├── test_advanced.py
    └── run_tests.py
```

---

## 💻 Cách Cài Đặt & Sử Dụng

### 1. Yêu cầu môi trường
- Python 3.10 trở lên. Không cần cài thêm thư viện bên ngoài (Zero Dependencies).

### 2. Các câu lệnh cơ bản

```bash
# 1. Chạy một tệp mã nguồn V++ (.vpp)
python3 vpp.py examples/01_chao_the_gioi.vpp

# 2. Chạy với chế độ biên dịch tối ưu (Transpiler)
python3 vpp.py -t examples/06_thuat_toan_sap_xep.vpp

# 3. Chạy trực tiếp một dòng lệnh V++
python3 vpp.py -c 'in("Xin chao ngon ngu V++!");'

# 4. Biên dịch tệp .vpp sang .py thuần
python3 vpp.py bien_dich examples/05_huong_doi_tuong.vpp -o tai_khoan.py

# 5. Mở môi trường REPL tương tác
python3 vpp.py
```

### 3. Chạy kiểm thử tự động (Test Suite)
```bash
python3 tests/run_tests.py
```

---

## 📖 Bảng Tra Cứu Từ Khóa (Keywords)

| Từ khóa V++ | Ý nghĩa tương đương | Ví dụ |
| :--- | :--- | :--- |
| `bien` | Khai báo biến | `bien x = 10;` |
| `hang` | Khai báo hằng số | `hang PI = 3.14;` |
| `neu` | Điều kiện if | `neu (x > 5) { ... }` |
| `khong_thi_neu` / `hoac_neu` | Điều kiện else if | `khong_thi_neu (x == 5) { ... }` |
| `khong_thi` / `nguoc_lai` | Điều kiện else | `khong_thi { ... }` |
| `khi` / `lap_khi` | Vòng lặp while | `khi (i < 10) { i++; }` |
| `lap` / `cho` ... `trong` | Vòng lặp for-in | `lap (pt trong danh_sach) { ... }` |
| `dung_lap` / `dung` / `ngat` | Thoát vòng lặp (break) | `dung_lap;` |
| `tiep_tuc` | Bước sang vòng lặp kế (continue) | `tiep_tuc;` |
| `ham` | Khai báo hàm | `ham tinh_tong(a, b) { tra_ve a + b; }` |
| `tra_ve` | Trả về giá trị (return) | `tra_ve ket_qua;` |
| `lop` | Khai báo lớp (class) | `lop HocSinh { ... }` |
| `ke_thua` | Kế thừa lớp (extends) | `lop HocSinh ke_thua Nguoi { ... }` |
| `khoi_tao` | Hàm tạo (constructor) | `khoi_tao(ten, tuoi) { ... }` |
| `ban_than` | Tham chiếu đối tượng (this/self) | `ban_than.ten = ten;` |
| `thu` | Bắt đầu khối try | `thu { ... }` |
| `bat_loi` | Bắt ngoại lệ catch | `bat_loi (loi) { ... }` |
| `cuoi_cung` | Khối finally | `cuoi_cung { ... }` |
| `nem_loi` | Ném ngoại lệ throw | `nem_loi "Mau so bang 0";` |
| `dung` / `sai` | Boolean true / false | `bien ok = dung;` |
| `rong` / `null` | Giá trị rỗng (None/null) | `bien res = rong;` |
| `va` / `&&` | Phép AND logic | `neu (a > 0 va b > 0) { ... }` |
| `hoac` / `||` | Phép OR logic | `neu (a == 0 hoac b == 0) { ... }` |
| `phu_dinh` / `!` | Phép NOT logic | `neu (phu_dinh tim_thay) { ... }` |
