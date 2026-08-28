#!/usr/bin/env python3
"""
========================================================================
  V++ PROGRAMMING LANGUAGE (PHIÊN BẢN 1.0) — MASTER ENTRY POINT
========================================================================
"""

import sys
import os

# Thêm thư mục hiện tại vào đường dẫn import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    # Chạy giao diện dòng lệnh V++ CLI & REPL
    from vpp_core.vpp_cli import main as cli_main
    cli_main()

if __name__ == "__main__":
    main()
