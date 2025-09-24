#!/usr/bin/env python3
"""
ПРОВЕРКА СИСТЕМЫ БЕЗ ИСПОЛЬЗОВАНИЯ ТЕРМИНАЛА
"""

import sys
import os
import platform
import subprocess
from pathlib import Path

def check_system():
    """Полная проверка системы"""
    print("🔍 ДИАГНОСТИКА СИСТЕМЫ")
    print("=" * 40)
    
    # Системная информация
    print(f"💻 ОС: {platform.system()} {platform.release()}")
    print(f"🐍 Python: {sys.version.split()[0]}")
    print(f"📁 Рабочая папка: {Path.cwd()}")
    print(f"🏠 Домашняя папка: {Path.home()}")
    
    # Проверка Python команд
    print("\n🐍 ПРОВЕРКА PYTHON КОМАНД:")
    python_commands = ['python', 'py', 'python3']
    
    for cmd in python_commands:
        try:
            result = subprocess.run([cmd, '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                version = result.stdout.strip() or result.stderr.strip()
                print(f"   ✅ {cmd}: {version}")
            else:
                print(f"   ❌ {cmd}: не работает")
        except FileNotFoundError:
            print(f"   ❌ {cmd}: не найден")
        except subprocess.TimeoutExpired:
            print(f"   ⏱️ {cmd}: таймаут")
        except Exception as e:
            print(f"   ❌ {cmd}: ошибка - {e}")
    
    # Проверка pip
    print("\n📦 ПРОВЕРКА PIP:")
    pip_commands = ['pip', 'pip3', 'python -m pip', 'py -m pip']
    
    for cmd in pip_commands:
        try:
            cmd_parts = cmd.split()
            result = subprocess.run(cmd_parts + ['--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"   ✅ {cmd}: {version}")
                break
        except Exception:
            print(f"   ❌ {cmd}: не работает")
    
    # Проверка файлов проекта
    print("\n📁 ПРОВЕРКА ФАЙЛОВ ПРОЕКТА:")
    required_files = [
        "app/main.py",
        "app/config.py", 
        "app/db.py",
        "requirements.txt",
        "env.mvp"
    ]
    
    all_good = True
    for file in required_files:
        if Path(file).exists():
            size = Path(file).stat().st_size
            print(f"   ✅ {file} ({size} байт)")
        else:
            print(f"   ❌ {file} - ОТСУТСТВУЕТ!")
            all_good = False
    
    # Проверка зависимостей
    print("\n📦 ПРОВЕРКА ЗАВИСИМОСТЕЙ:")
    required_modules = [
        'fastapi',
        'uvicorn', 
        'sqlalchemy',
        'jinja2',
        'pydantic'
    ]
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"   ✅ {module}")
        except ImportError:
            print(f"   ❌ {module} - НЕ УСТАНОВЛЕН!")
            all_good = False
    
    # Тест импорта приложения
    print("\n🧪 ТЕСТ ИМПОРТА ПРИЛОЖЕНИЯ:")
    try:
        from app.main import app
        print("   ✅ app.main импортирован успешно")
        print(f"   ✅ Тип приложения: {type(app)}")
    except Exception as e:
        print(f"   ❌ Ошибка импорта: {e}")
        all_good = False
    
    # Результат
    print("\n" + "=" * 40)
    if all_good:
        print("🎉 ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ!")
        print("🚀 Система готова к запуску сервера")
        print("\n💡 Для запуска используйте:")
        print("   - Двойной клик на ЗАПУСК_СЕРВЕРА_ПРЯМО_СЕЙЧАС.bat")
        print("   - Или двойной клик на start_server_NOW.py")
    else:
        print("❌ НАЙДЕНЫ ПРОБЛЕМЫ!")
        print("🔧 Исправьте ошибки выше и повторите проверку")
    
    return all_good

if __name__ == "__main__":
    try:
        success = check_system()
        input(f"\n{'✅ Готово!' if success else '❌ Есть проблемы!'} Нажмите Enter...")
    except Exception as e:
        print(f"\n💥 Критическая ошибка: {e}")
        input("Нажмите Enter для выхода...")
