@echo off
chcp 65001 >nul
title Cai Dat Ngon Ngu Lap Trinh V++ (1-Click Installer)
color 0B

echo ================================================================
echo           BO CAI DAT TU DONG NGON NGU LAP TRINH V++
echo ================================================================
echo.

set "INSTALL_DIR=%LOCALAPPDATA%\Vpp"
set "EXT_DIR=%USERPROFILE%\.vscode\extensions\vpp-language-support"
set "AGY_EXT_DIR=%USERPROFILE%\.antigravity-ide\extensions\vpp-language-support"

echo [1/4] Dang tao thu muc cai dat tai: %INSTALL_DIR%
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

echo [2/4] Dang sao chep vpp.exe va Logo...
copy /Y "vpp.exe" "%INSTALL_DIR%\vpp.exe" >nul
copy /Y "vpp_logo.ico" "%INSTALL_DIR%\vpp_logo.ico" >nul

echo [3/4] Dang cai dat Extension cho Visual Studio Code & Antigravity IDE...
if exist "%USERPROFILE%\.vscode\extensions" (
    xcopy /E /I /Y "vpp-vscode-extension" "%EXT_DIR%" >nul
    echo   - Da cai Extension cho VS Code thanh cong!
)
if exist "%USERPROFILE%\.antigravity-ide\extensions" (
    xcopy /E /I /Y "vpp-vscode-extension" "%AGY_EXT_DIR%" >nul
    echo   - Da cai Extension cho Antigravity IDE thanh cong!
)

echo [4/4] Dang dang ky dinh dang tep .vpp vao Windows Registry...
reg add "HKCU\Software\Classes\.vpp" /ve /d "VppSourceFile" /f >nul
reg add "HKCU\Software\Classes\VppSourceFile" /ve /d "V++ Source Code File" /f >nul
reg add "HKCU\Software\Classes\VppSourceFile\DefaultIcon" /ve /d "%INSTALL_DIR%\vpp_logo.ico,0" /f >nul
reg add "HKCU\Software\Classes\VppSourceFile\shell\open\command" /ve /d "\"%INSTALL_DIR%\vpp.exe\" \"%%1\"" /f >nul

:: Add to user PATH if not exists
setx PATH "%PATH%;%INSTALL_DIR%" >nul 2>&1

echo.
echo ================================================================
echo   CHUC MUNG! CAI DAT V++ HOAN TAT VA SAN SANG SU DUNG!
echo   - Go 'vpp' trong Terminal / PowerShell de chay.
echo   - Mo Visual Studio Code se tu dong to mau va goi y code .vpp!
echo ================================================================
pause
