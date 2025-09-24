# Руководство по развертыванию Sirius Group

## 🎯 Стабильная версия для продакшена

### Предварительные требования
- Python 3.8+
- pip
- PostgreSQL (рекомендуется) или SQLite
- nginx (рекомендуется)

## 🚀 Быстрое развертывание

### 1. Клонирование и настройка
```bash
git clone <repository-url>
cd Sirius_sklad_new-master
pip install -r requirements.txt
```

### 2. Проверка готовности
```bash
python quick_check.py
```

### 3. Настройка окружения
```bash
# Создайте .env файл
cp env.example .env

# Отредактируйте .env
nano .env
```

### 4. Запуск
```bash
python start_optimized.py
```

## 🔧 Настройка для продакшена

### Переменные окружения (.env)
```bash
# База данных
DATABASE_URL=postgresql://user:password@localhost/sirius_db

# Безопасность
SECRET_KEY=your-super-secret-key-32-characters-long
ENVIRONMENT=production
DEBUG=false

# Таймауты
STARTUP_TIMEOUT=30
DATABASE_TIMEOUT=5
HTTP_TIMEOUT=10

# Мониторинг
MONITORING_MAX_REQUESTS=1000
MONITORING_MAX_DB_QUERIES=500
MONITORING_MAX_ERRORS=100

# Внешние сервисы (опционально)
ENABLE_EXTERNAL_SERVICES=true
ENABLE_TELEGRAM=true
ENABLE_EMAIL=true
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_CHAT_ID=your-chat-id
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-password
```

### Настройка PostgreSQL
```sql
-- Создание базы данных
CREATE DATABASE sirius_db;
CREATE USER sirius_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE sirius_db TO sirius_user;
```

### Настройка nginx
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/Sirius_sklad_new-master/app/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

## 🐧 Настройка systemd (Linux)

### Создание сервиса
```bash
sudo nano /etc/systemd/system/sirius.service
```

### Содержимое сервиса
```ini
[Unit]
Description=Sirius Group Warehouse Management System
After=network.target postgresql.service

[Service]
Type=simple
User=sirius
Group=sirius
WorkingDirectory=/path/to/Sirius_sklad_new-master
Environment=PATH=/path/to/Sirius_sklad_new-master/venv/bin
ExecStart=/path/to/Sirius_sklad_new-master/venv/bin/python start_optimized.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Управление сервисом
```bash
# Включение автозапуска
sudo systemctl enable sirius

# Запуск сервиса
sudo systemctl start sirius

# Проверка статуса
sudo systemctl status sirius

# Просмотр логов
sudo journalctl -u sirius -f
```

## 🪟 Настройка Windows Service

### Использование NSSM
```bash
# Скачайте NSSM с https://nssm.cc/
# Установите сервис
nssm install SiriusService "C:\Python\python.exe" "C:\path\to\Sirius_sklad_new-master\start_optimized.py"

# Настройте автозапуск
nssm set SiriusService Start SERVICE_AUTO_START

# Запустите сервис
nssm start SiriusService
```

## 📊 Мониторинг

### Health-check
```bash
# Проверка состояния
curl http://your-domain.com/health

# Ожидаемый ответ
{
  "status": "ok",
  "version": "1.0.0",
  "database": "connected",
  "timestamp": 1234567890.123
}
```

### Логи
```bash
# Просмотр логов
tail -f logs/sirius_*.log

# Поиск ошибок
grep "ERROR" logs/sirius_*.log

# Статистика запросов
grep "HTTP" logs/sirius_*.log | wc -l
```

### Метрики
- **URL**: `/admin/metrics`
- **Время работы**: uptime
- **Запросы**: количество и время ответа
- **Ошибки**: типы и количество
- **База данных**: время запросов

## 🔒 Безопасность

### Рекомендации
1. **Используйте HTTPS** - настройте SSL сертификат
2. **Смените SECRET_KEY** - сгенерируйте уникальный ключ
3. **Ограничьте доступ** - используйте firewall
4. **Регулярные обновления** - обновляйте зависимости
5. **Бэкапы** - регулярно делайте резервные копии

### Генерация SECRET_KEY
```python
import secrets
print(secrets.token_urlsafe(32))
```

## 💾 Бэкапы

### Автоматический бэкап БД
```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump sirius_db > backup_$DATE.sql
gzip backup_$DATE.sql
```

### Восстановление из бэкапа
```bash
gunzip backup_20241219_120000.sql.gz
psql sirius_db < backup_20241219_120000.sql
```

## 🚨 Troubleshooting

### Проблемы запуска
1. **Проверьте логи**: `sudo journalctl -u sirius -f`
2. **Проверьте порт**: `netstat -tlnp | grep 8000`
3. **Проверьте права**: `ls -la /path/to/Sirius_sklad_new-master`

### Проблемы производительности
1. **Проверьте мониторинг**: `/admin/metrics`
2. **Проверьте БД**: `SELECT * FROM pg_stat_activity;`
3. **Проверьте память**: `free -h`

### Проблемы с БД
1. **Проверьте подключение**: `psql -h localhost -U sirius_user -d sirius_db`
2. **Проверьте права**: `GRANT ALL PRIVILEGES ON DATABASE sirius_db TO sirius_user;`
3. **Проверьте логи PostgreSQL**: `/var/log/postgresql/postgresql-*.log`

## 📈 Масштабирование

### Горизонтальное масштабирование
1. **Load balancer** - nginx с несколькими инстансами
2. **База данных** - PostgreSQL с репликацией
3. **Кэширование** - Redis для сессий
4. **Статические файлы** - CDN

### Вертикальное масштабирование
1. **Увеличение RAM** - для кэширования
2. **SSD диски** - для БД
3. **CPU** - для обработки запросов

## ✅ Чек-лист развертывания

- [ ] Python 3.8+ установлен
- [ ] Зависимости установлены (`pip install -r requirements.txt`)
- [ ] База данных настроена
- [ ] Переменные окружения настроены
- [ ] SECRET_KEY изменен
- [ ] nginx настроен (опционально)
- [ ] systemd сервис создан (Linux)
- [ ] Автозапуск настроен
- [ ] Мониторинг работает
- [ ] Бэкапы настроены
- [ ] SSL сертификат установлен (опционально)
- [ ] Firewall настроен
- [ ] Логи ротируются

---

**Система готова к продакшену! 🚀**
