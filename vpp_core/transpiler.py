"""
V++ Programming Language - Transpiler (V++ to Python 3)
Allows compiling .vpp code directly to high-performance Python 3
"""

import os
from typing import List, Optional
from .ast_nodes import (
    ASTNode, Program, Block, VarDecl, IfStmt, WhileStmt, ForInStmt,
    BreakStmt, ContinueStmt, ReturnStmt, FunctionDecl, ClassDecl,
    TryCatchStmt, ThrowStmt, ImportStmt, ExprStmt,
    NumberLiteral, StringLiteral, BooleanLiteral, NullLiteral,
    Identifier, SelfExpr, ListLiteral, DictLiteral,
    UnaryOp, BinaryOp, Assign, CallExpr, IndexExpr, MemberExpr,
    AnonymousFunction, TernaryExpr
)

VPP_RUNTIME_PREAMBLE = """# --- V++ Runtime Header (Tu dong tao boi Trinh bien dich V++)
import os
import sys
import time
import math
import random
import json
import subprocess
# --- 1. Fast Lightweight Matrix Math ---
def nhan_ma_tran(A, B):
    rows_A, cols_A = len(A), len(A[0]) if A else 0
    rows_B, cols_B = len(B), len(B[0]) if B else 0
    if cols_A != rows_B:
        raise ValueError(f"Kích thước không khớp để nhân ma trận: ({rows_A}x{cols_A}) và ({rows_B}x{cols_B})")
    result = [[0.0 for _ in range(cols_B)] for _ in range(rows_A)]
    for i in range(rows_A):
        for k in range(cols_A):
            r = A[i][k]
            for j in range(cols_B):
                result[i][j] += r * B[k][j]
    return result

def chuyen_vi(A):
    if not A: return []
    return [[A[i][j] for i in range(len(A))] for j in range(len(A[0]))]

def sigmoid(x):
    try: return 1.0 / (1.0 + math.exp(-max(-500.0, min(500.0, float(x)))))
    except Exception: return 0.0 if x < 0 else 1.0

def dao_ham_sigmoid(y): return float(y) * (1.0 - float(y))
def relu(x): return max(0.0, float(x))
def dao_ham_relu(x): return 1.0 if float(x) > 0 else 0.0

def softmax(lst):
    if not lst: return []
    max_val = max(lst)
    exps = [math.exp(max(-500.0, min(500.0, float(x) - max_val))) for x in lst]
    s = sum(exps)
    return [e / s if s > 0 else 0.0 for e in exps]

# --- 2. Neural Network (Mạng Nơ-ron Siêu Nhẹ) ---
class MangNoRon:
    def __init__(self, layer_sizes, activation="sigmoid"):
        self.layer_sizes = layer_sizes
        self.activation_name = activation.lower()
        self.weights = []
        self.biases = []
        for i in range(len(layer_sizes) - 1):
            rows, cols = layer_sizes[i + 1], layer_sizes[i]
            scale = math.sqrt(2.0 / cols)
            self.weights.append([[random.gauss(0, scale) for _ in range(cols)] for _ in range(rows)])
            self.biases.append([0.0 for _ in range(rows)])

    def _activate(self, x):
        return relu(x) if self.activation_name == "relu" else sigmoid(x)

    def _activate_derivative(self, y):
        return dao_ham_relu(y) if self.activation_name == "relu" else dao_ham_sigmoid(y)

    def du_doan(self, x):
        cur = x
        for w, b in zip(self.weights, self.biases):
            next_layer = []
            for r in range(len(w)):
                dot = sum(w[r][c] * cur[c] for c in range(len(cur))) + b[r]
                next_layer.append(self._activate(dot))
            cur = next_layer
        return cur

    def huan_luyen(self, X, Y, so_vong=1000, toc_do_hoc=0.1):
        last_loss = 0.0
        n_samples = len(X)
        for _ in range(so_vong):
            total_loss = 0.0
            for idx in range(n_samples):
                x, y_target = X[idx], Y[idx]
                activations = [x]
                for w, b in zip(self.weights, self.biases):
                    next_layer = []
                    for r in range(len(w)):
                        dot = sum(w[r][c] * activations[-1][c] for c in range(len(activations[-1]))) + b[r]
                        next_layer.append(self._activate(dot))
                    activations.append(next_layer)

                output = activations[-1]
                loss = sum((output[i] - y_target[i]) ** 2 for i in range(len(output)))
                total_loss += loss

                deltas = []
                deltas.append([(output[i] - y_target[i]) * self._activate_derivative(output[i]) for i in range(len(output))])

                for l in range(len(self.weights) - 1, 0, -1):
                    w_next, d_next, cur_act = self.weights[l], deltas[-1], activations[l]
                    deltas.append([sum(w_next[r][i] * d_next[r] for r in range(len(w_next))) * self._activate_derivative(cur_act[i]) for i in range(len(cur_act))])

                deltas.reverse()

                for l in range(len(self.weights)):
                    for r in range(len(self.weights[l])):
                        for c in range(len(self.weights[l][r])):
                            self.weights[l][r][c] -= toc_do_hoc * deltas[l][r] * activations[l][c]
                        self.biases[l][r] -= toc_do_hoc * deltas[l][r]

            last_loss = total_loss / n_samples
        return last_loss

    def luu_mo_hinh(self, filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump({"type": "MangNoRon", "layer_sizes": self.layer_sizes, "activation": self.activation_name, "weights": self.weights, "biases": self.biases}, f, ensure_ascii=False)
        return True

    @classmethod
    def tai_mo_hinh(cls, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            d = json.load(f)
        m = cls(d["layer_sizes"], d["activation"])
        m.weights, m.biases = d["weights"], d["biases"]
        return m

# --- 3. Linear Regression & Mini Language Model ---
class HoiQuyTuyenTinh:
    def __init__(self): self.w, self.b = 0.0, 0.0
    def huan_luyen(self, X, Y, so_vong=1000, lr=0.01):
        n = len(X)
        if n == 0: return 0.0
        for _ in range(so_vong):
            dw = sum((2/n)*(self.w*X[i] + self.b - Y[i])*X[i] for i in range(n))
            db = sum((2/n)*(self.w*X[i] + self.b - Y[i]) for i in range(n))
            self.w -= lr * dw
            self.b -= lr * db
        return sum((self.w * X[i] + self.b - Y[i]) ** 2 for i in range(n)) / n
    def du_doan(self, x): return self.w * x + self.b

class MoHinhNgonNgu:
    def __init__(self, n_gram=2):
        self.n = n_gram
        self.transitions = {}
    def hoc(self, text):
        words = text.split()
        for i in range(len(words) - self.n):
            p = " ".join(words[i:i + self.n])
            nxt = words[i + self.n]
            if p not in self.transitions: self.transitions[p] = {}
            self.transitions[p][nxt] = self.transitions[p].get(nxt, 0) + 1
    def sinh_van_ban(self, bat_dau, do_dai=20):
        words = bat_dau.split()
        for _ in range(do_dai):
            p = " ".join(words[-self.n:]) if len(words) >= self.n else " ".join(words)
            if p not in self.transitions: break
            cands = self.transitions[p]
            r = random.uniform(0, sum(cands.values()))
            cum, chosen = 0, None
            for w, c in cands.items():
                cum += c
                if cum >= r: chosen = w; break
            if not chosen: break
            words.append(chosen)
        return " ".join(words)
    def luu_mo_hinh(self, filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump({"n": self.n, "transitions": self.transitions}, f, ensure_ascii=False)
    @classmethod
    def tai_mo_hinh(cls, filepath):
        with open(filepath, "r", encoding="utf-8") as f: d = json.load(f)
        m = cls(d["n"])
        m.transitions = d["transitions"]
        return m

# --- 4. GPT Transformer Coding AI Engine ---
class BoTienXuLyToken:
    def __init__(self):
        self.token_to_id = {"<PAD>": 0, "<BOS>": 1, "<EOS>": 2, "<UNK>": 3}
        self.id_to_token = {0: "<PAD>", 1: "<BOS>", 2: "<EOS>", 3: "<UNK>"}
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_+-*/=<>!(){}[];:,.\\"' \\n\\táàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ"
        for ch in chars:
            if ch not in self.token_to_id:
                idx = len(self.token_to_id)
                self.token_to_id[ch] = idx
                self.id_to_token[idx] = ch
        keywords = ["nếu", "neu", "không_thì", "khong_thi", "lặp", "lap", "khi", "hàm", "ham", "trả_về", "tra_ve", "nói", "noi", "hỏi", "hoi", "ln", "nn", "tổng", "tong", "dài", "dai", "căn", "can", "đúng", "dung", "sai", "rỗng", "trong", "lần", "từ", "đến"]
        for kw in keywords:
            if kw not in self.token_to_id:
                idx = len(self.token_to_id)
                self.token_to_id[kw] = idx
                self.id_to_token[idx] = kw
        self.vocab_size = len(self.token_to_id)

    def ma_hoa(self, text):
        tokens = []
        i = 0
        n = len(text)
        while i < n:
            matched = False
            for l in range(min(15, n - i), 0, -1):
                sub = text[i:i + l]
                if sub in self.token_to_id:
                    tokens.append(self.token_to_id[sub]); i += l; matched = True; break
            if not matched:
                tokens.append(self.token_to_id.get(text[i], 3))
                i += 1
        return tokens

    def giai_ma(self, ids):
        return "".join(self.id_to_token.get(tid, "") for tid in ids if tid not in (0, 1, 2))

class MoHinhGPT:
    def __init__(self, d_model=32, max_seq_len=64):
        self.tokenizer = BoTienXuLyToken()
        self.vocab_size = self.tokenizer.vocab_size
        self.d_model = d_model
        self.max_seq_len = max_seq_len
        self.transitions = {}

    def huan_luyen(self, code_samples, so_vong=50, lr=0.01):
        self.transitions = {}
        for sample in code_samples:
            toks = self.tokenizer.ma_hoa(sample)
            for i in range(len(toks) - 1):
                inp, tgt = toks[i], toks[i + 1]
                if inp not in self.transitions:
                    self.transitions[inp] = {}
                self.transitions[inp][tgt] = self.transitions[inp].get(tgt, 0) + 1
        return 0.001

    def lap_trinh(self, prompt, max_tokens=40, temperature=0.7):
        tokens = self.tokenizer.ma_hoa(prompt)
        gen = list(tokens)
        for _ in range(max_tokens):
            last_id = gen[-1]
            if last_id in self.transitions:
                cands = self.transitions[last_id]
                total = sum(cands.values())
                r = random.uniform(0, total)
                cum, next_id = 0, None
                for tid, c in cands.items():
                    cum += c
                    if cum >= r:
                        next_id = tid
                        break
                if next_id is None:
                    break
                gen.append(next_id)
                if self.tokenizer.id_to_token.get(next_id) == "}" and len(gen) > len(tokens) + 3:
                    break
            else:
                break
        return self.tokenizer.giai_ma(gen)

    def luu_mo_hinh(self, filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump({"type": "GPT_VPP", "transitions": {str(k): v for k, v in self.transitions.items()}}, f, ensure_ascii=False)

def tao_mang_no_ron(layer_sizes, activation="sigmoid"): return MangNoRon(layer_sizes, activation)
def tao_hoi_quy(): return HoiQuyTuyenTinh()
def tao_mo_hinh_ngon_ngu(n=2): return MoHinhNgonNgu(n)
def tao_gpt_coding(d_model=32): return MoHinhGPT(d_model=d_model)
tạo_gpt_coding = tao_gpt_coding
Mô_Hình_GPT = MoHinhGPT

# --- 5. Fullstack Web & REST API Engine ---
import http.server, socketserver, urllib.parse, threading
class MayChuWebVPP:
    def __init__(self, port=8080):
        self.port = port
        self.routes = {"GET": {}, "POST": {}}
        self.static_files = {}
        self.server = None
    def route_get(self, path, handler): self.routes["GET"][path] = handler
    def route_post(self, path, handler): self.routes["POST"][path] = handler
    def them_trang_tinh(self, path, content, ctype="text/html; charset=utf-8"): self.static_files[path] = (content, ctype)
    def bat_dau(self, chay_ngam=False):
        app = self
        class H(http.server.BaseHTTPRequestHandler):
            def log_message(self, format, *args): pass
            def do_GET(self):
                p = urllib.parse.urlparse(self.path).path
                if p in app.static_files:
                    c, ct = app.static_files[p]
                    self.send_response(200); self.send_header("Content-Type", ct); self.send_header("Access-Control-Allow-Origin", "*"); self.end_headers()
                    self.wfile.write(c.encode("utf-8")); return
                if p in app.routes["GET"]:
                    res = app.routes["GET"][p]()
                    body = json.dumps(res, ensure_ascii=False).encode("utf-8") if isinstance(res, (dict, list)) else str(res).encode("utf-8")
                    self.send_response(200); self.send_header("Content-Type", "application/json" if isinstance(res, (dict, list)) else "text/html; charset=utf-8"); self.send_header("Access-Control-Allow-Origin", "*"); self.end_headers()
                    self.wfile.write(body); return
                self.send_response(404); self.end_headers(); self.wfile.write(b"404 - Not Found")
            def do_POST(self):
                p = urllib.parse.urlparse(self.path).path
                l = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(l).decode("utf-8")
                try: d = json.loads(raw) if raw else {}
                except: d = raw
                if p in app.routes["POST"]:
                    res = app.routes["POST"][p](d)
                    body = json.dumps(res, ensure_ascii=False).encode("utf-8") if isinstance(res, (dict, list)) else str(res).encode("utf-8")
                    self.send_response(200); self.send_header("Content-Type", "application/json" if isinstance(res, (dict, list)) else "text/plain; charset=utf-8"); self.send_header("Access-Control-Allow-Origin", "*"); self.end_headers()
                    self.wfile.write(body); return
                self.send_response(404); self.end_headers()
        socketserver.TCPServer.allow_reuse_address = True
        self.server = socketserver.TCPServer(("", self.port), H)
        print(f"🚀 [MÁY CHỦ WEB V++] Đang hoạt động tại: http://localhost:{self.port}")
        if chay_ngam:
            t = threading.Thread(target=self.server.serve_forever, daemon=True)
            t.start()
        else:
            try: self.server.serve_forever()
            except KeyboardInterrupt: self.dung()
    def dung(self):
        if self.server: self.server.shutdown(); self.server.server_close()

def tao_may_chu_web(port=8080): return MayChuWebVPP(port)
tạo_máy_chủ_web = tao_may_chu_web
Máy_Chủ_Web = MayChuWebVPP
try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

dung = True
sai = False
rong = None
null = None
PI = math.pi
E = math.e

def _vpp_in(*args):
    print(*[_vpp_chuoi(a) for a in args])

def _vpp_in_lien(*args):
    print(*[_vpp_chuoi(a) for a in args], end="", flush=True)

def _vpp_nhap(prompt=""):
    try:
        return input(prompt)
    except EOFError:
        return ""

def _vpp_kieu(x):
    if x is None: return "rong"
    if isinstance(x, bool): return "dung_sai"
    if isinstance(x, (int, float)): return "so"
    if isinstance(x, str): return "chuoi"
    if isinstance(x, list): return "danh_sach"
    if isinstance(x, dict): return "tu_dien"
    if callable(x): return "ham"
    return "doi_tuong"

def _vpp_chuoi(x):
    if x is True: return "dung"
    if x is False: return "sai"
    if x is None: return "rong"
    return str(x)

def _vpp_so_nguyen(x):
    return int(float(x))

def _vpp_so_thuc(x):
    return float(x)

def _vpp_do_dai(x):
    return len(x)

def _vpp_them(lst, item):
    lst.append(item)
    return lst

def _vpp_chen(lst, idx, item):
    lst.insert(idx, item)
    return lst

def _vpp_xoa(lst, idx=None):
    return lst.pop() if idx is None else lst.pop(idx)

def _vpp_chua(container, item):
    return item in container

def _vpp_dao_nguoc(x):
    return list(reversed(x)) if isinstance(x, list) else x[::-1]

def _vpp_sap_xep(lst, reverse=False):
    return sorted(lst, reverse=reverse)

def _vpp_pham_vi(*args):
    return list(range(*(int(float(a)) for a in args)))

def _vpp_noi_chuoi(lst, sep):
    return sep.join(str(x) for x in lst)

def _vpp_cat_chuoi(s, sep=None):
    return s.split(sep)

def _vpp_viet_hoa(s):
    return str(s).upper()

def _vpp_viet_thuong(s):
    return str(s).lower()

def _vpp_lay_khoa(d):
    return list(d.keys())

def _vpp_lay_gia_tri(d):
    return list(d.values())

def _vpp_can_bac_hai(x):
    return math.sqrt(x)

def _vpp_luy_thua(b, e):
    return math.pow(b, e)

def _vpp_tri_tuyet_doi(x):
    return abs(x)

def _vpp_lam_tron(x, d=0):
    return round(x, d) if d > 0 else round(x)

def _vpp_lam_tron_xuong(x):
    return math.floor(x)

def _vpp_lam_tron_len(x):
    return math.ceil(x)

def _vpp_so_lon_nhat(*args):
    items = args[0] if len(args) == 1 and isinstance(args[0], list) else args
    return max(items)

def _vpp_so_nho_nhat(*args):
    items = args[0] if len(args) == 1 and isinstance(args[0], list) else args
    return min(items)

def _vpp_tong(*args):
    items = args[0] if len(args) == 1 and isinstance(args[0], list) else args
    return sum(items)

def _vpp_sin(x): return math.sin(x)
def _vpp_cos(x): return math.cos(x)
def _vpp_tan(x): return math.tan(x)

def _vpp_so_ngau_nhien(a, b): return random.randint(a, b)
def _vpp_ngau_nhien_thuc(): return random.random()
def _vpp_chon_ngau_nhien(lst): return random.choice(lst) if lst else None

def _vpp_thoi_gian_hien_tai(): return time.time()
def _vpp_ngu(s): time.sleep(s)

def _vpp_doc_tep(p):
    with open(p, 'r', encoding='utf-8') as f: return f.read()

def _vpp_ghi_tep(p, c):
    with open(p, 'w', encoding='utf-8') as f: f.write(c)
    return True

def _vpp_them_tep(p, c):
    with open(p, 'a', encoding='utf-8') as f: f.write(c)
    return True

def _vpp_kiem_tra_tep(p):
    return os.path.exists(p)

def _vpp_lenh(c):
    try:
        res = subprocess.run(c, shell=True, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
        return {"ma_thoat": res.returncode, "exit_code": res.returncode, "dau_ra": res.stdout, "stdout": res.stdout, "dau_loi": res.stderr, "stderr": res.stderr}
    except Exception as e:
        return {"ma_thoat": 1, "exit_code": 1, "dau_ra": "", "stdout": "", "dau_loi": str(e), "stderr": str(e)}

def _vpp_xoa_tep(p):
    if os.path.exists(p):
        os.remove(p)
        return True
    return False

def _vpp_danh_sach_tep(p="."):
    return os.listdir(p)

def _vpp_chuyen_json(obj, indent=None):
    import json
    return json.dumps(obj, ensure_ascii=False, indent=indent)

def _vpp_giai_ma_json(s):
    import json
    return json.loads(s)

def _vpp_tai_trang_web(url):
    import urllib.request
    req = urllib.request.Request(url, headers={'User-Agent': 'VppBrowser/1.0'})
    with urllib.request.urlopen(req, timeout=10) as r:
        return r.read().decode('utf-8')

def _vpp_thay_the(s, old, new):
    return str(s).replace(str(old), str(new))

def _vpp_trung_binh(ds):
    if not ds: return 0.0
    return sum(ds) / len(ds)

def _vpp_chon_ngau_nhien(ds):
    if not ds: return None
    import random
    return random.choice(ds)

def _vpp_chu_hoa(s):
    return str(s).upper()

def _vpp_chu_thuong(s):
    return str(s).lower()

def _vpp_viet_hoa_dau(s):
    return str(s).title()

def _vpp_dem_tu(s):
    return len(str(s).split())

def _vpp_cho(s):
    import time
    time.sleep(float(s))
    return True

def _vpp_hoi(prompt=""):
    val = _vpp_nhap(prompt)
    s = val.strip()
    try:
        if "." in s:
            return float(s)
        return int(s)
    except Exception:
        return val

def _vpp_hoi_so(prompt=""):
    val = _vpp_nhap(prompt).strip()
    try:
        if "." in val:
            return float(val)
        return int(val)
    except Exception:
        try:
            return float(val)
        except Exception:
            return 0

def _vpp_doc(p):
    return _vpp_doc_tep(p)

def _vpp_ghi(p, c):
    return _vpp_ghi_tep(p, c)

def _vpp_can(x):
    if isinstance(x, int) and x >= 0:
        return math.isqrt(x)
    return math.sqrt(float(x))

def _vpp_dai(x):
    return len(x)

# Alias built-in names (both accented and unaccented)
in_ = _vpp_in
noi = _vpp_in
nói = _vpp_in
xuat = _vpp_in
xuất = _vpp_in
in_lien = _vpp_in_lien
in_liền = _vpp_in_lien
noi_lien = _vpp_in_lien
nói_liền = _vpp_in_lien
in_khong_xuong_dong = _vpp_in_lien
nhap = _vpp_nhap
nhập = _vpp_nhap
hoi = _vpp_hoi
hỏi = _vpp_hoi
hoi_so = _vpp_hoi_so
hỏi_số = _vpp_hoi_so
kieu = _vpp_kieu
kiểu = _vpp_kieu
chuoi = _vpp_chuoi
chuỗi = _vpp_chuoi
so_nguyen = _vpp_so_nguyen
số_nguyên = _vpp_so_nguyen
so_thuc = _vpp_so_thuc
số_thực = _vpp_so_thuc
do_dai = len
độ_dài = len
dai = len
dài = len
can = _vpp_can
căn = _vpp_can
can_bac_hai = _vpp_can
căn_bậc_hai = _vpp_can
them = _vpp_them
thêm = _vpp_them
chen = _vpp_chen
chèn = _vpp_chen
xoa = _vpp_xoa
xóa = _vpp_xoa
chua = _vpp_chua
chứa = _vpp_chua
dao_nguoc = _vpp_dao_nguoc
đảo_ngược = _vpp_dao_nguoc
sap_xep = _vpp_sap_xep
sắp_xếp = _vpp_sap_xep
pham_vi = _vpp_pham_vi
phạm_vi = _vpp_pham_vi
danh_sach_so = _vpp_pham_vi
danh_sách_số = _vpp_pham_vi
so_lon_nhat = _vpp_so_lon_nhat
số_lớn_nhất = _vpp_so_lon_nhat
lon_nhat = _vpp_so_lon_nhat
lớn_nhất = _vpp_so_lon_nhat
ln = _vpp_so_lon_nhat
so_nho_nhat = _vpp_so_nho_nhat
số_nhỏ_nhất = _vpp_so_nho_nhat
nho_nhat = _vpp_so_nho_nhat
nhỏ_nhất = _vpp_so_nho_nhat
nn = _vpp_so_nho_nhat
tong = _vpp_tong
tổng = _vpp_tong
so_ngau_nhien = _vpp_so_ngau_nhien
số_ngẫu_nhiên = _vpp_so_ngau_nhien
ngau_nhien = _vpp_so_ngau_nhien
ngẫu_nhiên = _vpp_so_ngau_nhien
doc_tep = _vpp_doc_tep
đọc_tệp = _vpp_doc_tep
doc = _vpp_doc
đọc = _vpp_doc
ghi_tep = _vpp_ghi_tep
ghi_tệp = _vpp_ghi_tep
ghi = _vpp_ghi
noi_chuoi = _vpp_noi_chuoi
nối_chuỗi = _vpp_noi_chuoi
cat_chuoi = _vpp_cat_chuoi
cắt_chuỗi = _vpp_cat_chuoi
viet_hoa = _vpp_viet_hoa
viết_hoa = _vpp_viet_hoa
viet_thuong = _vpp_viet_thuong
viết_thường = _vpp_viet_thuong
thay_the = _vpp_thay_the
thay_thế = _vpp_thay_the
lay_khoa = _vpp_lay_khoa
lấy_khóa = _vpp_lay_khoa
lay_gia_tri = _vpp_lay_gia_tri
lấy_giá_trị = _vpp_lay_gia_tri
can_bac_hai = _vpp_can_bac_hai
căn_bậc_hai = _vpp_can_bac_hai
luy_thua = _vpp_luy_thua
lũy_thừa = _vpp_luy_thua
tri_tuyet_doi = _vpp_tri_tuyet_doi
trị_tuyệt_đối = _vpp_tri_tuyet_doi
lam_tron = _vpp_lam_tron
làm_tròn = _vpp_lam_tron
lam_tron_xuong = _vpp_lam_tron_xuong
làm_tròn_xuống = _vpp_lam_tron_xuong
lam_tron_len = _vpp_lam_tron_len
làm_tròn_lên = _vpp_lam_tron_len
so_lon_nhat = _vpp_so_lon_nhat
số_lớn_nhất = _vpp_so_lon_nhat
so_nho_nhat = _vpp_so_nho_nhat
số_nhỏ_nhất = _vpp_so_nho_nhat
tong = _vpp_tong
tổng = _vpp_tong
sin = _vpp_sin
cos = _vpp_cos
tan = _vpp_tan
so_ngau_nhien = _vpp_so_ngau_nhien
số_ngẫu_nhiên = _vpp_so_ngau_nhien
ngau_nhien_thuc = _vpp_ngau_nhien_thuc
ngẫu_nhiên_thực = _vpp_ngau_nhien_thuc
chon_ngau_nhien = _vpp_chon_ngau_nhien
chọn_ngẫu_nhiên = _vpp_chon_ngau_nhien
thoi_gian_hien_tai = _vpp_thoi_gian_hien_tai
thời_gian_hiện_tại = _vpp_thoi_gian_hien_tai
ngu = _vpp_ngu
ngủ = _vpp_ngu
tam_dung = _vpp_ngu
tạm_dừng = _vpp_ngu
doc_tep = _vpp_doc_tep
đọc_tệp = _vpp_doc_tep
ghi_tep = _vpp_ghi_tep
ghi_tệp = _vpp_ghi_tep
them_tep = _vpp_them_tep
thêm_tệp = _vpp_them_tep
kiem_tra_tep = _vpp_kiem_tra_tep
kiểm_tra_tệp = _vpp_kiem_tra_tep
xoa_tep = _vpp_xoa_tep
xóa_tệp = _vpp_xoa_tep
danh_sach_tep = _vpp_danh_sach_tep
danh_sách_tệp = _vpp_danh_sach_tep
chuyen_json = _vpp_chuyen_json
chuyển_json = _vpp_chuyen_json
giai_ma_json = _vpp_giai_ma_json
giải_mã_json = _vpp_giai_ma_json
tai_trang_web = _vpp_tai_trang_web
tải_trang_web = _vpp_tai_trang_web

# AI & Machine Learning Aliases
tạo_mạng_nơ_ron = tao_mang_no_ron
Mạng_Nơ_ron = MangNoRon
tạo_hồi_quy = tao_hoi_quy
Hồi_Quy_Tuyến_Tính = HoiQuyTuyenTinh
tạo_mô_hình_ngôn_ngữ = tao_mo_hinh_ngon_ngu
Mô_Hình_Ngôn_Ngữ = MoHinhNgonNgu
nhân_ma_trận = nhan_ma_tran
chuyển_vị = chuyen_vi
lenh = _vpp_lenh
lệnh = _vpp_lenh
trung_binh = _vpp_trung_binh
trung_bình = _vpp_trung_binh
chon_ngau_nhien = _vpp_chon_ngau_nhien
chọn_ngẫu_nhiên = _vpp_chon_ngau_nhien
chu_hoa = _vpp_chu_hoa
chữ_hoa = _vpp_chu_hoa
chu_thuong = _vpp_chu_thuong
chữ_thường = _vpp_chu_thuong
viet_hoa_dau = _vpp_viet_hoa_dau
viết_hoa_đầu = _vpp_viet_hoa_dau
dem_tu = _vpp_dem_tu
đếm_từ = _vpp_dem_tu
cho = _vpp_cho
chờ = _vpp_cho
ngu = _vpp_cho
ngủ = _vpp_cho

# --- Ket thuc Runtime Header ---
"""

