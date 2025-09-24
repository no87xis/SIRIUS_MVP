# Развертывание Sirius Group MVP

## 🚀 Быстрое развертывание

### 1. Подготовка окружения

#### Windows
```cmd
# Клонирование репозитория
git clone <repository-url>
cd Sirius_sklad_new-master

# Установка Python зависимостей
pip install -r requirements.txt

# Проверка готовности
python quick_check.py
```

#### Linux/macOS
```bash
# Клонирование репозитория
git clone <repository-url>
cd Sirius_sklad_new-master

# Установка Python зависимостей
pip3 install -r requirements.txt

# Проверка готовности
python3 quick_check.py
```

### 2. Запуск сервера

#### Разработка
```bash
python start_optimized.py
```

#### Продакшн
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1
```

## ⚙️ Конфигурация

### env.mvp (по умолчанию)
```env
# Database
DATABASE_URL=sqlite:///./sirius.db

# Security
SECRET_KEY=mvp-secret-key-32-characters-long-2024
SESSION_MAX_AGE=86400

# Environment
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO
```

### .env (продакшн)
```env
# Database
DATABASE_URL=sqlite:///./sirius.db

# Security
SECRET_KEY=your-secure-secret-key-32-characters-minimum
SESSION_MAX_AGE=86400

# Environment
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=WARNING
```

## 🐳 Docker развертывание

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  sirius-mvp:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./sirius.db:/app/sirius.db
      - ./logs:/app/logs
    environment:
      - DATABASE_URL=sqlite:///./sirius.db
      - SECRET_KEY=your-secure-secret-key-32-characters-minimum
      - ENVIRONMENT=production
      - DEBUG=false
    restart: unless-stopped
```

### Запуск с Docker
```bash
# Сборка и запуск
docker-compose up -d

# Проверка статуса
docker-compose ps

# Просмотр логов
docker-compose logs -f
```

## 🔧 Настройка веб-сервера

### Nginx (рекомендуется)
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

    location /static/ {
        alias /path/to/Sirius_sklad_new-master/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### Apache
```apache
<VirtualHost *:80>
    ServerName your-domain.com
    
    ProxyPreserveHost On
    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/
    
    Alias /static /path/to/Sirius_sklad_new-master/static
    <Directory /path/to/Sirius_sklad_new-master/static>
        Require all granted
    </Directory>
</VirtualHost>
```

## 📊 Мониторинг

### Health Check
```bash
# Проверка статуса
curl http://localhost:8000/health

# Ожидаемый ответ
{
  "status": "ok",
  "version": "1.0.0",
  "database": "connected",
  "timestamp": "2024-12-19T10:30:00Z"
}
```

### Логи
```bash
# Просмотр логов
tail -f logs/sirius_$(date +%Y%m%d).log

# Поиск ошибок
grep "ERROR" logs/sirius_*.log

# Статистика запросов
grep "HTTP" logs/sirius_*.log | wc -l
```

### Мониторинг ресурсов
```bash
# Использование памяти
ps aux | grep uvicorn

# Использование диска
du -sh sirius.db logs/

# Сетевые соединения
netstat -tulpn | grep :8000
```

## 🔒 Безопасность

### Настройки безопасности
1. **Смените SECRET_KEY** в продакшн
2. **Ограничьте доступ** к админ-панели
3. **Настройте HTTPS** через reverse proxy
4. **Регулярно обновляйте** зависимости

### Firewall
```bash
# Разрешить только HTTP/HTTPS
ufw allow 80
ufw allow 443
ufw deny 8000  # Прямой доступ к приложению
```

### SSL сертификат
```bash
# Let's Encrypt
certbot --nginx -d your-domain.com
```

## 📈 Масштабирование

### Горизонтальное масштабирование
```yaml
# docker-compose.yml
services:
  sirius-mvp:
    build: .
    ports:
      - "8000-8002:8000"
    deploy:
      replicas: 3
    environment:
      - DATABASE_URL=sqlite:///./sirius.db
```

### Load Balancer
```nginx
upstream sirius_backend {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

server {
    location / {
        proxy_pass http://sirius_backend;
    }
}
```

## 🔄 Обновление

### Обновление кода
```bash
# Остановка сервиса
systemctl stop sirius-mvp

# Обновление кода
git pull origin main

# Установка зависимостей
pip install -r requirements.txt

# Запуск сервиса
systemctl start sirius-mvp
```

### Обновление с Docker
```bash
# Обновление образа
docker-compose pull

# Перезапуск сервиса
docker-compose up -d
```

## 🚨 Устранение неполадок

### Проблема: Сервер не запускается
```bash
# Проверка логов
journalctl -u sirius-mvp -f

# Проверка портов
netstat -tulpn | grep :8000

# Проверка зависимостей
python quick_check.py
```

### Проблема: База данных заблокирована
```bash
# Проверка процессов
lsof sirius.db

# Перезапуск сервиса
systemctl restart sirius-mvp
```

### Проблема: Медленная работа
```bash
# Проверка ресурсов
htop
iostat 1

# Оптимизация SQLite
sqlite3 sirius.db "VACUUM;"
```

## 📋 Чек-лист развертывания

### Перед запуском
- [ ] Python 3.8+ установлен
- [ ] Зависимости установлены
- [ ] Конфигурация настроена
- [ ] Права доступа настроены
- [ ] Firewall настроен

### После запуска
- [ ] Health check проходит
- [ ] Основные страницы доступны
- [ ] Логи записываются
- [ ] Мониторинг работает
- [ ] Резервное копирование настроено

### Регулярные задачи
- [ ] Мониторинг логов
- [ ] Резервное копирование БД
- [ ] Обновление зависимостей
- [ ] Проверка безопасности
- [ ] Мониторинг производительности

---

**Sirius Group MVP** - Готов к развертыванию! 🚀
