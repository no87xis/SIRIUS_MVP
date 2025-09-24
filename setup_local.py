#!/usr/bin/env python3
"""
Автоматическая настройка локального окружения Sirius Group MVP
"""

import sys
import os
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, description=""):
    """Выполнение команды с обработкой ошибок"""
    print(f"🔄 {description}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✅ {description} - OK")
            return True
        else:
            print(f"   ❌ {description} - Ошибка: {result.stderr}")
            return False
    except Exception as e:
        print(f"   ❌ {description} - Исключение: {e}")
        return False

def check_python():
    """Проверка Python"""
    print("🐍 Проверка Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} - требуется >= 3.10")
        return False

def create_venv():
    """Создание виртуального окружения"""
    print("📦 Создание виртуального окружения...")
    
    venv_path = Path(".venv")
    if venv_path.exists():
        print("   ✅ Виртуальное окружение уже существует")
        return True
    
    if run_command("python -m venv .venv", "Создание venv"):
        print("   ✅ Виртуальное окружение создано")
        return True
    else:
        print("   ❌ Не удалось создать виртуальное окружение")
        return False

def activate_venv():
    """Активация виртуального окружения"""
    print("🔄 Активация виртуального окружения...")
    
    if os.name == 'nt':  # Windows
        activate_script = ".venv\\Scripts\\activate"
    else:  # Unix/Linux/macOS
        activate_script = ".venv/bin/activate"
    
    if Path(activate_script).exists():
        print(f"   ✅ Скрипт активации найден: {activate_script}")
        return activate_script
    else:
        print(f"   ❌ Скрипт активации не найден: {activate_script}")
        return None

def install_dependencies():
    """Установка зависимостей"""
    print("📦 Установка зависимостей...")
    
    # Обновляем pip
    if not run_command("python -m pip install --upgrade pip", "Обновление pip"):
        return False
    
    # Устанавливаем зависимости
    if run_command("pip install -r requirements.txt", "Установка зависимостей"):
        print("   ✅ Зависимости установлены")
        return True
    else:
        print("   ❌ Не удалось установить зависимости")
        return False

def setup_config():
    """Настройка конфигурации"""
    print("⚙️ Настройка конфигурации...")
    
    # Копируем env.mvp в .env
    if Path("env.mvp").exists():
        if not Path(".env").exists():
            shutil.copy("env.mvp", ".env")
            print("   ✅ .env создан из env.mvp")
        else:
            print("   ✅ .env уже существует")
    else:
        # Создаем .env с базовыми настройками
        env_content = """# Local Development Configuration
DATABASE_URL=sqlite:///./sirius.db
SECRET_KEY=Sirius_Local_Dev_ChangeMe_32chars_min
SESSION_MAX_AGE=86400
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO
"""
        with open(".env", "w") as f:
            f.write(env_content)
        print("   ✅ .env создан с базовыми настройками")
    
    # Создаем необходимые директории
    dirs = ["logs", "backups", "app/static", "app/templates"]
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    print("   ✅ Директории созданы")
    return True

def test_imports():
    """Тестирование импортов"""
    print("🧪 Тестирование импортов...")
    
    if run_command('python -c "from app.main import app; print(\'Imports OK\')"', "Проверка импортов"):
        print("   ✅ Импорты работают")
        return True
    else:
        print("   ❌ Ошибка импортов")
        return False

def create_startup_scripts():
    """Создание скриптов запуска"""
    print("📝 Создание скриптов запуска...")
    
    # Windows batch файл
    win_script = """@echo off
echo 🚀 Запуск Sirius Group MVP
cd /d "%~dp0"
call .venv\\Scripts\\activate
echo ✅ Виртуальное окружение активировано
echo 🌐 Запуск сервера на http://127.0.0.1:8000
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
pause
"""
    
    with open("start_local.bat", "w") as f:
        f.write(win_script)
    
    # Unix shell скрипт
    unix_script = """#!/bin/bash
echo "🚀 Запуск Sirius Group MVP"
cd "$(dirname "$0")"
source .venv/bin/activate
echo "✅ Виртуальное окружение активировано"
echo "🌐 Запуск сервера на http://127.0.0.1:8000"
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
"""
    
    with open("start_local.sh", "w") as f:
        f.write(unix_script)
    
    # Делаем shell скрипт исполняемым
    if os.name != 'nt':
        os.chmod("start_local.sh", 0o755)
    
    print("   ✅ Скрипты запуска созданы")
    return True

def main():
    """Основная функция настройки"""
    print("🚀 НАСТРОЙКА ЛОКАЛЬНОГО ОКРУЖЕНИЯ SIRIUS GROUP MVP")
    print("=" * 60)
    
    steps = [
        ("Проверка Python", check_python),
        ("Создание venv", create_venv),
        ("Настройка конфигурации", setup_config),
        ("Установка зависимостей", install_dependencies),
        ("Тестирование импортов", test_imports),
        ("Создание скриптов", create_startup_scripts)
    ]
    
    results = []
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}...")
        try:
            result = step_func()
            results.append(result)
        except Exception as e:
            print(f"   ❌ Ошибка в {step_name}: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print("📊 РЕЗУЛЬТАТЫ НАСТРОЙКИ:")
    
    success_count = sum(results)
    total_count = len(results)
    
    for i, (step_name, _) in enumerate(steps):
        status = "✅" if results[i] else "❌"
        print(f"   {status} {step_name}")
    
    print(f"\n🎯 Завершено: {success_count}/{total_count} шагов")
    
    if success_count == total_count:
        print("\n🎉 НАСТРОЙКА ЗАВЕРШЕНА УСПЕШНО!")
        print("\n🚀 ДЛЯ ЗАПУСКА СЕРВЕРА:")
        print("   Windows: start_local.bat")
        print("   Unix: ./start_local.sh")
        print("   Или: uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload")
        print("\n🌐 ССЫЛКИ:")
        print("   Health: http://127.0.0.1:8000/health")
        print("   Магазин: http://127.0.0.1:8000/shop")
        print("   Админ: http://127.0.0.1:8000/admin")
        return True
    else:
        print(f"\n❌ НАСТРОЙКА НЕ ЗАВЕРШЕНА ({total_count - success_count} ошибок)")
        print("🔧 Проверьте ошибки выше и повторите настройку")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
