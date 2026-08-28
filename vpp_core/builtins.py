"""
V++ Programming Language - Standard Library & Built-in Functions
All names in Vietnamese without accents (tieng Viet khong dau)
"""

import math
import time
import random
import os
import subprocess
from typing import List, Dict, Any
from .objects import (
    VppObject, VppNumber, VppString, VppBoolean, VppNull,
    VppList, VppDict, VppBuiltinFunction, VppRuntimeError,
    VPP_DUNG, VPP_SAI, VPP_RONG
)

def py_to_vpp(val: Any) -> VppObject:
    if val is None:
        return VPP_RONG
    if isinstance(val, bool):
        return VPP_DUNG if val else VPP_SAI
    if isinstance(val, (int, float)):
        return VppNumber(val)
    if isinstance(val, str):
        return VppString(val)
    if isinstance(val, list):
        return VppList([py_to_vpp(x) for x in val])
    if isinstance(val, dict):
        d = {}
        for k, v in val.items():
            d[py_to_vpp(k)] = py_to_vpp(v)
        return VppDict(d)
    if isinstance(val, VppObject):
        return val
    return VppString(str(val))

def vpp_to_py(obj: VppObject) -> Any:
    if isinstance(obj, VppNull):
        return None
    if isinstance(obj, VppBoolean):
        return obj.value
    if isinstance(obj, VppNumber):
        return obj.value
    if isinstance(obj, VppString):
        return obj.value
    if isinstance(obj, VppList):
        return [vpp_to_py(x) for x in obj.elements]
    if isinstance(obj, VppDict):
        return {vpp_to_py(k): vpp_to_py(v) for k, v in obj.pairs.items()}
    return obj

# Built-in implementations
def builtin_in(args: List[VppObject]) -> VppObject:
    out = " ".join(arg.to_string() for arg in args)
    print(out)
    return VPP_RONG

def builtin_in_lien(args: List[VppObject]) -> VppObject:
    out = " ".join(arg.to_string() for arg in args)
    print(out, end="", flush=True)
    return VPP_RONG

def builtin_nhap(args: List[VppObject]) -> VppObject:
    prompt = args[0].to_string() if args else ""
    try:
        val = input(prompt)
        return VppString(val)
    except EOFError:
        return VppString("")

def builtin_kieu(args: List[VppObject]) -> VppObject:
    if not args:
        raise VppRuntimeError("Ham 'kieu' yeu cau 1 doi so")
    return VppString(args[0].type_name())

def builtin_chuoi(args: List[VppObject]) -> VppObject:
    if not args:
        return VppString("")
    return VppString(args[0].to_string())

def builtin_so_nguyen(args: List[VppObject]) -> VppObject:
    if not args:
        return VppNumber(0)
    arg = args[0]
    try:
        if isinstance(arg, VppNumber):
            return VppNumber(int(arg.value))
        if isinstance(arg, VppString):
            return VppNumber(int(float(arg.value)))
        if isinstance(arg, VppBoolean):
            return VppNumber(1 if arg.value else 0)
        return VppNumber(0)
    except Exception:
        raise VppRuntimeError(f"Khong the chuyen '{arg.to_string()}' thanh so nguyen")

def builtin_so_thuc(args: List[VppObject]) -> VppObject:
    if not args:
        return VppNumber(0.0)
    arg = args[0]
    try:
        if isinstance(arg, VppNumber):
            return VppNumber(float(arg.value))
        if isinstance(arg, VppString):
            return VppNumber(float(arg.value))
        if isinstance(arg, VppBoolean):
            return VppNumber(1.0 if arg.value else 0.0)
        return VppNumber(0.0)
    except Exception:
        raise VppRuntimeError(f"Khong the chuyen '{arg.to_string()}' thanh so thuc")

