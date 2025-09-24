@echo off
title ОЧИСТКА НАСТРОЕК CURSOR
echo.
echo    🧹 ОЧИСТКА НАСТРОЕК CURSOR
echo    ==========================
echo.

echo 🔍 Шаг 1: Создаем резервную копию настроек...
echo.

if exist "%APPDATA%\Cursor\User\settings.json" (
    copy "%APPDATA%\Cursor\User\settings.json" "%APPDATA%\Cursor\User\settings.json.backup"
    echo ✅ Резервная копия создана: settings.json.backup
) else (
    echo ❌ settings.json не найден
)

if exist "%APPDATA%\Cursor\User\keybindings.json" (
    copy "%APPDATA%\Cursor\User\keybindings.json" "%APPDATA%\Cursor\User\keybindings.json.backup"
    echo ✅ Резервная копия создана: keybindings.json.backup
) else (
    echo ❌ keybindings.json не найден
)

echo.
echo 🔍 Шаг 2: Очищаем настройки Cursor...
echo.

echo Создаем чистый settings.json...
echo { > "%APPDATA%\Cursor\User\settings.json"
echo     "window.commandCenter": true, >> "%APPDATA%\Cursor\User\settings.json"
echo     "terminal.integrated.shell.windows": "powershell.exe" >> "%APPDATA%\Cursor\User\settings.json"
echo } >> "%APPDATA%\Cursor\User\settings.json"

echo ✅ settings.json очищен

echo.
echo Создаем чистый keybindings.json...
echo [ > "%APPDATA%\Cursor\User\keybindings.json"
echo ] >> "%APPDATA%\Cursor\User\keybindings.json"

echo ✅ keybindings.json очищен

echo.
echo 🔍 Шаг 3: Удаляем кэш Cursor...
echo.

if exist "%APPDATA%\Cursor\CachedData" (
    rmdir /s /q "%APPDATA%\Cursor\CachedData"
    echo ✅ Кэш Cursor удален
) else (
    echo ❌ Кэш Cursor не найден
)

if exist "%APPDATA%\Cursor\logs" (
    rmdir /s /q "%APPDATA%\Cursor\logs"
    echo ✅ Логи Cursor удалены
) else (
    echo ❌ Логи Cursor не найдены
)

echo.
echo 🔍 Шаг 4: Проверяем расширения...
echo.

if exist "%APPDATA%\Cursor\extensions" (
    echo 📁 Расширения Cursor:
    dir "%APPDATA%\Cursor\extensions" /b
    echo.
    echo 🔍 Поиск подозрительных расширений:
    dir "%APPDATA%\Cursor\extensions" /b | findstr /i "qr"
    if %errorlevel%==0 (
        echo ❌ Найдены подозрительные расширения!
        echo ⚠️ Рекомендуется удалить их вручную
    ) else (
        echo ✅ Подозрительные расширения не найдены
    )
) else (
    echo ❌ Папка расширений не найдена
)

echo.
echo ✅ ОЧИСТКА НАСТРОЕК ЗАВЕРШЕНА!
echo.
echo 🔄 РЕКОМЕНДАЦИИ:
echo 1. Закройте Cursor полностью
echo 2. Перезапустите Cursor
echo 3. Проверьте терминал
echo 4. Если проблема остается - переустановите Cursor
echo.
pause

