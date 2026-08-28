@echo off
chcp 65001 >nul
echo ==========================================================
echo    CÀI ĐẶT TỰ ĐỘNG NGÔN NGỮ LẬP TRÌNH V++ CHO WINDOWS     
echo ==========================================================
echo.

set "VPP_DIR=%~dp0"
set "VPP_DIR=%VPP_DIR:~0,-1%"

echo [1/3] Đang sao chép tệp thực thi vào thư mục hệ thống...
if not exist "%USERPROFILE%\.vpp" mkdir "%USERPROFILE%\.vpp"
copy /Y "%VPP_DIR%\vpp.exe" "%USERPROFILE%\.vpp\vpp.exe" >nul

echo [2/3] Đang cấu hình biến môi trường PATH...
for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /v Path 2^>nul') do set "USER_PATH=%%b"
echo %USER_PATH% | find /i "%USERPROFILE%\.vpp" >nul
if errorlevel 1 (
    if defined USER_PATH (
        setx Path "%USER_PATH%;%USERPROFILE%\.vpp" >nul
    ) else (
        setx Path "%USERPROFILE%\.vpp" >nul
    )
    echo    Đã thêm "%USERPROFILE%\.vpp" vào PATH thành công!
) else (
    echo    Đường dẫn đã tồn tại trong PATH.
)

echo [3/3] Đang đăng ký mở tệp đuôi .vpp...
assoc .vpp=VPPFile >nul 2>&1
ftype VPPFile="%USERPROFILE%\.vpp\vpp.exe" "%%1" %%* >nul 2>&1

echo.
echo ==========================================================
echo    🎉 CÀI ĐẶT V++ HOÀN TẤT THÀNH CÔNG 100%!
echo.
echo    • Chạy code : vpp ten_file.vpp
echo    • REPL tương tác: vpp
echo    • Xem trợ giúp: vpp --help
echo ==========================================================
pause
