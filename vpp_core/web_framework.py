"""
================================================================================
  V++ Programming Language — Fullstack Web & Backend Engine (Top-Tier)
  Máy chủ Web HTTP REST API, Phục vụ HTML/CSS/JS, Xử lý JSON & CORS siêu tốc
================================================================================
"""

import http.server
import socketserver
import json
import urllib.parse
import threading
from typing import Dict, Any, Callable, Optional

class MayChuWebVPP:
    def __init__(self, port: int = 8080):
        self.port = port
        self.routes: Dict[str, Dict[str, Callable]] = {"GET": {}, "POST": {}, "PUT": {}, "DELETE": {}}
        self.static_files: Dict[str, str] = {}
        self.server: Optional[socketserver.TCPServer] = None
        self._thread: Optional[threading.Thread] = None

    def route_get(self, path: str, handler: Callable):
        self.routes["GET"][path] = handler

    def route_post(self, path: str, handler: Callable):
        self.routes["POST"][path] = handler

    def them_trang_tinh(self, path: str, content: str, content_type: str = "text/html; charset=utf-8"):
        self.static_files[path] = (content, content_type)

    def bat_dau(self, chay_ngam: bool = False):
        app = self

        class CustomHandler(http.server.BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                pass  # Suppress default noisy console logs

            def send_cors_headers(self):
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
                self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

            def do_OPTIONS(self):
                self.send_response(200)
                self.send_cors_headers()
                self.end_headers()

            def do_GET(self):
                parsed = urllib.parse.urlparse(self.path)
                path = parsed.path

                if path in app.static_files:
                    content, ctype = app.static_files[path]
                    self.send_response(200)
                    self.send_header("Content-Type", ctype)
                    self.send_cors_headers()
                    self.end_headers()
                    self.wfile.write(content.encode("utf-8"))
                    return

                if path in app.routes["GET"]:
                    try:
                        res = app.routes["GET"][path]()
                        if isinstance(res, (dict, list)):
                            body = json.dumps(res, ensure_ascii=False).encode("utf-8")
                            self.send_response(200)
                            self.send_header("Content-Type", "application/json; charset=utf-8")
                        else:
                            body = str(res).encode("utf-8")
                            self.send_response(200)
                            self.send_header("Content-Type", "text/html; charset=utf-8")
                        self.send_cors_headers()
                        self.end_headers()
                        self.wfile.write(body)
                    except Exception as e:
                        self.send_response(500)
                        self.send_header("Content-Type", "application/json")
                        self.send_cors_headers()
                        self.end_headers()
                        self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
                    return

                self.send_response(404)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write(b"404 - Khong tim thay trang yeu cau")

            def do_POST(self):
                parsed = urllib.parse.urlparse(self.path)
                path = parsed.path

                content_len = int(self.headers.get("Content-Length", 0))
                post_body = self.rfile.read(content_len).decode("utf-8")
                try:
                    json_data = json.loads(post_body) if post_body else {}
                except Exception:
                    json_data = post_body

                if path in app.routes["POST"]:
                    try:
                        res = app.routes["POST"][path](json_data)
                        if isinstance(res, (dict, list)):
                            body = json.dumps(res, ensure_ascii=False).encode("utf-8")
                            self.send_response(200)
                            self.send_header("Content-Type", "application/json; charset=utf-8")
                        else:
                            body = str(res).encode("utf-8")
                            self.send_response(200)
                            self.send_header("Content-Type", "text/plain; charset=utf-8")
                        self.send_cors_headers()
                        self.end_headers()
                        self.wfile.write(body)
                    except Exception as e:
                        self.send_response(500)
                        self.send_header("Content-Type", "application/json")
                        self.send_cors_headers()
                        self.end_headers()
                        self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
                    return

                self.send_response(404)
                self.end_headers()

        socketserver.TCPServer.allow_reuse_address = True
        self.server = socketserver.TCPServer(("", self.port), CustomHandler)
        print(f"🚀 [MÁY CHỦ WEB V++] Đang hoạt động tại: http://localhost:{self.port}")

        if chay_ngam:
            self._thread = threading.Thread(target=self.server.serve_forever, daemon=True)
            self._thread.start()
        else:
            try:
                self.server.serve_forever()
            except KeyboardInterrupt:
                self.dung()

    def dung(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()


def tao_may_chu_web(port: int = 8080) -> MayChuWebVPP:
    return MayChuWebVPP(port)
