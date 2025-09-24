# 🚀 Настройка локального окружения Sirius Group MVP

## ⚠️ ПРОБЛЕМА С ТЕРМИНАЛОМ

Обнаружена проблема с терминалом - команды Python не выполняются из-за префикса "qс". 

## 🔧 РЕШЕНИЕ

### Вариант 1: Исправление терминала
1. Откройте новый терминал PowerShell
2. Перейдите в папку проекта:
   ```powershell
   cd "D:\!РАЗРАБОТКА ПО\Sirius_sklad_new-master"
   ```
3. Проверьте Python:
   ```powershell
   python --version
   ```

### Вариант 2: Использование VS Code
1. Откройте проект в VS Code
2. Откройте терминал (Ctrl+`)
3. Выполните команды ниже

## 📋 ПОШАГОВАЯ НАСТРОЙКА

### Шаг 1: Диагностика окружения
```bash
python diagnose_environment.py
```

### Шаг 2: Создание виртуального окружения
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Шаг 3: Установка зависимостей
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Шаг 4: Настройка конфигурации
```bash
# Копируем MVP конфигурацию
copy env.mvp .env
```

### Шаг 5: Проверка импортов
```bash
python -c "from app.main import app; print('Imports OK')"
```

### Шаг 6: Запуск сервера
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Шаг 7: Проверка health
```bash
curl http://127.0.0.1:8000/health
```

## 🎯 ОЖИДАЕМЫЕ РЕЗУЛЬТАТЫ

- **Python**: >= 3.10
- **Git**: Установлен
- **Структура проекта**: Все файлы на месте
- **Сервер**: Запущен на http://127.0.0.1:8000
- **Health**: {"status":"ok"}

## 🚨 ЕСЛИ ЧТО-ТО НЕ РАБОТАЕТ

### Python не найден:
```bash
# Windows (PowerShell от администратора)
winget install Python.Python.3

# Или скачайте с python.org
```

### Git не найден:
```bash
# Windows
winget install Git.Git

# Или скачайте с git-scm.com
```

### Порт занят:
```bash
# Попробуйте другой порт
uvicorn app.main:app --host 127.0.0.1 --port 8010 --reload
```

## 📞 ПОДДЕРЖКА

Если проблемы продолжаются:
1. Проверьте, что Python установлен в PATH
2. Перезапустите терминал
3. Используйте VS Code терминал
4. Проверьте права доступа к папке

---

**Выполните команды выше для настройки локального окружения!** 🚀
