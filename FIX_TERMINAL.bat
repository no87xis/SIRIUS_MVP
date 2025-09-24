@echo off
title Исправление префикса "qс" в терминале
color 0C

echo.
echo ========================================
echo    🔧 ИСПРАВЛЕНИЕ ПРЕФИКСА "qс"
echo ========================================
echo.

echo ❌ ПРОБЛЕМА: Все команды получают префикс "qс"
echo 🔧 РЕШЕНИЕ: Запуск скрипта исправления
echo.

echo 🚀 Запуск PowerShell скрипта исправления...
echo.

REM Запускаем PowerShell скрипт от имени администратора
powershell -Command "Start-Process PowerShell -ArgumentList '-ExecutionPolicy Bypass -File \"%~dp0fix_terminal_prefix.ps1\"' -Verb RunAs"

echo.
echo ✅ Скрипт исправления запущен
echo.
echo 🔄 СЛЕДУЮЩИЕ ШАГИ:
echo 1. В открывшемся окне PowerShell следуйте инструкциям
echo 2. Перезапустите терминал после завершения
echo 3. Проверьте команды: echo ok, python --version
echo.
pause