def builtin_do_dai(args: List[VppObject]) -> VppObject:
    if not args:
        raise VppRuntimeError("Ham 'do_dai' yeu cau 1 doi so")
    arg = args[0]
    if isinstance(arg, VppString):
        return VppNumber(len(arg.value))
    if isinstance(arg, VppList):
        return VppNumber(len(arg.elements))
    if isinstance(arg, VppDict):
        return VppNumber(len(arg.pairs))
    raise VppRuntimeError(f"Doi tuong kieu '{arg.type_name()}' khong ho tro ham 'do_dai'")

def builtin_them(args: List[VppObject]) -> VppObject:
    if len(args) < 2:
        raise VppRuntimeError("Ham 'them' yeu cau 2 doi so (danh_sach, phan_tu)")
    lst = args[0]
    if not isinstance(lst, VppList):
        raise VppRuntimeError("Doi so dau tien cua 'them' phai la danh sach")
    lst.elements.append(args[1])
    return lst

def builtin_chen(args: List[VppObject]) -> VppObject:
    if len(args) < 3:
        raise VppRuntimeError("Ham 'chen' yeu cau 3 doi so (danh_sach, vi_tri, phan_tu)")
    lst = args[0]
    idx = args[1]
    if not isinstance(lst, VppList) or not isinstance(idx, VppNumber):
        raise VppRuntimeError("Sai kieu doi so trong ham 'chen'")
    lst.elements.insert(int(idx.value), args[2])
    return lst

def builtin_xoa(args: List[VppObject]) -> VppObject:
    if not args:
        raise VppRuntimeError("Ham 'xoa' yeu cau it nhat 1 doi so (danh_sach, [vi_tri])")
    lst = args[0]
    if not isinstance(lst, VppList):
        raise VppRuntimeError("Doi so dau tien cua 'xoa' phai la danh sach")
    if len(args) > 1:
        idx = args[1]
        if not isinstance(idx, VppNumber):
            raise VppRuntimeError("Vi tri xoa phai la so")
        i = int(idx.value)
        if 0 <= i < len(lst.elements):
            return lst.elements.pop(i)
        raise VppRuntimeError(f"Chi muc vuot ngoai pham vi: {i}")
    else:
        if lst.elements:
            return lst.elements.pop()
        raise VppRuntimeError("Danh sach rong, khong the xoa")

def builtin_chua(args: List[VppObject]) -> VppObject:
    if len(args) < 2:
        raise VppRuntimeError("Ham 'chua' yeu cau 2 doi so (tap_hop, phan_tu)")
    container = args[0]
    item = args[1]
    if isinstance(container, VppList):
        for elem in container.elements:
            if elem == item:
                return VPP_DUNG
        return VPP_SAI
    if isinstance(container, VppString):
        return VPP_DUNG if item.to_string() in container.value else VPP_SAI
    if isinstance(container, VppDict):
        return VPP_DUNG if item in container.pairs else VPP_SAI
    return VPP_SAI

def builtin_dao_nguoc(args: List[VppObject]) -> VppObject:
    if not args:
        raise VppRuntimeError("Ham 'dao_nguoc' yeu cau 1 doi so")
    arg = args[0]
    if isinstance(arg, VppList):
        return VppList(list(reversed(arg.elements)))
    if isinstance(arg, VppString):
        return VppString(arg.value[::-1])
    raise VppRuntimeError("Chi co the dao nguoc danh sach hoac chuoi")

def builtin_sap_xep(args: List[VppObject]) -> VppObject:
    if not args:
        raise VppRuntimeError("Ham 'sap_xep' yeu cau 1 danh sach")
    lst = args[0]
    if not isinstance(lst, VppList):
        raise VppRuntimeError("Ham 'sap_xep' chi ap dung cho danh sach")
    reverse = False
    if len(args) > 1:
        reverse = args[1].is_truthy()
    
    def sort_key(item: VppObject):
        if isinstance(item, VppNumber):
            return (0, item.value)
        if isinstance(item, VppString):
            return (1, item.value)
        return (2, str(item))

    sorted_elems = sorted(lst.elements, key=sort_key, reverse=reverse)
    return VppList(sorted_elems)

