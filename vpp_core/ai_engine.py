"""
================================================================================
  V++ Programming Language — Ultra-Lightweight Built-in AI Engine
  Module Trí Tuệ Nhân Tạo & Học Máy Siêu Nhẹ (Zero-Dependency AI, < 100KB)
================================================================================
"""

import math
import random
import json
import os
from typing import List, Dict, Any, Optional

# --- 1. Fast Lightweight Matrix Math ---

def nhan_ma_tran(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
    """Nhân 2 ma trận A và B (A x B)"""
    rows_A = len(A)
    cols_A = len(A[0]) if rows_A > 0 else 0
    rows_B = len(B)
    cols_B = len(B[0]) if rows_B > 0 else 0

    if cols_A != rows_B:
        raise ValueError(f"Kích thước không khớp để nhân ma trận: ({rows_A}x{cols_A}) và ({rows_B}x{cols_B})")

    result = [[0.0 for _ in range(cols_B)] for _ in range(rows_A)]
    for i in range(rows_A):
        for k in range(cols_A):
            r = A[i][k]
            for j in range(cols_B):
                result[i][j] += r * B[k][j]
    return result

def chuyen_vi(A: List[List[float]]) -> List[List[float]]:
    """Chuyển vị ma trận A^T"""
    if not A:
        return []
    rows = len(A)
    cols = len(A[0])
    return [[A[i][j] for i in range(rows)] for j in range(cols)]

def sigmoid(x: float) -> float:
    try:
        return 1.0 / (1.0 + math.exp(-max(-500.0, min(500.0, x))))
    except Exception:
        return 0.0 if x < 0 else 1.0

def dao_ham_sigmoid(y: float) -> float:
    return y * (1.0 - y)

def relu(x: float) -> float:
    return max(0.0, x)

def dao_ham_relu(x: float) -> float:
    return 1.0 if x > 0 else 0.0

def softmax(lst: List[float]) -> List[float]:
    if not lst:
        return []
    max_val = max(lst)
    exps = [math.exp(max(-500.0, min(500.0, x - max_val))) for x in lst]
    sum_exps = sum(exps)
    return [e / sum_exps if sum_exps > 0 else 0.0 for e in exps]


# --- 2. Ultra-Lightweight Neural Network (Mạng Nơ-ron Nhân Tạo Siêu Nhẹ) ---

class MangNoRon:
    """
    Mạng Nơ-ron nhân tạo nhiều lớp (Multi-Layer Perceptron)
    Kích thước file mô hình chỉ vài KB, không cần thư viện GB bên ngoài!
    """
    def __init__(self, layer_sizes: List[int], activation: str = "sigmoid"):
        self.layer_sizes = layer_sizes
        self.activation_name = activation.lower()
        self.num_layers = len(layer_sizes)
        
        # Khởi tạo trọng số (Weights) và độ lệch (Biases)
        self.weights = []
        self.biases = []
        for i in range(len(layer_sizes) - 1):
            rows = layer_sizes[i + 1]
            cols = layer_sizes[i]
            # He / Xavier initialization
            scale = math.sqrt(2.0 / cols)
            w = [[random.gauss(0, scale) for _ in range(cols)] for _ in range(rows)]
            b = [0.0 for _ in range(rows)]
            self.weights.append(w)
            self.biases.append(b)

    def _activate(self, x: float) -> float:
        return relu(x) if self.activation_name == "relu" else sigmoid(x)

    def _activate_derivative(self, y: float) -> float:
        return dao_ham_relu(y) if self.activation_name == "relu" else dao_ham_sigmoid(y)

    def du_doan(self, x: List[float]) -> List[float]:
        """Truyền thẳng (Forward Propagation) để đưa ra dự đoán"""
        cur = x
        for w, b in zip(self.weights, self.biases):
            next_layer = []
            for r in range(len(w)):
                dot = sum(w[r][c] * cur[c] for c in range(len(cur))) + b[r]
                next_layer.append(self._activate(dot))
            cur = next_layer
        return cur

    def huan_luyen(self, X: List[List[float]], Y: List[List[float]], so_vong: int = 1000, toc_do_hoc: float = 0.1) -> float:
        """Huấn luyện mạng nơ-ron bằng thuật toán Lan Truyền Ngược (Backpropagation)"""
        last_loss = 0.0
        n_samples = len(X)

        for epoch in range(so_vong):
            total_loss = 0.0
            for idx in range(n_samples):
                x = X[idx]
                y_target = Y[idx]

                # 1. Forward Pass
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

                # 2. Backward Pass (Lan truyền ngược)
                deltas = []
                # Output layer delta
                output_delta = []
                for i in range(len(output)):
                    error = output[i] - y_target[i]
                    output_delta.append(error * self._activate_derivative(output[i]))
                deltas.append(output_delta)

                # Hidden layer deltas
                for l in range(len(self.weights) - 1, 0, -1):
                    w_next = self.weights[l]
                    d_next = deltas[-1]
                    cur_act = activations[l]
                    layer_delta = []
                    for i in range(len(cur_act)):
                        error = sum(w_next[r][i] * d_next[r] for r in range(len(w_next)))
                        layer_delta.append(error * self._activate_derivative(cur_act[i]))
                    deltas.append(layer_delta)

                deltas.reverse()

                # 3. Update Weights & Biases (Cập nhật trọng số)
                for l in range(len(self.weights)):
                    for r in range(len(self.weights[l])):
                        for c in range(len(self.weights[l][r])):
                            self.weights[l][r][c] -= toc_do_hoc * deltas[l][r] * activations[l][c]
                        self.biases[l][r] -= toc_do_hoc * deltas[l][r]

            last_loss = total_loss / n_samples
        return last_loss

    def luu_mo_hinh(self, filepath: str) -> bool:
        """Lưu toàn bộ mô hình AI ra file JSON siêu nhẹ (< 20 KB)"""
        data = {
            "type": "MangNoRon",
            "layer_sizes": self.layer_sizes,
            "activation": self.activation_name,
            "weights": self.weights,
            "biases": self.biases
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        return True

    @classmethod
    def tai_mo_hinh(cls, filepath: str) -> 'MangNoRon':
        """Tải mô hình AI đã huấn luyện từ file JSON"""
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        model = cls(data["layer_sizes"], data["activation"])
        model.weights = data["weights"]
        model.biases = data["biases"]
        return model


# --- 3. Linear Regression (Hồi Quy Tuyến Tính Siêu Tốc) ---

class HoiQuyTuyenTinh:
    """Mô hình dự đoán xu hướng và giá trị số (Linear Regression)"""
    def __init__(self):
        self.w = 0.0
        self.b = 0.0

    def huan_luyen(self, X: List[float], Y: List[float], so_vong: int = 1000, lr: float = 0.01) -> float:
        n = len(X)
        if n == 0: return 0.0
        for _ in range(so_vong):
            dw = 0.0
            db = 0.0
            for i in range(n):
                y_pred = self.w * X[i] + self.b
                err = y_pred - Y[i]
                dw += (2 / n) * err * X[i]
                db += (2 / n) * err
            self.w -= lr * dw
            self.b -= lr * db
        return sum((self.w * X[i] + self.b - Y[i]) ** 2 for i in range(n)) / n

    def du_doan(self, x: float) -> float:
        return self.w * x + self.b


# --- 4. Mini Language Model (Mô Hình AI Sinh Ngôn Ngữ Siêu Nhẹ) ---

class MoHinhNgonNgu:
    """Mô hình AI học hiểu và tự sinh văn bản thông minh (Mini Text Generator)"""
    def __init__(self, n_gram: int = 2):
        self.n = n_gram
        self.transitions: Dict[str, Dict[str, int]] = {}

    def hoc(self, text: str):
        words = text.split()
        if len(words) < self.n:
            return
        for i in range(len(words) - self.n):
            prefix = " ".join(words[i:i + self.n])
            nxt = words[i + self.n]
            if prefix not in self.transitions:
                self.transitions[prefix] = {}
            self.transitions[prefix][nxt] = self.transitions[prefix].get(nxt, 0) + 1

    def sinh_van_ban(self, bat_dau: str, do_dai: int = 20) -> str:
        words = bat_dau.split()
        for _ in range(do_dai):
            prefix = " ".join(words[-self.n:]) if len(words) >= self.n else " ".join(words)
            if prefix not in self.transitions:
                break
            candidates = self.transitions[prefix]
            total = sum(candidates.values())
            r = random.uniform(0, total)
            cum = 0
            chosen = None
            for word, count in candidates.items():
                cum += count
                if cum >= r:
                    chosen = word
                    break
            if not chosen:
                break
            words.append(chosen)
        return " ".join(words)

    def luu_mo_hinh(self, filepath: str):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump({"n": self.n, "transitions": self.transitions}, f, ensure_ascii=False)

    @classmethod
    def tai_mo_hinh(cls, filepath: str) -> 'MoHinhNgonNgu':
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        m = cls(data["n"])
        m.transitions = data["transitions"]
        return m


# --- Helper Factory Functions cho V++ ---

def tao_mang_no_ron(layer_sizes: List[int], activation: str = "sigmoid") -> MangNoRon:
    return MangNoRon(layer_sizes, activation)

def tao_hoi_quy() -> HoiQuyTuyenTinh:
    return HoiQuyTuyenTinh()

def tao_mo_hinh_ngon_ngu(n: int = 2) -> MoHinhNgonNgu:
    return MoHinhNgonNgu(n)
