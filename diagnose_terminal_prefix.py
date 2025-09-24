#!/usr/bin/env python3
"""
Диагностика проблемы с префиксом "qс" в терминале
"""

import os
import sys
import subprocess
from pathlib import Path

def check_vscode_config():
    """Проверка конфигурации VS Code"""
    print("🔍 Проверка конфигурации VS Code...")
    
    vscode_paths = [
        ".vscode/settings.json",
        ".vscode/tasks.json", 
        ".vscode/launch.json",
        ".vscode/extensions.json"
    ]
    
    found_files = []
    for path in vscode_paths:
        if Path(path).exists():
            found_files.append(path)
            print(f"   ✅ Найден: {path}")
            
            # Проверяем содержимое на наличие "qс"
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'qс' in content:
                        print(f"   ⚠️ Найден префикс 'qс' в {path}")
                        return path, content
            except Exception as e:
                print(f"   ❌ Ошибка чтения {path}: {e}")
        else:
            print(f"   ❌ Не найден: {path}")
    
    if not found_files:
        print("   ℹ️ Папка .vscode не найдена")
    
    return None, None

def check_powershell_profile():
    """Проверка PowerShell профиля"""
    print("\n🔍 Проверка PowerShell профиля...")
    
    try:
        # Получаем путь к профилю
        result = subprocess.run(['powershell', '-Command', '$PROFILE'], 
                              capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            profile_path = result.stdout.strip()
            print(f"   📁 Путь к профилю: {profile_path}")
            
            if Path(profile_path).exists():
                print(f"   ✅ Профиль существует")
                with open(profile_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'qс' in content:
                        print(f"   ⚠️ Найден префикс 'qс' в профиле")
                        return profile_path, content
                    else:
                        print(f"   ✅ Префикс 'qс' не найден в профиле")
            else:
                print(f"   ❌ Профиль не существует")
        else:
            print(f"   ❌ Не удалось получить путь к профилю")
    except Exception as e:
        print(f"   ❌ Ошибка проверки профиля: {e}")
    
    return None, None

def check_environment_variables():
    """Проверка переменных окружения"""
    print("\n🔍 Проверка переменных окружения...")
    
    env_vars = ['PSModulePath', 'PATH', 'PSExecutionPolicyPreference']
    for var in env_vars:
        value = os.environ.get(var, '')
        if 'qс' in value:
            print(f"   ⚠️ Найден префикс 'qс' в {var}: {value}")
            return var, value
        else:
            print(f"   ✅ {var}: OK")
    
    return None, None

def check_registry():
    """Проверка реестра Windows"""
    print("\n🔍 Проверка реестра Windows...")
    
    try:
        # Проверяем ключи реестра, связанные с PowerShell
        reg_keys = [
            r'HKEY_CURRENT_USER\Software\Microsoft\PowerShell',
            r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\PowerShell',
            r'HKEY_CURRENT_USER\Console'
        ]
        
        for key in reg_keys:
            try:
                result = subprocess.run(['reg', 'query', key], 
                                      capture_output=True, text=True, shell=True)
                if result.returncode == 0 and 'qс' in result.stdout:
                    print(f"   ⚠️ Найден префикс 'qс' в реестре: {key}")
                    return key, result.stdout
            except:
                pass
        
        print("   ✅ Префикс 'qс' не найден в реестре")
    except Exception as e:
        print(f"   ❌ Ошибка проверки реестра: {e}")
    
    return None, None

def create_fix_script():
    """Создание скрипта для исправления"""
    print("\n🔧 Создание скрипта исправления...")
    
    fix_script = '''# PowerShell скрипт для исправления префикса "qс"
# Запустите от имени администратора

Write-Host "🔧 ИСПРАВЛЕНИЕ ПРЕФИКСА 'qс' В ТЕРМИНАЛЕ" -ForegroundColor Green
Write-Host "=" * 50

# Проверяем права администратора
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "❌ Скрипт должен быть запущен от имени администратора!" -ForegroundColor Red
    Read-Host "Нажмите Enter для выхода"
    exit 1
}

Write-Host "✅ Скрипт запущен от имени администратора" -ForegroundColor Green

# Создаем резервную копию профиля PowerShell
$profilePath = $PROFILE
if (Test-Path $profilePath) {
    $backupPath = "$profilePath.backup.$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    Copy-Item $profilePath $backupPath
    Write-Host "✅ Резервная копия профиля создана: $backupPath" -ForegroundColor Green
    
    # Проверяем содержимое профиля
    $content = Get-Content $profilePath -Raw
    if ($content -match 'qс') {
        Write-Host "⚠️ Найден префикс 'qс' в профиле PowerShell" -ForegroundColor Yellow
        $newContent = $content -replace 'qс', ''
        Set-Content $profilePath $newContent -Encoding UTF8
        Write-Host "✅ Префикс 'qс' удален из профиля" -ForegroundColor Green
    }
}

# Проверяем переменные окружения
Write-Host "`n🔍 Проверка переменных окружения..." -ForegroundColor Cyan
$envVars = @('PSModulePath', 'PATH', 'PSExecutionPolicyPreference')
foreach ($var in $envVars) {
    $value = [Environment]::GetEnvironmentVariable($var, 'User')
    if ($value -and $value -match 'qс') {
        Write-Host "⚠️ Найден префикс 'qс' в переменной $var" -ForegroundColor Yellow
        $newValue = $value -replace 'qс', ''
        [Environment]::SetEnvironmentVariable($var, $newValue, 'User')
        Write-Host "✅ Переменная $var исправлена" -ForegroundColor Green
    }
}

# Перезагружаем переменные окружения
Write-Host "`n🔄 Перезагрузка переменных окружения..." -ForegroundColor Cyan
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

Write-Host "`n✅ ИСПРАВЛЕНИЕ ЗАВЕРШЕНО!" -ForegroundColor Green
Write-Host "🔄 Перезапустите терминал для применения изменений" -ForegroundColor Yellow
Read-Host "Нажмите Enter для выхода"
'''
    
    with open('fix_terminal_prefix.ps1', 'w', encoding='utf-8') as f:
        f.write(fix_script)
    
    print("   ✅ Создан скрипт: fix_terminal_prefix.ps1")

def main():
    """Основная функция диагностики"""
    print("🔍 ДИАГНОСТИКА ПРЕФИКСА 'qс' В ТЕРМИНАЛЕ")
    print("=" * 50)
    
    # Проверяем различные источники проблемы
    sources = [
        ("VS Code конфигурация", check_vscode_config),
        ("PowerShell профиль", check_powershell_profile),
        ("Переменные окружения", check_environment_variables),
        ("Реестр Windows", check_registry)
    ]
    
    found_source = None
    found_content = None
    
    for source_name, check_func in sources:
        print(f"\n📋 {source_name}...")
        try:
            source, content = check_func()
            if source:
                found_source = source
                found_content = content
                print(f"   🎯 ИСТОЧНИК НАЙДЕН: {source}")
                break
        except Exception as e:
            print(f"   ❌ Ошибка проверки: {e}")
    
    print("\n" + "=" * 50)
    print("📊 РЕЗУЛЬТАТЫ ДИАГНОСТИКИ:")
    
    if found_source:
        print(f"✅ ИСТОЧНИК ПРОБЛЕМЫ НАЙДЕН: {found_source}")
        print("🔧 Создаю скрипт исправления...")
        create_fix_script()
    else:
        print("❌ ИСТОЧНИК ПРОБЛЕМЫ НЕ НАЙДЕН")
        print("🔧 Создаю общий скрипт исправления...")
        create_fix_script()
    
    print("\n🚀 РЕКОМЕНДАЦИИ:")
    print("1. Запустите fix_terminal_prefix.ps1 от имени администратора")
    print("2. Перезапустите терминал")
    print("3. Проверьте команды: echo ok, python --version")
    
    return found_source is not None

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