def builtin_pham_vi(args: List[VppObject]) -> VppObject:
    if not args:
        raise VppRuntimeError("Ham 'pham_vi' yeu cau it nhat 1 doi so")
    if len(args) == 1:
        start, end, step = 0, int(args[0].value), 1
    elif len(args) == 2:
        start, end, step = int(args[0].value), int(args[1].value), 1
    else:
        start, end, step = int(args[0].value), int(args[1].value), int(args[2].value)
    
    elems = [VppNumber(i) for i in range(start, end, step)]
    return VppList(elems)

def builtin_noi_chuoi(args: List[VppObject]) -> VppObject:
    if len(args) < 2:
        raise VppRuntimeError("Ham 'noi_chuoi' yeu cau 2 doi so (danh_sach, ky_tu_noi)")
    lst = args[0]
    sep = args[1].to_string()
    if not isinstance(lst, VppList):
        raise VppRuntimeError("Doi so dau tien phai la danh sach")
    return VppString(sep.join(x.to_string() for x in lst.elements))

def builtin_cat_chuoi(args: List[VppObject]) -> VppObject:
    if not args:
        raise VppRuntimeError("Ham 'cat_chuoi' yeu cau it nhat 1 chuoi")
    s = args[0].to_string()
    sep = args[1].to_string() if len(args) > 1 else None
    parts = s.split(sep)
    return VppList([VppString(p) for p in parts])

def builtin_viet_hoa(args: List[VppObject]) -> VppObject:
    if not args:
        return VppString("")
    return VppString(args[0].to_string().upper())

def builtin_viet_thuong(args: List[VppObject]) -> VppObject:
    if not args:
        return VppString("")
    return VppString(args[0].to_string().lower())

def builtin_lay_khoa(args: List[VppObject]) -> VppObject:
    if not args or not isinstance(args[0], VppDict):
        raise VppRuntimeError("Ham 'lay_khoa' yeu cau 1 tu dien")
    return VppList(list(args[0].pairs.keys()))

def builtin_lay_gia_tri(args: List[VppObject]) -> VppObject:
    if not args or not isinstance(args[0], VppDict):
        raise VppRuntimeError("Ham 'lay_gia_tri' yeu cau 1 tu dien")
    return VppList(list(args[0].pairs.values()))

# Math functions
def builtin_can_bac_hai(args: List[VppObject]) -> VppObject:
    if not args or not isinstance(args[0], VppNumber):
        raise VppRuntimeError("Ham 'can_bac_hai' yeu cau 1 so")
    if args[0].value < 0:
        raise VppRuntimeError("Khong the tinh can bac hai cua so am")
    return VppNumber(math.sqrt(args[0].value))

def builtin_luy_thua(args: List[VppObject]) -> VppObject:
    if len(args) < 2 or not isinstance(args[0], VppNumber) or not isinstance(args[1], VppNumber):
        raise VppRuntimeError("Ham 'luy_thua' yeu cau 2 so (co_so, so_mu)")
    return VppNumber(math.pow(args[0].value, args[1].value))

def builtin_tri_tuyet_doi(args: List[VppObject]) -> VppObject:
    if not args or not isinstance(args[0], VppNumber):
        raise VppRuntimeError("Ham 'tri_tuyet_doi' yeu cau 1 so")
    return VppNumber(abs(args[0].value))

def builtin_lam_tron(args: List[VppObject]) -> VppObject:
    if not args or not isinstance(args[0], VppNumber):
        raise VppRuntimeError("Ham 'lam_tron' yeu cau it nhat 1 so")
    digits = int(args[1].value) if len(args) > 1 and isinstance(args[1], VppNumber) else 0
    val = round(args[0].value, digits)
    return VppNumber(val if digits > 0 else int(val))

