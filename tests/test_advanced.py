"""
V++ Advanced Test Suite - Algorithms, Data Structures, OOP, Modules
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from vpp_core import run_code
from vpp_core.objects import VppNumber, VppString, VppList, VppDict, VPP_DUNG, VPP_SAI

class TestVppAdvanced(unittest.TestCase):
    def test_quicksort_algorithm(self):
        code = """
        ham quicksort(arr) {
            neu (do_dai(arr) <= 1) {
                tra_ve arr;
            }
            bien chot = arr[0];
            bien nho_hon = [];
            bien bang = [];
            bien lon_hon = [];

            lap (x trong arr) {
                neu (x < chot) {
                    them(nho_hon, x);
                } khong_thi_neu (x == chot) {
                    them(bang, x);
                } khong_thi {
                    them(lon_hon, x);
                }
            }

            tra_ve quicksort(nho_hon) + bang + quicksort(lon_hon);
        }

        bien mang_chua_sap_xep = [64, 34, 25, 12, 22, 11, 90];
        bien mang_da_sap_xep = quicksort(mang_chua_sap_xep);
        """
        res = run_code(code)

    def test_binary_search(self):
        code = """
        ham tim_nhi_phan(arr, target) {
            bien trai = 0;
            bien phai = do_dai(arr) - 1;

            khi (trai <= phai) {
                bien giua = so_nguyen((trai + phai) / 2);
                neu (arr[giua] == target) {
                    tra_ve giua;
                } khong_thi_neu (arr[giua] < target) {
                    trai = giua + 1;
                } khong_thi {
                    phai = giua - 1;
                }
            }
            tra_ve -1;
        }

        bien ds = [10, 20, 30, 40, 50, 60, 70];
        bien vi_tri = tim_nhi_phan(ds, 40); // 3
        """
        run_code(code)

    def test_bank_account_oop(self):
        code = """
        lop TaiKhoanNganHang {
            khoi_tao(chu_tai_khoan, so_du_ban_dau) {
                ban_than.chu_tai_khoan = chu_tai_khoan;
                ban_than.so_du = so_du_ban_dau;
                ban_than.lich_su = [];
            }

            ham nap_tien(so_tien) {
                neu (so_tien <= 0) {
                    nem_loi "So tien nap phai lon hon 0";
                }
                ban_than.so_du += so_tien;
                them(ban_than.lich_su, "+ " + chuoi(so_tien));
                tra_ve ban_than.so_du;
            }

            ham rut_tien(so_tien) {
                neu (so_tien > ban_than.so_du) {
                    nem_loi "So du khong du";
                }
                ban_than.so_du -= so_tien;
                them(ban_than.lich_su, "- " + chuoi(so_tien));
                tra_ve ban_than.so_du;
            }

            ham lay_so_du() {
                tra_ve ban_than.so_du;
            }
        }

        bien tk = TaiKhoanNganHang("Vuong Gia Binh", 1000000);
        tk.nap_tien(500000);
        tk.rut_tien(200000);
        bien so_du_cuoi = tk.lay_so_du(); // 1300000
        """
        run_code(code)

    def test_file_io_and_persistence(self):
        import tempfile
        tmp_file = os.path.join(tempfile.gettempdir(), "test_vpp_io.txt").replace("\\", "/")
        code = f"""
        bien duong_dan = "{tmp_file}";
        ghi_tep(duong_dan, "Xin chao tu V++\\nDong 2");
        them_tep(duong_dan, "\\nDong 3 them vao");
        bien noi_dung = doc_tep(duong_dan);
        bien ton_tai = kiem_tra_tep(duong_dan);
        """
        run_code(code)

    def test_matrix_operations(self):
        code = """
        ham tao_ma_tran(so_dong, cot, gia_tri_mac_dinh) {
            bien mt = [];
            lap (i trong pham_vi(so_dong)) {
                bien dong = [];
                lap (j trong pham_vi(cot)) {
                    them(dong, gia_tri_mac_dinh);
                }
                them(mt, dong);
            }
            tra_ve mt;
        }

        bien m = tao_ma_tran(3, 3, 0);
        m[0][0] = 1;
        m[1][1] = 1;
        m[2][2] = 1;
        """
        run_code(code)

if __name__ == "__main__":
    unittest.main()
