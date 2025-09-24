#!/usr/bin/env python3
"""
Минимальная версия приложения для тестирования
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# Создаем простое приложение
app = FastAPI(title="Sirius Test", version="1.0.0")

@app.get("/")
async def root():
    """Главная страница"""
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sirius Test</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>🚀 Sirius Test Server</h1>
        <p>Сервер работает!</p>
        <p>Время: <span id="time"></span></p>
        <script>
            document.getElementById('time').textContent = new Date().toLocaleString();
        </script>
    </body>
    </html>
    """)

@app.get("/health")
async def health():
    """Проверка здоровья"""
    return {"status": "ok", "message": "Сервер работает"}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Запуск минимального сервера...")
    uvicorn.run("app_minimal_test:app", host="127.0.0.1", port=8000, reload=True)