def builtin_lam_tron_xuong(args: List[VppObject]) -> VppObject:
    if not args or not isinstance(args[0], VppNumber):
        raise VppRuntimeError("Ham 'lam_tron_xuong' yeu cau 1 so")
    return VppNumber(math.floor(args[0].value))

def builtin_lam_tron_len(args: List[VppObject]) -> VppObject:
    if not args or not isinstance(args[0], VppNumber):
        raise VppRuntimeError("Ham 'lam_tron_len' yeu cau 1 so")
    return VppNumber(math.ceil(args[0].value))

def builtin_so_lon_nhat(args: List[VppObject]) -> VppObject:
    if not args:
        raise VppRuntimeError("Ham 'so_lon_nhat' yeu cau it nhat 1 doi so")
    if len(args) == 1 and isinstance(args[0], VppList):
        items = args[0].elements
    else:
        items = args
    if not items:
        raise VppRuntimeError("Khong co phan tu de tim so lon nhat")
    max_val = items[0]
    for item in items[1:]:
        if isinstance(item, VppNumber) and isinstance(max_val, VppNumber):
            if item.value > max_val.value:
                max_val = item
    return max_val

def builtin_so_nho_nhat(args: List[VppObject]) -> VppObject:
    if not args:
        raise VppRuntimeError("Ham 'so_nho_nhat' yeu cau it nhat 1 doi so")
    if len(args) == 1 and isinstance(args[0], VppList):
        items = args[0].elements
    else:
        items = args
    if not items:
        raise VppRuntimeError("Khong co phan tu de tim so nho nhat")
    min_val = items[0]
    for item in items[1:]:
        if isinstance(item, VppNumber) and isinstance(min_val, VppNumber):
            if item.value < min_val.value:
                min_val = item
    return min_val

def builtin_tong(args: List[VppObject]) -> VppObject:
    if not args:
        return VppNumber(0)
    if len(args) == 1 and isinstance(args[0], VppList):
        items = args[0].elements
    else:
        items = args
    total = 0
    for it in items:
        if isinstance(it, VppNumber):
            total += it.value
    return VppNumber(total)

# Random
def builtin_so_ngau_nhien(args: List[VppObject]) -> VppObject:
    if len(args) < 2:
        raise VppRuntimeError("Ham 'so_ngau_nhien' yeu cau 2 so (nho_nhat, lon_nhat)")
    a = int(args[0].value)
    b = int(args[1].value)
    return VppNumber(random.randint(a, b))

def builtin_ngau_nhien_thuc(args: List[VppObject]) -> VppObject:
    return VppNumber(random.random())

def builtin_chon_ngau_nhien(args: List[VppObject]) -> VppObject:
    if not args or not isinstance(args[0], VppList):
        raise VppRuntimeError("Ham 'chon_ngau_nhien' yeu cau 1 danh sach")
    lst = args[0].elements
    if not lst:
        return VPP_RONG
    return random.choice(lst)

# Time
def builtin_thoi_gian_hien_tai(args: List[VppObject]) -> VppObject:
    return VppNumber(time.time())

def builtin_ngu(args: List[VppObject]) -> VppObject:
    if not args or not isinstance(args[0], VppNumber):
        raise VppRuntimeError("Ham 'ngu' yeu cau so giay (so)")
    time.sleep(args[0].value)
    return VPP_RONG

# File IO
def builtin_doc_tep(args: List[VppObject]) -> VppObject:
    if not args:
        raise VppRuntimeError("Ham 'doc_tep' yeu cau duong dan tep")
    path = args[0].to_string()
    try:
        with open(path, "r", encoding="utf-8") as f:
            return VppString(f.read())
    except Exception as e:
        raise VppRuntimeError(f"Khong the doc tep '{path}': {str(e)}")

