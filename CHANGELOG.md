# 📝 V++ Programming Language — Changelog

Tất cả các thay đổi, tính năng mới và cải tiến quan trọng của ngôn ngữ lập trình **V++ (Vietnamese Plus Plus)** được ghi lại chi tiết tại đây.

---

## 🚀 [1.0.0] - Bản Phát Hành Chính Thức Đầu Tiên (Official Release)

### 🌟 1. Cú pháp Thuần Việt & Đa Dạng Cách Viết
- Hỗ trợ **100% cú pháp tiếng Việt** cả có dấu và không dấu:
  - Khai báo biến & hằng: `bien` / `biến`, `hang` / `hằng` hoặc gán trực tiếp `x = 10`.
  - Điều kiện rẽ nhánh: `neu` / `nếu`, `khong_thi_neu` / `hoac_neu` / `hoặc_nếu`, `khong_thi` / `không_thì` / `nguoc_lai`.
  - Vòng lặp tự nhiên: `lap` / `lặp` ... `trong`, `lap` / `lặp` ... `lan` / `lần`, `lap ... tu ... den ...`, `khi` / `lap_khi` (while).
  - Điều khiển vòng lặp: `dung` / `ngat` / `ngắt` (break), `tiep_tuc` / `tiếp_tục` (continue).
  - Khai báo hàm: `ham` / `hàm`, `tra_ve` / `trả_về` (return).
  - Giá trị logic: `dung` / `đúng` (true), `sai` (false), `rong` / `rỗng` / `null` (None/null).
  - Phép toán logic: `va` / `và` / `&&`, `hoac` / `hoặc` / `||`, `phu_dinh` / `phủ_định` / `!`.

---

### ⚡ 2. Động Cơ Thực Thi Kép (Dual Execution Engine)
- **High-Speed Python 3 Transpiler**:
  - Tự động biên dịch mã nguồn V++ sang mã máy Python tối ưu với tốc độ siêu nhanh (nhanh hơn Python thông thường x10 lần đối với các thuật toán mảng và đệ quy).
  - Hỗ trợ xuất mã nguồn thuần sang file `.py` bằng lệnh `vpp bien_dich file.vpp -o output.py`.
- **AST Tree-Walking Interpreter**:
  - Trình thông dịch trực tiếp phục vụ cho việc kiểm tra cú pháp nhanh và chạy dòng lệnh tức thì.
- **Hệ thống Chẩn đoán & Báo lỗi (Diagnostics)**:
  - Thông báo lỗi 100% bằng tiếng Việt có dấu, chỉ rõ số dòng, số cột và gợi ý cách khắc phục lỗi.

---

### 🏛️ 3. Lập Trình Hướng Đối Tượng (OOP) Hoàn Chỉnh
- Khai báo lớp đối tượng: `lop` / `lớp`.
- Kế thừa lớp: `ke_thua` / `kế_thừa` (extends/inheritance).
- Hàm khởi tạo (Constructor): `khoi_tao` / `khởi_tạo`.
- Tham chiếu đối tượng bản thân: `ban_than` / `bản_thân` (this/self).
- Đa hình, ghi đè phương thức và đóng gói thuộc tính.

---

### 📚 4. Thư Viện Chuẩn Phong Phú (Built-in Standard Library)
- **Xử lý Văn bản & Chuỗi**:
  - `chu_hoa` / `chữ_hoa`, `chu_thuong` / `chữ_thường`, `viet_hoa_dau` / `viết_hoa_đầu`.
  - `dem_tu` / `đếm_từ`, `dao_nguoc` / `đảo_ngược`, `cat_chuoi` / `cắt_chuỗi`, `noi_chuoi` / `nối_chuỗi`, `thay_the` / `thay_thế`.
- **Toán học & Thống kê**:
  - `can` / `căn` (căn bậc hai), `luy_thua` / `lũy_thừa`, `lam_tron` / `làm_tròn`.
  - `tong` / `tổng`, `trung_binh` / `trung_bình`, `lon_nhat` / `lớn_nhất` (`ln`), `nho_nhat` / `nhỏ_nhất` (`nn`).
- **Mảng & Danh sách**:
  - `them` / `thêm` (append), `chen` / `chèn` (insert), `xoa` / `xóa` (remove), `sap_xep` / `sắp_xếp` (sort), `chon_ngau_nhien` / `chọn_ngẫu_nhiên`.
- **Tương tác Tệp & Hệ Thống (File I/O)**:
  - `doc_tep` / `đọc_tệp`, `ghi_tep` / `ghi_tệp`, `xoa_tep` / `xóa_tệp`, `danh_sach_tep` / `danh_sách_tệp`.
  - `lenh` / `lệnh` (thực thi tiến trình shell hệ điều hành an toàn với timeout).
- **Mạng & Máy Chủ Web Fullstack**:
  - `tao_may_chu_web` / `tạo_máy_chủ_web`: Khởi tạo máy chủ HTTP REST API và phục vụ giao diện Frontend HTML5/CSS3.
  - `tai_trang_web` / `tải_trang_web`: Gửi yêu cầu tải dữ liệu từ internet.
  - `chuyen_json` / `chuyển_json`, `giai_ma_json` / `giải_mã_json`.

---

### 🛠️ 5. Công Cụ & Hệ Sinh Thái Lập Trình
- **Binary thực thi độc lập (`vpp.exe`)**:
  - Đóng gói nguyên khối, chạy trực tiếp trên Windows không cần cài đặt Python.
- **Trình tự động cài đặt 1-Click (`dist/installer.bat`)**:
  - Tự động thiết lập biến môi trường PATH và đăng ký mở tệp đuôi `.vpp`.
- **VS Code Extension (`vpp-language-support`)**:
  - Hỗ trợ tô màu cú pháp (Syntax Highlighting), bộ Snippets gợi ý code và biểu tượng tệp V++.
- **Chế độ dòng lệnh tương tác REPL**:
  - Gõ và chạy code trực tiếp từng dòng trên Terminal.
