#!/usr/bin/env python3
"""
Скрипт запуска FastAPI с автоперезапуском при изменениях
Требует: pip install watchfiles
"""

import sys
import os
import subprocess
from pathlib import Path

def install_watchfiles():
    """Установка watchfiles если не установлен"""
    try:
        import watchfiles
        print("✅ watchfiles уже установлен")
        return True
    except ImportError:
        print("📦 Устанавливаю watchfiles...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "watchfiles"])
            print("✅ watchfiles установлен успешно")
            return True
        except subprocess.CalledProcessError:
            print("❌ Ошибка установки watchfiles")
            return False

def start_server_with_watch():
    """Запуск сервера с автоперезапуском"""
    if not install_watchfiles():
        print("❌ Не удалось установить watchfiles, запускаю обычный сервер")
        os.system("python start_optimized.py")
        return
    
    try:
        from watchfiles import run_process
        
        print("🚀 Запуск FastAPI с автоперезапуском...")
        print("📁 Отслеживаемые папки: app/, tests/")
        print("🔄 Сервер будет перезапускаться при изменении файлов")
        print("🛑 Для остановки нажмите Ctrl+C")
        print("-" * 50)
        
        # Запуск с автоперезапуском
        run_process(
            "app/",
            target="python",
            args=["start_optimized.py"],
            watch_filter=lambda changes: any(
                change[1].endswith(('.py', '.html', '.css', '.js'))
                for change in changes
            )
        )
        
    except ImportError:
        print("❌ watchfiles не установлен, запускаю обычный сервер")
        os.system("python start_optimized.py")
    except KeyboardInterrupt:
        print("\n🛑 Сервер остановлен")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        print("🔄 Запускаю обычный сервер...")
        os.system("python start_optimized.py")

if __name__ == "__main__":
    start_server_with_watch()