def builtin_ghi_tep(args: List[VppObject]) -> VppObject:
    if len(args) < 2:
        raise VppRuntimeError("Ham 'ghi_tep' yeu cau (duong_dan, noi_dung)")
    path = args[0].to_string()
    content = args[1].to_string()
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return VPP_DUNG
    except Exception as e:
        raise VppRuntimeError(f"Khong the ghi vao tep '{path}': {str(e)}")

def builtin_them_tep(args: List[VppObject]) -> VppObject:
    if len(args) < 2:
        raise VppRuntimeError("Ham 'them_tep' yeu cau (duong_dan, noi_dung)")
    path = args[0].to_string()
    content = args[1].to_string()
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(content)
        return VPP_DUNG
    except Exception as e:
        raise VppRuntimeError(f"Khong the them vao tep '{path}': {str(e)}")

def builtin_kiem_tra_tep(args: List[VppObject]) -> VppObject:
    if not args:
        return VPP_SAI
    path = args[0].to_string()
    return VPP_DUNG if os.path.exists(path) else VPP_SAI

# JSON
import json
import urllib.request

def builtin_chuyen_json(args: List[VppObject]) -> VppObject:
    if not args:
        return VppString("{}")
    py_obj = vpp_to_py(args[0])
    try:
        indent = int(args[1].value) if len(args) > 1 and isinstance(args[1], VppNumber) else None
        return VppString(json.dumps(py_obj, ensure_ascii=False, indent=indent))
    except Exception as e:
        raise VppRuntimeError(f"Loi chuyen doi sang JSON: {str(e)}")

def builtin_giai_ma_json(args: List[VppObject]) -> VppObject:
    if not args:
        raise VppRuntimeError("Ham 'giai_ma_json' yeu cau chuoi JSON")
    s = args[0].to_string()
    try:
        py_obj = json.loads(s)
        return py_to_vpp(py_obj)
    except Exception as e:
        raise VppRuntimeError(f"Loi giai ma JSON: {str(e)}")

# Web Request
def builtin_tai_trang_web(args: List[VppObject]) -> VppObject:
    if not args:
        raise VppRuntimeError("Ham 'tai_trang_web' yeu cau dia chi URL")
    url = args[0].to_string()
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'VppBrowser/1.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode('utf-8')
            return VppString(content)
    except Exception as e:
        raise VppRuntimeError(f"Loi tai trang web '{url}': {str(e)}")

def builtin_xoa_tep(args: List[VppObject]) -> VppObject:
    if not args:
        raise VppRuntimeError("Ham 'xoa_tep' yeu cau duong dan tep")
    path = args[0].to_string()
    try:
        if os.path.exists(path):
            os.remove(path)
            return VPP_DUNG
        return VPP_SAI
    except Exception as e:
        raise VppRuntimeError(f"Khong the xoa tep '{path}': {str(e)}")

def builtin_danh_sach_tep(args: List[VppObject]) -> VppObject:
    path = args[0].to_string() if args else "."
    try:
        files = os.listdir(path)
        return VppList([VppString(f) for f in files])
    except Exception as e:
        raise VppRuntimeError(f"Loi doc danh sach thu muc '{path}': {str(e)}")

def builtin_thay_the(args: List[VppObject]) -> VppObject:
    if len(args) < 3:
        raise VppRuntimeError("Ham 'thay_the' yeu cau (chuoi_goc, chuoi_tim, chuoi_thay)")
    s = args[0].to_string()
    old = args[1].to_string()
    new = args[2].to_string()
    return VppString(s.replace(old, new))

# System
def builtin_lenh(args: List[VppObject]) -> VppObject:
    if not args:
        raise VppRuntimeError("Ham 'lenh' yeu cau cau lenh shell")
    cmd = args[0].to_string()
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return VppString(res.stdout)
    except Exception as e:
        raise VppRuntimeError(f"Loi thuc thi lenh '{cmd}': {str(e)}")

