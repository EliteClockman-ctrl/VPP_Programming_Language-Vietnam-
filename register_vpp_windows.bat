@echo off
chcp 65001 > nul
echo ============================================================
echo   DANG KY DINH DANG TEP .VPP VOI TRINH BIEN DICH VPP.EXE
echo ============================================================
echo.

set VPP_EXE=%~dp0vpp.exe

if not exist "%VPP_EXE%" (
    echo [Loi] Khong tim thay vpp.exe trong thu muc hien tai!
    pause
    exit /b 1
)

echo Dang thiet lap Registry Windows de mo .vpp bang vpp.exe...
assoc .vpp=VppSourceFile > nul
ftype VppSourceFile="%VPP_EXE%" "%%1" > nul

echo [Thanh cong] Da dang ky thanh cong .vpp voi vpp.exe!
echo Tu gio ban co the:
echo   1. Click dup truc tiep vao bat ky file .vpp nao de chay
echo   2. Chay lenh: vpp ten_file.vpp trong Terminal
echo.
pause
