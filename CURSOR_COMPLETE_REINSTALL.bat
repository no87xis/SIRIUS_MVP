@echo off
title ПОЛНАЯ ПЕРЕУСТАНОВКА CURSOR
echo.
echo    🔄 ПОЛНАЯ ПЕРЕУСТАНОВКА CURSOR
echo    ==============================
echo.

echo ⚠️ ВНИМАНИЕ: Этот скрипт полностью удалит Cursor и все его настройки!
echo.
echo 🔍 Шаг 1: Закрываем все процессы Cursor...
echo.
taskkill /f /im cursor.exe 2>nul
taskkill /f /im "Cursor.exe" 2>nul
echo ✅ Процессы Cursor завершены
echo.

echo 🔍 Шаг 2: Удаляем папку настроек Cursor...
echo.
if exist "%APPDATA%\Cursor" (
    echo ⚠️ Найдена папка настроек: %APPDATA%\Cursor
    echo Создаем резервную копию...
    xcopy "%APPDATA%\Cursor" "%APPDATA%\Cursor_backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%" /e /i /h /y
    echo ✅ Резервная копия создана
    echo.
    echo Удаляем папку настроек...
    rmdir /s /q "%APPDATA%\Cursor"
    echo ✅ Папка настроек удалена
) else (
    echo ✅ Папка настроек не найдена
)
echo.

echo 🔍 Шаг 3: Удаляем папку локальных данных Cursor...
echo.
if exist "%LOCALAPPDATA%\Cursor" (
    echo ⚠️ Найдена папка локальных данных: %LOCALAPPDATA%\Cursor
    echo Удаляем папку локальных данных...
    rmdir /s /q "%LOCALAPPDATA%\Cursor"
    echo ✅ Папка локальных данных удалена
) else (
    echo ✅ Папка локальных данных не найдена
)
echo.

echo 🔍 Шаг 4: Удаляем папку временных файлов Cursor...
echo.
if exist "%TEMP%\Cursor" (
    echo ⚠️ Найдена папка временных файлов: %TEMP%\Cursor
    echo Удаляем папку временных файлов...
    rmdir /s /q "%TEMP%\Cursor"
    echo ✅ Папка временных файлов удалена
) else (
    echo ✅ Папка временных файлов не найдена
)
echo.

echo 🔍 Шаг 5: Удаляем записи из реестра...
echo.
reg delete "HKEY_CURRENT_USER\Software\Cursor" /f 2>nul
if %errorlevel%==0 (
    echo ✅ Записи реестра удалены
) else (
    echo ✅ Записи реестра не найдены
)
echo.

echo 🔍 Шаг 6: Удаляем ярлыки Cursor...
echo.
if exist "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Cursor.lnk" (
    del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Cursor.lnk"
    echo ✅ Ярлык из меню Пуск удален
)
if exist "%USERPROFILE%\Desktop\Cursor.lnk" (
    del "%USERPROFILE%\Desktop\Cursor.lnk"
    echo ✅ Ярлык с рабочего стола удален
)
echo.

echo 🔍 Шаг 7: Очищаем кэш браузера (если используется)...
echo.
if exist "%LOCALAPPDATA%\Google\Chrome\User Data\Default\Local Storage\https_cursor.sh" (
    rmdir /s /q "%LOCALAPPDATA%\Google\Chrome\User Data\Default\Local Storage\https_cursor.sh"
    echo ✅ Кэш браузера очищен
)
echo.

echo ✅ ПОЛНАЯ ОЧИСТКА CURSOR ЗАВЕРШЕНА!
echo.
echo 🔄 СЛЕДУЮЩИЕ ШАГИ:
echo 1. Перезагрузите компьютер
echo 2. Скачайте Cursor с официального сайта
echo 3. Установите Cursor заново
echo 4. Проверьте терминал
echo.
echo 📁 Резервная копия настроек: %APPDATA%\Cursor_backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%
echo.
pause