def get_builtin_scope() -> Dict[str, VppObject]:
    builtins = {
        # I/O
        "in": VppBuiltinFunction("in", builtin_in),
        "noi": VppBuiltinFunction("noi", builtin_in),
        "nói": VppBuiltinFunction("nói", builtin_in),
        "xuat": VppBuiltinFunction("xuat", builtin_in),
        "xuất": VppBuiltinFunction("xuất", builtin_in),
        "in_lien": VppBuiltinFunction("in_lien", builtin_in_lien),
        "in_liền": VppBuiltinFunction("in_liền", builtin_in_lien),
        "noi_lien": VppBuiltinFunction("noi_lien", builtin_in_lien),
        "nói_liền": VppBuiltinFunction("nói_liền", builtin_in_lien),
        "in_khong_xuong_dong": VppBuiltinFunction("in_khong_xuong_dong", builtin_in_lien),
        "nhap": VppBuiltinFunction("nhap", builtin_nhap),
        "nhập": VppBuiltinFunction("nhập", builtin_nhap),
        
        # Types & Conversion
        "kieu": VppBuiltinFunction("kieu", builtin_kieu),
        "kiểu": VppBuiltinFunction("kiểu", builtin_kieu),
        "chuoi": VppBuiltinFunction("chuoi", builtin_chuoi),
        "chuỗi": VppBuiltinFunction("chuỗi", builtin_chuoi),
        "so_nguyen": VppBuiltinFunction("so_nguyen", builtin_so_nguyen),
        "số_nguyên": VppBuiltinFunction("số_nguyên", builtin_so_nguyen),
        "so_thuc": VppBuiltinFunction("so_thuc", builtin_so_thuc),
        "số_thực": VppBuiltinFunction("số_thực", builtin_so_thuc),
        "do_dai": VppBuiltinFunction("do_dai", builtin_do_dai),
        "độ_dài": VppBuiltinFunction("độ_dài", builtin_do_dai),
        
        # Lists & Collections
        "them": VppBuiltinFunction("them", builtin_them),
        "thêm": VppBuiltinFunction("thêm", builtin_them),
        "chen": VppBuiltinFunction("chen", builtin_chen),
        "chèn": VppBuiltinFunction("chèn", builtin_chen),
        "xoa": VppBuiltinFunction("xoa", builtin_xoa),
        "xóa": VppBuiltinFunction("xóa", builtin_xoa),
        "chua": VppBuiltinFunction("chua", builtin_chua),
        "chứa": VppBuiltinFunction("chứa", builtin_chua),
        "dao_nguoc": VppBuiltinFunction("dao_nguoc", builtin_dao_nguoc),
        "đảo_ngược": VppBuiltinFunction("đảo_ngược", builtin_dao_nguoc),
        "sap_xep": VppBuiltinFunction("sap_xep", builtin_sap_xep),
        "sắp_xếp": VppBuiltinFunction("sắp_xếp", builtin_sap_xep),
        "pham_vi": VppBuiltinFunction("pham_vi", builtin_pham_vi),
        "phạm_vi": VppBuiltinFunction("phạm_vi", builtin_pham_vi),
        "danh_sach_so": VppBuiltinFunction("danh_sach_so", builtin_pham_vi),
        "danh_sách_số": VppBuiltinFunction("danh_sách_số", builtin_pham_vi),
        "noi_chuoi": VppBuiltinFunction("noi_chuoi", builtin_noi_chuoi),
        "nối_chuỗi": VppBuiltinFunction("nối_chuỗi", builtin_noi_chuoi),
        "cat_chuoi": VppBuiltinFunction("cat_chuoi", builtin_cat_chuoi),
        "cắt_chuỗi": VppBuiltinFunction("cắt_chuỗi", builtin_cat_chuoi),
        "viet_hoa": VppBuiltinFunction("viet_hoa", builtin_viet_hoa),
        "viết_hoa": VppBuiltinFunction("viết_hoa", builtin_viet_hoa),
        "viet_thuong": VppBuiltinFunction("viet_thuong", builtin_viet_thuong),
        "viết_thường": VppBuiltinFunction("viết_thường", builtin_viet_thuong),
        "thay_the": VppBuiltinFunction("thay_the", builtin_thay_the),
        "thay_thế": VppBuiltinFunction("thay_thế", builtin_thay_the),
        
        # Dict
        "lay_khoa": VppBuiltinFunction("lay_khoa", builtin_lay_khoa),
        "lấy_khóa": VppBuiltinFunction("lấy_khóa", builtin_lay_khoa),
        "lay_gia_tri": VppBuiltinFunction("lay_gia_tri", builtin_lay_gia_tri),
        "lấy_giá_trị": VppBuiltinFunction("lấy_giá_trị", builtin_lay_gia_tri),
        
        # Math
        "can_bac_hai": VppBuiltinFunction("can_bac_hai", builtin_can_bac_hai),
        "căn_bậc_hai": VppBuiltinFunction("căn_bậc_hai", builtin_can_bac_hai),
        "luy_thua": VppBuiltinFunction("luy_thua", builtin_luy_thua),
        "lũy_thừa": VppBuiltinFunction("lũy_thừa", builtin_luy_thua),
        "tri_tuyet_doi": VppBuiltinFunction("tri_tuyet_doi", builtin_tri_tuyet_doi),
        "trị_tuyệt_đối": VppBuiltinFunction("trị_tuyệt_đối", builtin_tri_tuyet_doi),
        "lam_tron": VppBuiltinFunction("lam_tron", builtin_lam_tron),
        "làm_tròn": VppBuiltinFunction("làm_tròn", builtin_lam_tron),
        "lam_tron_xuong": VppBuiltinFunction("lam_tron_xuong", builtin_lam_tron_xuong),
        "làm_tròn_xuống": VppBuiltinFunction("làm_tròn_xuống", builtin_lam_tron_xuong),
        "lam_tron_len": VppBuiltinFunction("lam_tron_len", builtin_lam_tron_len),
        "làm_tròn_lên": VppBuiltinFunction("làm_tròn_lên", builtin_lam_tron_len),
        "so_lon_nhat": VppBuiltinFunction("so_lon_nhat", builtin_so_lon_nhat),
        "số_lớn_nhất": VppBuiltinFunction("số_lớn_nhất", builtin_so_lon_nhat),
        "lon_nhat": VppBuiltinFunction("lon_nhat", builtin_so_lon_nhat),
        "lớn_nhất": VppBuiltinFunction("lớn_nhất", builtin_so_lon_nhat),
        "ln": VppBuiltinFunction("ln", builtin_so_lon_nhat),
        "so_nho_nhat": VppBuiltinFunction("so_nho_nhat", builtin_so_nho_nhat),
        "số_nhỏ_nhất": VppBuiltinFunction("số_nhỏ_nhất", builtin_so_nho_nhat),
        "nho_nhat": VppBuiltinFunction("nho_nhat", builtin_so_nho_nhat),
        "nhỏ_nhất": VppBuiltinFunction("nhỏ_nhất", builtin_so_nho_nhat),
        "nn": VppBuiltinFunction("nn", builtin_so_nho_nhat),
        "tong": VppBuiltinFunction("tong", builtin_tong),
        "tổng": VppBuiltinFunction("tổng", builtin_tong),
        "hoi": VppBuiltinFunction("hoi", builtin_nhap),
        "hỏi": VppBuiltinFunction("hỏi", builtin_nhap),
        "hoi_so": VppBuiltinFunction("hoi_so", builtin_nhap),
        "hỏi_số": VppBuiltinFunction("hỏi_số", builtin_nhap),
        "doc": VppBuiltinFunction("doc", builtin_doc_tep),
        "đọc": VppBuiltinFunction("đọc", builtin_doc_tep),
        "ghi": VppBuiltinFunction("ghi", builtin_ghi_tep),
        "sin": VppBuiltinFunction("sin", lambda args: VppNumber(math.sin(args[0].value))),
        "cos": VppBuiltinFunction("cos", lambda args: VppNumber(math.cos(args[0].value))),
        "tan": VppBuiltinFunction("tan", lambda args: VppNumber(math.tan(args[0].value))),
        "PI": VppNumber(math.pi),
        "E": VppNumber(math.e),
        
        # Random
        "so_ngau_nhien": VppBuiltinFunction("so_ngau_nhien", builtin_so_ngau_nhien),
        "số_ngẫu_nhiên": VppBuiltinFunction("số_ngẫu_nhiên", builtin_so_ngau_nhien),
        "ngau_nhien_thuc": VppBuiltinFunction("ngau_nhien_thuc", builtin_ngau_nhien_thuc),
        "ngẫu_nhiên_thực": VppBuiltinFunction("ngẫu_nhiên_thực", builtin_ngau_nhien_thuc),
        "chon_ngau_nhien": VppBuiltinFunction("chon_ngau_nhien", builtin_chon_ngau_nhien),
        "chọn_ngẫu_nhiên": VppBuiltinFunction("chọn_ngẫu_nhiên", builtin_chon_ngau_nhien),
        
        # Time
        "thoi_gian_hien_tai": VppBuiltinFunction("thoi_gian_hien_tai", builtin_thoi_gian_hien_tai),
        "thời_gian_hiện_tại": VppBuiltinFunction("thời_gian_hiện_tại", builtin_thoi_gian_hien_tai),
        "ngu": VppBuiltinFunction("ngu", builtin_ngu),
        "ngủ": VppBuiltinFunction("ngủ", builtin_ngu),
        "tam_dung": VppBuiltinFunction("tam_dung", builtin_ngu),
        "tạm_dừng": VppBuiltinFunction("tạm_dừng", builtin_ngu),
        
        # File IO
        "doc_tep": VppBuiltinFunction("doc_tep", builtin_doc_tep),
        "đọc_tệp": VppBuiltinFunction("đọc_tệp", builtin_doc_tep),
        "ghi_tep": VppBuiltinFunction("ghi_tep", builtin_ghi_tep),
        "ghi_tệp": VppBuiltinFunction("ghi_tệp", builtin_ghi_tep),
        "them_tep": VppBuiltinFunction("them_tep", builtin_them_tep),
        "thêm_tệp": VppBuiltinFunction("thêm_tệp", builtin_them_tep),
        "kiem_tra_tep": VppBuiltinFunction("kiem_tra_tep", builtin_kiem_tra_tep),
        "kiểm_tra_tệp": VppBuiltinFunction("kiểm_tra_tệp", builtin_kiem_tra_tep),
        "xoa_tep": VppBuiltinFunction("xoa_tep", builtin_xoa_tep),
        "xóa_tệp": VppBuiltinFunction("xóa_tệp", builtin_xoa_tep),
        "danh_sach_tep": VppBuiltinFunction("danh_sach_tep", builtin_danh_sach_tep),
        "danh_sách_tệp": VppBuiltinFunction("danh_sách_tệp", builtin_danh_sach_tep),
        
        # JSON & Web
        "chuyen_json": VppBuiltinFunction("chuyen_json", builtin_chuyen_json),
        "chuyển_json": VppBuiltinFunction("chuyển_json", builtin_chuyen_json),
        "giai_ma_json": VppBuiltinFunction("giai_ma_json", builtin_giai_ma_json),
        "giải_mã_json": VppBuiltinFunction("giải_mã_json", builtin_giai_ma_json),
        "tai_trang_web": VppBuiltinFunction("tai_trang_web", builtin_tai_trang_web),
        "tải_trang_web": VppBuiltinFunction("tải_trang_web", builtin_tai_trang_web),
        
        # System
        "lenh": VppBuiltinFunction("lenh", builtin_lenh),
        "lệnh": VppBuiltinFunction("lệnh", builtin_lenh),
    }
    return builtins
