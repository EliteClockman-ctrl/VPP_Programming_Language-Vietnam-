# HƯỚNG DẪN CÚ PHÁP VÀ LẬP TRÌNH V++ (.vpp)

Tài liệu này cung cấp hướng dẫn toàn diện từ cơ bản đến nâng cao để lập trình với ngôn ngữ **V++**.

---

## 1. Cú Pháp Cơ Bản

### 1.1. Chú thích (Comments)
```vpp
// Day la chu thich 1 dong
# Day cung la chu thich 1 dong

/*
 Day la chu thich
 tren nhieu dong
*/
```

### 1.2. Biến và Hằng số
- Sử dụng `bien` để khai báo biến có thể gán lại giá trị.
- Sử dụng `hang` để khai báo hằng số (bắt buộc khởi tạo và không thể sửa đổi).
- Dấu chấm phẩy `;` là tùy chọn khi xuống dòng.

```vpp
bien ten = "Gia Binh";
bien tuoi = 14;
bien diem_so = 9.75;
bien da_tot_nghiep = sai;

hang TRUONG_HOC = "THCS";
hang SO_MAX = 1000;
```

---

## 2. Các Kiểu Dữ Liệu

| Kiểu dữ liệu | Tên kiểu (`kieu()`) | Ví dụ |
| :--- | :--- | :--- |
| Số (Integer/Float) | `"so"` | `100`, `3.14159`, `-25` |
| Chuỗi ký tự | `"chuoi"` | `"Xin chao"`, `'V++'` |
| Đúng / Sai | `"dung_sai"` | `dung`, `sai` |
| Rỗng / Null | `"rong"` | `rong`, `null` |
| Danh sách (List) | `"danh_sach"` | `[1, 2, "ba", dung]` |
| Từ điển (Dictionary) | `"tu_dien"` | `{"ten": "Binh", "tuoi": 14}` |
| Hàm | `"ham"` | `ham(a, b) { tra_ve a + b; }` |
| Lớp / Đối tượng | `"lop"` / `"doi_tuong"` | `lop Xe { ... }` |

---

## 3. Toán Tử

- **Số học**: `+`, `-`, `*`, `/`, `%` (chia lấy dư), `^` hoặc `**` (lũy thừa).
- **Tăng / Giảm**: `x++`, `x--`, `++x`, `--x`.
- **Gán kết hợp**: `+=`, `-=`, `*=`, `/=`, `%=`.
- **So sánh**: `==`, `!=`, `<`, `<=`, `>`, `>=`.
- **Logic**: `va` hoặc `&&`, `hoac` hoặc `||`, `phu_dinh` hoặc `!`.

---

## 4. Cấu Trúc Điều Khiển

### 4.1. Rẽ nhánh `neu ... khong_thi_neu ... khong_thi`
```vpp
bien diem = 8.5;

neu (diem >= 9.0) {
    in("Xuat sac");
} khong_thi_neu (diem >= 8.0) {
    in("Gioi");
} khong_thi_neu (diem >= 6.5) {
    in("Kha");
} khong_thi {
    in("Trung binh");
}
```

### 4.2. Vòng lặp `khi` (While)
```vpp
bien dem = 1;
khi (dem <= 5) {
    in("Lan lap thu:", dem);
    dem++;
}
```

### 4.3. Vòng lặp `lap ... trong` (For-in)
```vpp
// Lap qua danh sach
bien danh_sach_ten = ["An", "Binh", "Cuong", "Dung"];
lap (ten trong danh_sach_ten) {
    in("Xin chao:", ten);
}

// Lap qua day so bang pham_vi(dau, cuoi, buoc)
lap (i trong pham_vi(1, 10, 2)) {
    in("So le:", i); // 1, 3, 5, 7, 9
}
```

---

## 5. Hàm (Functions) & Đệ Quy

```vpp
// Dinh nghia ham
ham tinh_tong(a, b) {
    tra_ve a + b;
}

// Ham de quy tinh giai thua
ham giai_thua(n) {
    neu (n <= 1) {
        tra_ve 1;
    }
    tra_ve n * giai_thua(n - 1);
}

in("Tong 15 + 27 =", tinh_tong(15, 27));
in("Giai thua cua 6! =", giai_thua(6));
```

---

## 6. Lập Trình Hướng Đối Tượng (OOP)

