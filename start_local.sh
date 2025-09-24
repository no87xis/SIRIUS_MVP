#!/bin/bash
echo "🚀 Запуск Sirius Group MVP"
cd "$(dirname "$0")"
source .venv/bin/activate
echo "✅ Виртуальное окружение активировано"
echo "🌐 Запуск сервера на http://127.0.0.1:8000"
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
