# 📋 ИНСТРУКЦИЯ ДЛЯ ПРОГРАММИСТА — Доступ к серверу и управление проектом

## 🔐 Данные для подключения к серверу

### Вариант A — root по паролю
```bash
ssh root@185.239.50.157
# Пароль: uSH51YfTKa2h342Cef
```

Альтернатива с авто-приятием ключа:
```bash
sshpass -p 'uSH51YfTKa2h342Cef' ssh -o StrictHostKeyChecking=no root@185.239.50.157
```

Дополнительно (как вариант пароля, если потребуется):
```text
root
4w7cG1VN8ypzW3wYW5  # пароль на сервер
```

### Вариант B — пользователь deploy по SSH-ключу (рекомендовано)
```text
Сервер: 185.239.50.157
Пользователь: deploy
SSH-ключ: ~/.ssh/id_ed25519
```

> Примечание: если вход по паролю для root отключён, используйте `deploy` + ключ.

---

## 📁 Структура проекта и окружение

Переход в директорию проекта:
```bash
cd /root/New_Shop_Cursor
```

Активация виртуального окружения:
```bash
source venv/bin/activate
```

---

## 🚀 Управление сервером приложения

Остановка текущего процесса:
```bash
pkill -f uvicorn
```

Запуск в фоновом режиме:
```bash
nohup python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &
```

Проверка статуса:
```bash
ps aux | grep uvicorn
```

Просмотр логов:
```bash
# Последние 50 строк
tail -50 server.log

# Мониторинг в реальном времени
tail -f server.log
```

Доступ к сайту:
```text
Основной сайт: http://185.239.50.157:8000/shop/
Корзина:       http://185.239.50.157:8000/cart/
Оформление:    http://185.239.50.157:8000/shop/checkout
API корзины:   http://185.239.50.157:8000/api/shop/cart/items
```

---

## 🔧 Текущие задачи

1) Корзина не отображает товары в браузере
- Статус: API работает, сессии создаются, JavaScript корректный
- Гипотеза: блокировка выполнения JS в браузере (CORS/политики)
- Файлы: `app/routers/web_cart.py`

2) QR-коды для заказов
- Статус: код реализован, требуется тестирование
- Файлы: `app/services/qr_service.py`, `app/routers/order_tracking_api.py`

Текущее состояние:
- ✅ Работает: магазин, API корзины (добавление/удаление), сессии, PostgreSQL, код QR
- ❌ Требует: отображение товаров в корзине (браузер), тесты QR, финальное e2e тестирование заказа

---

## 🗄️ База данных PostgreSQL (в Docker)

Параметры:
```text
Контейнер: postgres16
База данных: appdb
Пользователь: appuser
Пароль: bd4a73a37cab06a21c929b8a46c6f78a894d556d448c9dbd
Доступ: 127.0.0.1:5432 (только локально)

Конфигурация: /home/deploy/postgres/
Данные:       /home/deploy/postgres/data/
Пароли:       /home/deploy/postgres/.env
```

Управление контейнером:
```bash
# Запуск
docker start postgres16

# Остановка
docker stop postgres16

# Логи
docker logs -f postgres16
```

Подключение к psql внутри контейнера:
```bash
docker exec -it postgres16 psql -U appuser -d appdb
```

SSH-туннель для локального доступа к БД:
```bash
# Запуск туннеля (требует настроенного ssh-конфига/доступа)
ssh -f -N maps-db

# Проверка подключения через локальный порт
PGPASSWORD=bd4a73a37cab06a21c929b8a46c6f78a894d556d448c9dbd \
psql -h 127.0.0.1 -p 5432 -U appuser -d appdb
```

Проверка API корзины через curl (нужен валидный session_id):
```bash
# Получение содержимого корзины
curl -X GET "http://185.239.50.157:8000/api/shop/cart/items" -H "Cookie: session_id=YOUR_SESSION_ID"

# Добавление товара
curl -X POST "http://185.239.50.157:8000/api/shop/cart/add?product_id=1&quantity=1" -H "Cookie: session_id=YOUR_SESSION_ID"
```

Полезные списки файлов:
```bash
ls -la app/routers/
ls -la app/services/
ls -la app/models/
```

---

## 🔒 Важные замечания по безопасности

- Всегда работайте в виртуальном окружении: `source venv/bin/activate`
- Перед изменениями делайте резервные копии файлов и БД
- Проверяйте `server.log` при ошибках
- Тестируйте в реальном браузере, не только через `curl`
- Root-вход по паролю может быть отключён; предпочтителен `deploy` + SSH-ключ
- PostgreSQL доступен только локально (127.0.0.1:5432)
- Пароли хранятся в `.env` на сервере
- Для удалённого доступа к БД используйте SSH-туннель

Контакты/контекст:
```text
Сервер: 185.239.50.157:8000
Проект: Sirius Group V2 — Интернет-магазин
Технологии: FastAPI, PostgreSQL, Python, JavaScript, Tailwind CSS
```