```vpp
// 1. Khai bao lop co ban
lop DongVat {
    khoi_tao(ten, tieng_keu) {
        ban_than.ten = ten;
        ban_than.tieng_keu = tieng_keu;
    }

    ham phat_am() {
        in(ban_than.ten, "phat ra tieng:", ban_than.tieng_keu);
    }
}

// 2. Ke thua lop
lop Cho ke_thua DongVat {
    khoi_tao(ten, giong_cho) {
        ban_than.ten = ten;
        ban_than.tieng_keu = "Gau Gau";
        ban_than.giong_cho = giong_cho;
    }

    ham sua() {
        ban_than.phat_am();
        in("Giong cho:", ban_than.giong_cho);
    }
}

bien chu_cho = Cho("Milu", "Shiba Inu");
chu_cho.sua();
```

---

## 7. Xử Lý Ngoại Lệ (Try-Catch)

```vpp
thu {
    bien a = 10;
    bien b = 0;
    neu (b == 0) {
        nem_loi "Khong the chia cho so 0!";
    }
    bien c = a / b;
} bat_loi (loi) {
    in("[Loi xu ly]:", loi);
} cuoi_cung {
    in("Khoi cuoi cung luon duoc thuc hien.");
}
```

---

## 8. Bảng Tra Cứu Thư Viện Chuẩn (Built-in Functions)

| Hàm | Cú pháp | Mô tả |
| :--- | :--- | :--- |
| **I/O** | `in(...)` / `xuat(...)` | In các giá trị có xuống dòng |
| | `in_lien(...)` | In các giá trị không xuống dòng |
| | `nhap("Thong bao")` | Nhập chuỗi từ bàn phím |
| **Kiểu** | `kieu(x)` | Trả về tên kiểu dữ liệu |
| | `chuoi(x)`, `so_nguyen(x)`, `so_thuc(x)` | Ép kiểu dữ liệu |
| | `do_dai(x)` | Trả về độ dài chuỗi, mảng, dict |
| **Mảng** | `them(ds, x)` | Thêm phần tử vào cuối danh sách |
| | `chen(ds, vi_tri, x)` | Chèn phần tử vào vị trí chỉ định |
| | `xoa(ds, [vi_tri])` | Xóa và lấy phần tử ra khỏi danh sách |
| | `chua(tap_hop, x)` | Kiểm tra phần tử có nằm trong tập hợp |
| | `dao_nguoc(ds)` | Đảo ngược danh sách / chuỗi |
| | `sap_xep(ds, [giam_dan])` | Sắp xếp danh sách tăng/giảm dần |
| | `pham_vi(dau, cuoi, buoc)` | Sinh danh sách số |
| **Chuỗi** | `noi_chuoi(ds, ky_tu)` | Nối các phần tử mảng thành chuỗi |
| | `cat_chuoi(s, ky_tu)` | Tách chuỗi thành danh sách |
| | `viet_hoa(s)`, `viet_thuong(s)` | Chuyển đổi chữ hoa / thường |
| **Từ điển**| `lay_khoa(tu_dien)` | Lấy danh sách các khóa |
| | `lay_gia_tri(tu_dien)` | Lấy danh sách các giá trị |
| **Toán học**| `can_bac_hai(x)`, `luy_thua(a, b)` | Căn bậc 2, lũy thừa |
| | `tri_tuyet_doi(x)`, `lam_tron(x, d)` | Giá trị tuyệt đối, làm tròn số |
| | `so_lon_nhat(...)`, `so_nho_nhat(...)`| Tìm giá trị lớn nhất / nhỏ nhất |
| | `tong(...)` | Tính tổng các số trong danh sách |
| | `sin(x)`, `cos(x)`, `tan(x)`, `PI`, `E` | Lượng giác và hằng số toán học |
| **Ngẫu nhiên**| `so_ngau_nhien(min, max)` | Sinh số nguyên ngẫu nhiên |
| | `ngau_nhien_thuc()` | Sinh số thực ngẫu nhiên [0, 1) |
| | `chon_ngau_nhien(ds)` | Chọn ngẫu nhiên 1 phần tử |
| **Tệp tin** | `doc_tep(duong_dan)` | Đọc toàn bộ nội dung tệp tin |
| | `ghi_tep(duong_dan, noi_dung)` | Ghi mới nội dung vào tệp |
| | `them_tep(duong_dan, noi_dung)` | Ghi nối tiếp nội dung vào tệp |
| | `kiem_tra_tep(duong_dan)` | Kiểm tra tệp có tồn tại không |
| **Hệ thống**| `thoi_gian_hien_tai()` | Lấy timestamp thời gian hiện tại |
| | `ngu(so_giay)` | Tạm dừng chương trình trong n giây |
| | `lenh("cau_lenh_shell")` | Thực thi lệnh hệ điều hành |
