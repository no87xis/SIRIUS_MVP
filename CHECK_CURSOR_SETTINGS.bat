@echo off
title ПРОВЕРКА НАСТРОЕК CURSOR
echo.
echo    🔍 ПРОВЕРКА НАСТРОЕК CURSOR
echo    ===========================
echo.

echo 🔍 Проверяем настройки Cursor...
echo.

echo 📁 Путь к настройкам: %APPDATA%\Cursor
echo.

if exist "%APPDATA%\Cursor\User\settings.json" (
    echo ✅ Найден settings.json
    echo.
    echo 🔍 Содержимое settings.json:
    type "%APPDATA%\Cursor\User\settings.json"
    echo.
    echo 🔍 Поиск "qс" в settings.json:
    type "%APPDATA%\Cursor\User\settings.json" | findstr /i "qс"
    if %errorlevel%==0 (
        echo ❌ Найден "qс" в settings.json!
    ) else (
        echo ✅ "qс" не найден в settings.json
    )
) else (
    echo ❌ settings.json не найден
)

echo.
if exist "%APPDATA%\Cursor\User\keybindings.json" (
    echo ✅ Найден keybindings.json
    echo.
    echo 🔍 Поиск "qс" в keybindings.json:
    type "%APPDATA%\Cursor\User\keybindings.json" | findstr /i "qс"
    if %errorlevel%==0 (
        echo ❌ Найден "qс" в keybindings.json!
    ) else (
        echo ✅ "qс" не найден в keybindings.json
    )
) else (
    echo ❌ keybindings.json не найден
)

echo.
echo 🔍 Проверяем расширения Cursor...
if exist "%APPDATA%\Cursor\extensions" (
    echo ✅ Папка расширений найдена
    dir "%APPDATA%\Cursor\extensions" /b | findstr /i "qr"
    if %errorlevel%==0 (
        echo ❌ Найдены подозрительные расширения!
    ) else (
        echo ✅ Подозрительные расширения не найдены
    )
) else (
    echo ❌ Папка расширений не найдена
)

echo.
echo 🔍 Проверяем логи Cursor...
if exist "%APPDATA%\Cursor\logs" (
    echo ✅ Папка логов найдена
    echo 🔍 Поиск "qс" в логах:
    findstr /s /i "qс" "%APPDATA%\Cursor\logs\*" 2>nul
    if %errorlevel%==0 (
        echo ❌ Найден "qс" в логах Cursor!
    ) else (
        echo ✅ "qс" не найден в логах
    )
) else (
    echo ❌ Папка логов не найдена
)

echo.
echo ✅ ПРОВЕРКА ЗАВЕРШЕНА!
echo.
pause

