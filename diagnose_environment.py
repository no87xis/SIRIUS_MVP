#!/usr/bin/env python3
"""
Диагностика окружения для запуска Sirius Group MVP
"""

import sys
import os
import subprocess
import platform
from pathlib import Path

def check_python():
    """Проверка версии Python"""
    print("🐍 Проверка Python...")
    version = sys.version_info
    print(f"   Версия: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 10:
        print("   ✅ Python >= 3.10 - OK")
        return True
    else:
        print("   ❌ Требуется Python >= 3.10")
        return False

def check_git():
    """Проверка Git"""
    print("📦 Проверка Git...")
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✅ Git найден: {result.stdout.strip()}")
            return True
        else:
            print("   ❌ Git не найден")
            return False
    except FileNotFoundError:
        print("   ❌ Git не установлен")
        return False

def check_project_structure():
    """Проверка структуры проекта"""
    print("📁 Проверка структуры проекта...")
    
    required_files = [
        'app/main.py',
        'requirements.txt',
        'env.mvp'
    ]
    
    required_dirs = [
        'app',
        'app/templates',
        'app/static'
    ]
    
    all_ok = True
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} - не найден")
            all_ok = False
    
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"   ✅ {dir_path}/")
        else:
            print(f"   ❌ {dir_path}/ - не найден")
            all_ok = False
    
    return all_ok

def check_os():
    """Проверка операционной системы"""
    print("💻 Информация об ОС...")
    system = platform.system()
    release = platform.release()
    version = platform.version()
    
    print(f"   Система: {system}")
    print(f"   Версия: {release}")
    print(f"   Сборка: {version}")
    
    if system == "Windows":
        print("   ✅ Windows - поддерживается")
    elif system == "Darwin":
        print("   ✅ macOS - поддерживается")
    elif system == "Linux":
        print("   ✅ Linux - поддерживается")
    else:
        print(f"   ⚠️ {system} - может потребоваться настройка")
    
    return True

def main():
    """Основная функция диагностики"""
    print("🔍 ДИАГНОСТИКА ОКРУЖЕНИЯ SIRIUS GROUP MVP")
    print("=" * 50)
    
    checks = [
        check_os,
        check_python,
        check_git,
        check_project_structure
    ]
    
    results = []
    for check in checks:
        try:
            result = check()
            results.append(result)
            print()
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
            results.append(False)
            print()
    
    print("=" * 50)
    print("📊 РЕЗУЛЬТАТЫ ДИАГНОСТИКИ:")
    
    if all(results):
        print("✅ Все проверки пройдены успешно!")
        print("🚀 Окружение готово к запуску")
        return True
    else:
        print("❌ Обнаружены проблемы:")
        if not results[1]:  # Python
            print("   - Установите Python >= 3.10")
        if not results[2]:  # Git
            print("   - Установите Git")
        if not results[3]:  # Project structure
            print("   - Проверьте структуру проекта")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
