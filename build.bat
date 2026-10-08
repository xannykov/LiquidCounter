@echo off
chcp 65001 >nul

taskkill /F /IM LiquidCounter.exe >nul 2>&1

if exist dist rmdir /S /Q dist
if exist build rmdir /S /Q build
if exist LiquidCounter.spec del /Q LiquidCounter.spec

python -m PyInstaller ^
    --onefile ^
    --windowed ^
    --icon "assets/icon-app.ico" ^
    --add-data "assets;assets" ^
    --name LiquidCounter ^
    --clean ^
    main.py

pause