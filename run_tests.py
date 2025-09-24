#!/usr/bin/env python3
"""
Скрипт для запуска быстрых тестов стабильности
Все тесты должны завершаться за секунды и не зависать
"""

import sys
import os
import time
import subprocess
from pathlib import Path

# Добавляем корневую папку проекта в путь
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def run_basic_tests():
    """Запуск базовых тестов"""
    print("🧪 Запуск базовых тестов...")
    start_time = time.time()
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/test_basic.py", 
            "-v", 
            "--tb=short",
            "--timeout=10",
            "--maxfail=3"
        ], capture_output=True, text=True, timeout=30)
        
        duration = time.time() - start_time
        print(f"⏱️ Базовые тесты завершены за {duration:.2f}s")
        
        if result.returncode == 0:
            print("✅ Базовые тесты пройдены успешно")
            return True
        else:
            print("❌ Базовые тесты провалены")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Базовые тесты превысили таймаут (30s)")
        return False
    except Exception as e:
        print(f"❌ Ошибка запуска базовых тестов: {e}")
        return False


def run_integration_tests():
    """Запуск интеграционных тестов"""
    print("🔗 Запуск интеграционных тестов...")
    start_time = time.time()
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/test_integration.py", 
            "-v", 
            "--tb=short",
            "--timeout=15",
            "--maxfail=3"
        ], capture_output=True, text=True, timeout=60)
        
        duration = time.time() - start_time
        print(f"⏱️ Интеграционные тесты завершены за {duration:.2f}s")
        
        if result.returncode == 0:
            print("✅ Интеграционные тесты пройдены успешно")
            return True
        else:
            print("❌ Интеграционные тесты провалены")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Интеграционные тесты превысили таймаут (60s)")
        return False
    except Exception as e:
        print(f"❌ Ошибка запуска интеграционных тестов: {e}")
        return False


def test_imports():
    """Быстрая проверка импортов"""
    print("📦 Проверка импортов...")
    start_time = time.time()
    
    try:
        # Проверяем основные импорты
        from app.main import app
        from app.config import settings
        from app.db import engine, Base, get_db
        from app.services.logger import logger
        from app.services.monitoring import performance_monitor
        from app.services.qr_service import QRService
        
        duration = time.time() - start_time
        print(f"✅ Импорты работают за {duration:.2f}s")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка импорта: {e}")
        return False


def test_syntax():
    """Проверка синтаксиса основных файлов"""
    print("🔍 Проверка синтаксиса...")
    start_time = time.time()
    
    files_to_check = [
        "app/main.py",
        "app/config.py", 
        "app/db.py",
        "app/services/logger.py",
        "app/services/monitoring.py",
        "app/services/qr_service.py"
    ]
    
    try:
        import ast
        
        for file_path in files_to_check:
            if not os.path.exists(file_path):
                print(f"⚠️ Файл не найден: {file_path}")
                continue
                
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Проверяем синтаксис
            ast.parse(content)
        
        duration = time.time() - start_time
        print(f"✅ Синтаксис корректен за {duration:.2f}s")
        return True
        
    except SyntaxError as e:
        print(f"❌ Ошибка синтаксиса в {e.filename}:{e.lineno}: {e.msg}")
        return False
    except Exception as e:
        print(f"❌ Ошибка проверки синтаксиса: {e}")
        return False


def main():
    """Основная функция запуска тестов"""
    print("🚀 Запуск тестов стабильности Sirius Group")
    print("=" * 50)
    
    total_start_time = time.time()
    
    # Проверяем синтаксис
    if not test_syntax():
        print("❌ Тесты прерваны из-за ошибок синтаксиса")
        sys.exit(1)
    
    # Проверяем импорты
    if not test_imports():
        print("❌ Тесты прерваны из-за ошибок импорта")
        sys.exit(1)
    
    # Запускаем базовые тесты
    basic_success = run_basic_tests()
    
    # Запускаем интеграционные тесты
    integration_success = run_integration_tests()
    
    total_duration = time.time() - total_start_time
    
    print("=" * 50)
    print(f"⏱️ Общее время выполнения: {total_duration:.2f}s")
    
    if basic_success and integration_success:
        print("🎉 Все тесты пройдены успешно!")
        print("✅ Система стабильна и готова к работе")
        sys.exit(0)
    else:
        print("❌ Некоторые тесты провалены")
        print("🔧 Требуется дополнительная настройка")
        sys.exit(1)


if __name__ == "__main__":
    main()
