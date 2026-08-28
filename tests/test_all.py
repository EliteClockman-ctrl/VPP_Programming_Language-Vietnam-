"""
V++ Comprehensive Unit and Integration Test Suite
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from vpp_core.lexer import Lexer, LexerError
from vpp_core.parser import Parser, ParserError
from vpp_core.evaluator import Interpreter
from vpp_core.objects import (
    VppNumber, VppString, VppBoolean, VppNull, VppList, VppDict,
    VppRuntimeError, VPP_DUNG, VPP_SAI, VPP_RONG
)
from vpp_core.transpiler import Transpiler

def run_vpp(code: str):
    lexer = Lexer(code, filename="<test>")
    tokens = lexer.tokenize()
    parser = Parser(tokens, filename="<test>")
    ast = parser.parse()
    interpreter = Interpreter(base_dir=".")
    return interpreter.eval(ast)

class TestVppCore(unittest.TestCase):
    def test_arithmetic(self):
        code = """
        bien a = 10 + 5 * 2;
        bien b = (10 + 5) * 2;
        bien c = 2 ^ 3;
        bien d = 17 % 5;
        bien e = 10 / 4;
        """
        run_vpp(code)

    def test_variables_and_constants(self):
        code = """
        bien x = 10;
        x = 20;
        hang PI = 3.14;
        """
        run_vpp(code)

        # Test constant reassignment error
        const_fail_code = """
        hang MAX = 100;
        MAX = 200;
        """
        with self.assertRaises(VppRuntimeError):
            run_vpp(const_fail_code)

    def test_if_else(self):
        code = """
        bien diem = 8.5;
        bien xep_loai = "";
        neu (diem >= 9.0) {
            xep_loai = "Xuat sac";
        } khong_thi_neu (diem >= 8.0) {
            xep_loai = "Gioi";
        } khong_thi {
            xep_loai = "Trung binh";
        }
        """
        run_vpp(code)

    def test_while_loop(self):
        code = """
        bien i = 0;
        bien tong = 0;
        khi (i <= 10) {
            tong += i;
            i++;
        }
        """
        run_vpp(code)

    def test_for_in_loop(self):
        code = """
        bien ds = [1, 2, 3, 4, 5];
        bien tong = 0;
        lap (x trong ds) {
            tong += x;
        }
        """
        run_vpp(code)

    def test_functions_and_recursion(self):
        code = """
        ham fibonacci(n) {
            neu (n <= 1) {
                tra_ve n;
            }
            tra_ve fibonacci(n - 1) + fibonacci(n - 2);
        }
        bien f7 = fibonacci(7); // 13
        """
        run_vpp(code)

    def test_lists_and_dicts(self):
        code = """
        bien ds = [10, 20, 30];
        them(ds, 40);
        bien phan_tu_dau = ds[0];
        bien cat_lat = ds[1:3];

        bien tu_dien_sv = {
            "ten": "Binh",
            "tuoi": 15,
            "diem": 9.5
        };
        bien ten_sv = tu_dien_sv["ten"];
        tu_dien_sv["lop"] = "8A";
        """
        run_vpp(code)

    def test_oop(self):
        code = """
        lop Nguoi {
            khoi_tao(ten, tuoi) {
                ban_than.ten = ten;
                ban_than.tuoi = tuoi;
            }

            ham gioi_thieu() {
                tra_ve "Toi la " + ban_than.ten + ", " + chuoi(ban_than.tuoi) + " tuoi";
            }
        }

        lop HocSinh ke_thua Nguoi {
            khoi_tao(ten, tuoi, lop_hoc) {
                ban_than.ten = ten;
                ban_than.tuoi = tuoi;
                ban_than.lop_hoc = lop_hoc;
            }

            ham lay_thong_tin() {
                tra_ve ban_than.gioi_thieu() + ", hoc lop " + ban_than.lop_hoc;
            }
        }

        bien hs = HocSinh("Gia Binh", 14, "8A1");
        bien info = hs.lay_thong_tin();
        """
        run_vpp(code)

    def test_try_catch(self):
        code = """
        bien da_bat_loi = sai;
        bien da_chay_finally = sai;
        thu {
            nem_loi "Loi mo phong";
        } bat_loi (e) {
            da_bat_loi = dung;
        } cuoi_cung {
            da_chay_finally = dung;
        }
        """
        run_vpp(code)

    def test_builtins_math_and_string(self):
        code = """
        bien can = can_bac_hai(16); // 4
        bien lt = luy_thua(2, 3); // 8
        bien tt = tri_tuyet_doi(-15); // 15
        bien s = viet_hoa("xin chao"); // "XIN CHAO"
        bien ds_tach = cat_chuoi("a,b,c", ",");
        bien chuoi_noi = noi_chuoi(["mot", "hai", "ba"], " - ");
        """
        run_vpp(code)

    def test_transpiler(self):
        code = """
        bien x = 5;
        bien y = 10;
        bien z = x * y + 2;
        ham tinh_tong(a, b) {
            tra_ve a + b;
        }
        bien kq = tinh_tong(z, 100);
        """
        lexer = Lexer(code, filename="<transpile_test>")
        tokens = lexer.tokenize()
        parser = Parser(tokens, filename="<transpile_test>")
        ast = parser.parse()
        transpiler = Transpiler()
        py_code = transpiler.transpile(ast)
        # Execute generated python code
        scope = {}
        exec(py_code, scope)
        self.assertEqual(scope["kq"], 152)

if __name__ == "__main__":
    unittest.main()
