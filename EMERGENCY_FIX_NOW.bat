@echo off
title ЭКСТРЕННОЕ ИСПРАВЛЕНИЕ ПРЕФИКСА "qс"
echo.
echo    🚨 ЭКСТРЕННОЕ ИСПРАВЛЕНИЕ "qс"
echo    ================================
echo.
echo ❌ ПРОБЛЕМА: Все команды получают префикс "qс"
echo ✅ РЕШЕНИЕ: Удаляем пакет qrcode и очищаем систему
echo.

echo 🔍 Шаг 1: Удаляем пакет qrcode...
pip uninstall qrcode -y
pip uninstall qrcode[pil] -y

echo.
echo 🔍 Шаг 2: Очищаем кэш pip...
pip cache purge

echo.
echo 🔍 Шаг 3: Проверяем переменные окружения...
setx PATH "%PATH:qс=%" /M
setx PSModulePath "%PSModulePath:qс=%" /M

echo.
echo 🔍 Шаг 4: Очищаем профиль PowerShell...
if exist "%USERPROFILE%\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1" (
    del "%USERPROFILE%\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1"
)
if exist "%USERPROFILE%\Documents\PowerShell\Microsoft.PowerShell_profile.ps1" (
    del "%USERPROFILE%\Documents\PowerShell\Microsoft.PowerShell_profile.ps1"
)

echo.
echo ✅ ИСПРАВЛЕНИЕ ЗАВЕРШЕНО!
echo.
echo 🔄 РЕКОМЕНДАЦИИ:
echo 1. Закройте ВСЕ терминалы
echo 2. Перезапустите Cursor
echo 3. Проверьте команды: echo ok, python --version
echo 4. Если проблема остается - перезагрузите компьютер
echo.
pause
