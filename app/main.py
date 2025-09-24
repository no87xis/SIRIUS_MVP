import asyncio
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from .config import settings
from .db import engine, Base, get_db, close_db_connections
from .services.auth import get_current_user_optional
from .services.logger import logger

# Ленивые импорты роутеров для быстрого старта (MVP: без QR и уведомлений)
def _import_routers():
    """Ленивый импорт роутеров"""
    from .routers import (
        web_public, web_products, web_orders, web_analytics, 
        web_admin_panel, api, web_shop, shop_api, shop_admin, 
        delivery_payment
    )
    return {
        'web_public': web_public,
        'web_products': web_products,
        'web_orders': web_orders,
        'web_analytics': web_analytics,
        'web_admin_panel': web_admin_panel,
        'api': api,
        'web_shop': web_shop,
        'shop_api': shop_api,
        'shop_admin': shop_admin,
        'delivery_payment': delivery_payment
    }

# Логирование уже настроено в services.logger

# Create FastAPI app
app = FastAPI(
    title="Сириус - Система учёта склада",
    description="Веб-приложение для управления складом, заказами и поставками",
    version="1.0.0"
)

# Startup event - создание таблиц с таймаутом
@app.on_event("startup")
async def startup_event():
    """Инициализация приложения при запуске"""
    try:
        logger.info("Запуск инициализации приложения...")
        
        # Создание таблиц с таймаутом
        await asyncio.wait_for(
            asyncio.get_event_loop().run_in_executor(
                None, lambda: Base.metadata.create_all(bind=engine)
            ),
            timeout=settings.startup_timeout
        )
        
        # Ленивая загрузка роутеров
        routers = _import_routers()
        
        # Подключение роутеров (MVP: без QR и уведомлений)
        app.include_router(routers['web_public'].router)
        app.include_router(routers['web_products'].router)
        app.include_router(routers['web_orders'].router)
        app.include_router(routers['web_analytics'].router, prefix="/admin")
        app.include_router(routers['web_admin_panel'].router)
        app.include_router(routers['api'].router, prefix="/api")
        app.include_router(routers['shop_api'].router)
        app.include_router(routers['web_shop'].router)
        app.include_router(routers['shop_admin'].router)
        app.include_router(routers['delivery_payment'].router)
        
        logger.info("✅ Таблицы базы данных созданы успешно")
        logger.info("✅ Роутеры подключены успешно")
        
    except asyncio.TimeoutError:
        logger.error("❌ Таймаут при создании таблиц БД")
        raise
    except Exception as e:
        logger.error(f"❌ Ошибка при инициализации: {e}")
        raise

# Shutdown event - graceful shutdown
@app.on_event("shutdown")
async def shutdown_event():
    """Корректное завершение работы приложения"""
    logger.info("Завершение работы приложения...")
    try:
        # Закрываем соединения с БД
        close_db_connections()
        logger.info("✅ Graceful shutdown завершен")
    except Exception as e:
        logger.error(f"❌ Ошибка при shutdown: {e}")
    finally:
        # Закрываем логгер
        logger.close()

# Add session middleware
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.secret_key,
    max_age=settings.session_max_age,
    same_site="lax",  # Улучшенная совместимость с браузерами
    https_only=False  # Разрешаем HTTP для локальной разработки
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Роутеры подключаются в startup event для быстрого старта

# Роуты для основных страниц
@app.get("/")
async def root(request: Request, db: Session = Depends(get_db)):
    """Главная страница"""
    current_user = get_current_user_optional(request, db)
    return templates.TemplateResponse("index.html", {"request": request, "current_user": current_user})


@app.get("/health")
async def health_check():
    """Проверка здоровья приложения с проверкой зависимостей"""
    try:
        # Быстрая проверка БД с таймаутом
        await asyncio.wait_for(
            asyncio.get_event_loop().run_in_executor(
                None,
                lambda: (
                    (lambda conn: (conn.execute(text("SELECT 1")), conn.close()))(
                        engine.connect()
                    )
                )
            ),
            timeout=2.0  # 2 секунды таймаут
        )
        
        return {
            "status": "ok",
            "version": "1.0.0",
            "database": "connected",
            "timestamp": asyncio.get_event_loop().time()
        }
        
    except asyncio.TimeoutError:
        logger.warning("Health check: таймаут подключения к БД")
        return {
            "status": "degraded",
            "version": "1.0.0", 
            "database": "timeout",
            "timestamp": asyncio.get_event_loop().time()
        }
    except Exception as e:
        logger.error(f"Health check: ошибка БД - {e}")
        return {
            "status": "error",
            "version": "1.0.0",
            "database": "error",
            "error": str(e),
            "timestamp": asyncio.get_event_loop().time()
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