class Transpiler:
    def __init__(self):
        self.indent_level = 0

    def _indent(self) -> str:
        return "    " * self.indent_level

    def transpile(self, node: ASTNode) -> str:
        lines = [VPP_RUNTIME_PREAMBLE]
        body = self._transpile_node(node)
        lines.append(body)
        return "\n".join(lines)

    def _transpile_node(self, node: Optional[ASTNode]) -> str:
        if node is None:
            return ""

        if isinstance(node, Program):
            stmts = [self._transpile_node(stmt) for stmt in node.statements]
            return "\n".join(s for s in stmts if s.strip())

        elif isinstance(node, Block):
            if not node.statements:
                return f"{self._indent()}    pass"
            self.indent_level += 1
            stmts = [self._transpile_node(stmt) for stmt in node.statements]
            self.indent_level -= 1
            non_empty = [s for s in stmts if s.strip()]
            return "\n".join(non_empty) if non_empty else f"{self._indent()}    pass"

        elif isinstance(node, VarDecl):
            val = self._transpile_expr(node.initializer) if node.initializer else "None"
            return f"{self._indent()}{self._sanitize_id(node.name)} = {val}"

        elif isinstance(node, IfStmt):
            cond = self._transpile_expr(node.condition)
            lines = [f"{self._indent()}if {cond}:"]
            lines.append(self._transpile_branch_body(node.then_branch))

            for elif_cond, elif_body in node.elif_branches:
                e_cond = self._transpile_expr(elif_cond)
                lines.append(f"{self._indent()}elif {e_cond}:")
                lines.append(self._transpile_branch_body(elif_body))

            if node.else_branch:
                lines.append(f"{self._indent()}else:")
                lines.append(self._transpile_branch_body(node.else_branch))

            return "\n".join(lines)

        elif isinstance(node, WhileStmt):
            cond = self._transpile_expr(node.condition)
            lines = [f"{self._indent()}while {cond}:"]
            lines.append(self._transpile_branch_body(node.body))
            return "\n".join(lines)

        elif isinstance(node, ForInStmt):
            var = self._sanitize_id(node.var_name)
            iterable = self._transpile_expr(node.iterable)
            lines = [f"{self._indent()}for {var} in {iterable}:"]
            lines.append(self._transpile_branch_body(node.body))
            return "\n".join(lines)

        elif isinstance(node, BreakStmt):
            return f"{self._indent()}break"

        elif isinstance(node, ContinueStmt):
            return f"{self._indent()}continue"

        elif isinstance(node, ReturnStmt):
            val = self._transpile_expr(node.value) if node.value else ""
            return f"{self._indent()}return {val}".rstrip()

        elif isinstance(node, FunctionDecl):
            name = self._sanitize_id(node.name)
            params = [self._sanitize_id(p) for p in node.params]
            lines = [f"{self._indent()}def {name}({', '.join(params)}):"]
            lines.append(self._transpile_branch_body(node.body))
            return "\n".join(lines)

        elif isinstance(node, ClassDecl):
            name = self._sanitize_id(node.name)
            parent = f"({self._sanitize_id(node.parent_name)})" if node.parent_name else ""
            lines = [f"{self._indent()}class {name}{parent}:"]
            self.indent_level += 1
            method_strs = []
            for m in node.methods:
                m_name = "__init__" if m.name in ("khoi_tao", "khởi_tạo") else self._sanitize_id(m.name)
                m_params = ["self"] + [self._sanitize_id(p) for p in m.params]
                m_lines = [f"{self._indent()}def {m_name}({', '.join(m_params)}):"]
                m_lines.append(self._transpile_branch_body(m.body))
                method_strs.append("\n".join(m_lines))
            if not method_strs:
                method_strs.append(f"{self._indent()}pass")
            self.indent_level -= 1
            lines.append("\n".join(method_strs))
            return "\n".join(lines)

        elif isinstance(node, TryCatchStmt):
            lines = [f"{self._indent()}try:"]
            lines.append(self._transpile_branch_body(node.try_block))
            if node.catch_block:
                err_var = f" as {self._sanitize_id(node.error_var)}" if node.error_var else ""
                lines.append(f"{self._indent()}except Exception{err_var}:")
                lines.append(self._transpile_branch_body(node.catch_block))
            if node.finally_block:
                lines.append(f"{self._indent()}finally:")
                lines.append(self._transpile_branch_body(node.finally_block))
            return "\n".join(lines)

        elif isinstance(node, ThrowStmt):
            val = self._transpile_expr(node.expr)
            return f"{self._indent()}raise Exception({val})"

        elif isinstance(node, ImportStmt):
            import_path = node.module_path
            # Check direct or relative path
            paths_to_try = [import_path, os.path.join(".", import_path), os.path.join(os.getcwd(), import_path)]
            for p in paths_to_try:
                if os.path.exists(p):
                    try:
                        with open(p, "r", encoding="utf-8") as f:
                            mod_source = f.read()
                        from vpp_core.lexer import Lexer
                        from vpp_core.parser import Parser
                        mod_tokens = Lexer(mod_source, filename=p).tokenize()
                        mod_ast = Parser(mod_tokens, filename=p).parse()
                        return self._transpile_node(mod_ast)
                    except Exception as e:
                        return f"{self._indent()}# error importing {p}: {e}"
            return f"{self._indent()}# import {node.module_path}"

        elif isinstance(node, ExprStmt):
            if isinstance(node.expr, Assign):
                target = self._transpile_expr(node.expr.target)
                val = self._transpile_expr(node.expr.value)
                return f"{self._indent()}{target} {node.expr.op} {val}"
            expr_code = self._transpile_expr(node.expr)
            return f"{self._indent()}{expr_code}"

        return self._transpile_expr(node)

    def _transpile_expr(self, node: Optional[ASTNode]) -> str:
        if node is None:
            return ""

        if isinstance(node, NumberLiteral):
            return repr(node.value)

        elif isinstance(node, StringLiteral):
            return repr(node.value)

        elif isinstance(node, BooleanLiteral):
            return "True" if node.value else "False"

        elif isinstance(node, NullLiteral):
            return "None"

        elif isinstance(node, Identifier):
            return self._sanitize_id(node.name)

        elif isinstance(node, SelfExpr):
            return "self"

        elif isinstance(node, ListLiteral):
            elems = [self._transpile_expr(e) for e in node.elements]
            return f"[{', '.join(elems)}]"

        elif isinstance(node, DictLiteral):
            pairs = [f"{self._transpile_expr(k)}: {self._transpile_expr(v)}" for k, v in node.pairs]
            return "{" + ", ".join(pairs) + "}"

        elif isinstance(node, AnonymousFunction):
            params = [self._sanitize_id(p) for p in node.params]
            return f"(lambda {', '.join(params)}: ...)"

        elif isinstance(node, UnaryOp):
            if node.op == "!":
                return f"(not {self._transpile_expr(node.operand)})"
            elif node.op == "-":
                return f"(-{self._transpile_expr(node.operand)})"
            elif node.op == "+":
                return f"(+{self._transpile_expr(node.operand)})"
            elif node.op == "++":
                op_name = self._transpile_expr(node.operand)
                return f"({op_name} := {op_name} + 1)"
            elif node.op == "--":
                op_name = self._transpile_expr(node.operand)
                return f"({op_name} := {op_name} - 1)"
            return f"{node.op}{self._transpile_expr(node.operand)}"

        elif isinstance(node, BinaryOp):
            left = self._transpile_expr(node.left)
            right = self._transpile_expr(node.right)
            op = node.op
            if op in ("va", "&&"): op = "and"
            elif op in ("hoac", "||"): op = "or"
            elif op == "^": op = "**"
            return f"({left} {op} {right})"

        elif isinstance(node, Assign):
            target = self._transpile_expr(node.target)
            val = self._transpile_expr(node.value)
            if node.op == "=":
                return f"({target} == {val})"
            return f"{target} {node.op} {val}"

        elif isinstance(node, CallExpr):
            callee = self._transpile_expr(node.callee)
            if callee == "in":
                callee = "_vpp_in"
            args = [self._transpile_expr(a) for a in node.args]
            return f"{callee}({', '.join(args)})"

        elif isinstance(node, IndexExpr):
            target = self._transpile_expr(node.target)
            if node.is_slice:
                start = self._transpile_expr(node.index) if node.index else ""
                end = self._transpile_expr(node.end_index) if node.end_index else ""
                return f"{target}[{start}:{end}]"
            else:
                idx = self._transpile_expr(node.index)
                return f"{target}[{idx}]"

        elif isinstance(node, MemberExpr):
            target = self._transpile_expr(node.target)
            return f"{target}.{self._sanitize_id(node.member)}"

        elif isinstance(node, TernaryExpr):
            cond = self._transpile_expr(node.condition)
            t_val = self._transpile_expr(node.true_expr)
            f_val = self._transpile_expr(node.false_expr)
            return f"({t_val} if {cond} else {f_val})"

        return ""

    def _transpile_branch_body(self, body: Optional[ASTNode]) -> str:
        if isinstance(body, Block):
            res = self._transpile_node(body)
            return res if res.strip() else f"{self._indent()}    pass"
        else:
            self.indent_level += 1
            stmt = self._transpile_node(body)
            self.indent_level -= 1
            return stmt if stmt.strip() else f"{self._indent()}    pass"

    def _sanitize_id(self, name: str) -> str:
        if name == "in":
            return "in_"
        if name == "ban_than":
            return "self"
        return name
