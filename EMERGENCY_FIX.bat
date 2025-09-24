@echo off
title ЭКСТРЕННОЕ ИСПРАВЛЕНИЕ ПРЕФИКСА
color 0E

echo.
echo ========================================
echo    🚨 ЭКСТРЕННОЕ ИСПРАВЛЕНИЕ "qс"
echo ========================================
echo.

echo 🔧 Запуск исправления Python скриптом...
python fix_terminal_direct.py

echo.
echo 🔄 Перезагрузка переменных окружения...
set PATH=%PATH%

echo.
echo ✅ ИСПРАВЛЕНИЕ ЗАВЕРШЕНО!
echo.
echo 📋 ПРОВЕРЬТЕ:
echo 1. Откройте НОВЫЙ терминал
echo 2. Выполните: echo test
echo 3. Выполните: python --version
echo.

pause

