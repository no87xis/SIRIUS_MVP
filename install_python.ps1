# PowerShell скрипт для установки Python и запуска сервера
# Запустите от имени администратора

Write-Host "🐍 УСТАНОВКА PYTHON И ЗАПУСК SIRIUS GROUP MVP" -ForegroundColor Green
Write-Host "=" * 50

# Проверяем, запущен ли скрипт от администратора
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "❌ Скрипт должен быть запущен от имени администратора!" -ForegroundColor Red
    Write-Host "🔧 Щелкните правой кнопкой на PowerShell и выберите 'Запуск от имени администратора'" -ForegroundColor Yellow
    Read-Host "Нажмите Enter для выхода"
    exit 1
}

Write-Host "✅ Скрипт запущен от имени администратора" -ForegroundColor Green

# Проверяем наличие winget
Write-Host "`n📦 Проверка winget..." -ForegroundColor Cyan
try {
    $wingetVersion = winget --version
    Write-Host "✅ winget найден: $wingetVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ winget не найден. Устанавливаем..." -ForegroundColor Red
    
    # Скачиваем и устанавливаем winget
    $wingetUrl = "https://github.com/microsoft/winget-cli/releases/latest/download/Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle"
    $wingetPath = "$env:TEMP\winget.msixbundle"
    
    Write-Host "📥 Скачивание winget..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri $wingetUrl -OutFile $wingetPath
    
    Write-Host "📦 Установка winget..." -ForegroundColor Yellow
    Add-AppxPackage -Path $wingetPath
    
    Remove-Item $wingetPath
    Write-Host "✅ winget установлен" -ForegroundColor Green
}

# Проверяем наличие Python
Write-Host "`n🐍 Проверка Python..." -ForegroundColor Cyan
try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match "Python 3\.(1[0-9]|[0-9])") {
        Write-Host "✅ Python уже установлен: $pythonVersion" -ForegroundColor Green
        $pythonInstalled = $true
    } else {
        Write-Host "⚠️ Python найден, но версия может быть устаревшей: $pythonVersion" -ForegroundColor Yellow
        $pythonInstalled = $false
    }
} catch {
    Write-Host "❌ Python не найден. Устанавливаем..." -ForegroundColor Red
    $pythonInstalled = $false
}

# Устанавливаем Python если нужно
if (-not $pythonInstalled) {
    Write-Host "`n📦 Установка Python 3.11..." -ForegroundColor Cyan
    try {
        winget install Python.Python.3.11 --accept-package-agreements --accept-source-agreements
        Write-Host "✅ Python 3.11 установлен" -ForegroundColor Green
    } catch {
        Write-Host "❌ Ошибка установки Python через winget" -ForegroundColor Red
        Write-Host "🔧 Попробуйте установить Python вручную с https://www.python.org/downloads/" -ForegroundColor Yellow
        Read-Host "Нажмите Enter для выхода"
        exit 1
    }
}

# Обновляем PATH
Write-Host "`n🔄 Обновление переменных окружения..." -ForegroundColor Cyan
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Проверяем Python после установки
Write-Host "`n🧪 Проверка Python после установки..." -ForegroundColor Cyan
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python работает: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python все еще не работает. Перезагрузите компьютер и попробуйте снова." -ForegroundColor Red
    Read-Host "Нажмите Enter для выхода"
    exit 1
}

# Переходим в папку проекта
Write-Host "`n📁 Переход в папку проекта..." -ForegroundColor Cyan
$projectPath = "D:\!РАЗРАБОТКА ПО\Sirius_sklad_new-master"
if (Test-Path $projectPath) {
    Set-Location $projectPath
    Write-Host "✅ Перешли в папку проекта" -ForegroundColor Green
} else {
    Write-Host "❌ Папка проекта не найдена: $projectPath" -ForegroundColor Red
    Read-Host "Нажмите Enter для выхода"
    exit 1
}

# Устанавливаем зависимости
Write-Host "`n📦 Установка зависимостей..." -ForegroundColor Cyan
try {
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    Write-Host "✅ Зависимости установлены" -ForegroundColor Green
} catch {
    Write-Host "❌ Ошибка установки зависимостей" -ForegroundColor Red
    Write-Host "🔧 Попробуйте запустить вручную: pip install -r requirements.txt" -ForegroundColor Yellow
}

# Создаем .env если нужно
Write-Host "`n⚙️ Настройка конфигурации..." -ForegroundColor Cyan
if (-not (Test-Path ".env")) {
    if (Test-Path "env.mvp") {
        Copy-Item "env.mvp" ".env"
        Write-Host "✅ .env создан из env.mvp" -ForegroundColor Green
    } else {
        $envContent = @"
# Local Development Configuration
DATABASE_URL=sqlite:///./sirius.db
SECRET_KEY=Sirius_Local_Dev_ChangeMe_32chars_min
SESSION_MAX_AGE=86400
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO
"@
        $envContent | Out-File -FilePath ".env" -Encoding UTF8
        Write-Host "✅ .env создан с базовыми настройками" -ForegroundColor Green
    }
} else {
    Write-Host "✅ .env уже существует" -ForegroundColor Green
}

# Создаем необходимые директории
Write-Host "`n📁 Создание директорий..." -ForegroundColor Cyan
$dirs = @("logs", "backups", "app\static", "app\templates")
foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}
Write-Host "✅ Директории созданы" -ForegroundColor Green

# Тестируем импорты
Write-Host "`n🧪 Тестирование импортов..." -ForegroundColor Cyan
try {
    python -c "from app.main import app; print('✅ Импорты работают')"
    Write-Host "✅ Приложение готово к запуску" -ForegroundColor Green
} catch {
    Write-Host "❌ Ошибка импортов" -ForegroundColor Red
    Write-Host "🔧 Проверьте зависимости и конфигурацию" -ForegroundColor Yellow
}

# Запускаем сервер
Write-Host "`n🚀 ЗАПУСК СЕРВЕРА..." -ForegroundColor Green
Write-Host "=" * 50
Write-Host "🌐 Сервер будет доступен по адресам:" -ForegroundColor Cyan
Write-Host "   Главная: http://127.0.0.1:8000" -ForegroundColor White
Write-Host "   Магазин: http://127.0.0.1:8000/shop" -ForegroundColor White
Write-Host "   Админ: http://127.0.0.1:8000/admin" -ForegroundColor White
Write-Host "   API Docs: http://127.0.0.1:8000/docs" -ForegroundColor White
Write-Host "   Health: http://127.0.0.1:8000/health" -ForegroundColor White
Write-Host "`n⏹️ Для остановки сервера нажмите Ctrl+C" -ForegroundColor Yellow
Write-Host "=" * 50

try {
    uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
} catch {
    Write-Host "`n❌ Ошибка запуска сервера" -ForegroundColor Red
    Write-Host "🔧 Попробуйте запустить вручную: python launch_server.py" -ForegroundColor Yellow
    Read-Host "Нажмите Enter для выхода"
}
