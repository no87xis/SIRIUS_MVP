import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool, QueuePool
from .config import settings

logger = logging.getLogger(__name__)

# Настройки connection pooling в зависимости от типа БД
if "sqlite" in settings.database_url:
    # SQLite - используем StaticPool для thread safety
    engine = create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=settings.debug,
        pool_pre_ping=True,  # Проверка соединений перед использованием
        pool_recycle=settings.database_pool_recycle
    )
else:
    # PostgreSQL/MySQL - используем QueuePool
    engine = create_engine(
        settings.database_url,
        poolclass=QueuePool,
        pool_size=settings.database_pool_size,
        max_overflow=settings.database_max_overflow,
        pool_timeout=settings.database_pool_timeout,
        pool_recycle=settings.database_pool_recycle,
        pool_pre_ping=True,
        echo=settings.debug
    )

# Create SessionLocal class
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine,
    expire_on_commit=False  # Предотвращает lazy loading issues
)

# Create Base class
Base = declarative_base()


def get_db():
    """Dependency to get database session with error handling"""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def get_db_sync():
    """Synchronous database session for non-async contexts"""
    return SessionLocal()


def close_db_connections():
    """Close all database connections (for shutdown)"""
    try:
        engine.dispose()
        logger.info("Database connections closed")
    except Exception as e:
        logger.error(f"Error closing database connections: {e}")
