import logging
import sys
import os
from datetime import datetime
from pathlib import Path
from logging.handlers import RotatingFileHandler
from ..config import settings


class LoggerService:
    """Централизованная система логирования с ленивой инициализацией"""
    
    def __init__(self):
        self.logger = logging.getLogger("sirius")
        self.logger.setLevel(logging.INFO)
        self._initialized = False
        self._file_handler = None
        self._console_handler = None
    
    def _ensure_initialized(self):
        """Ленивая инициализация логгера"""
        if self._initialized:
            return
        
        try:
            # Создаем директорию для логов только при необходимости
            log_dir = Path("logs")
            if not log_dir.exists():
                log_dir.mkdir(exist_ok=True)
            
            # Форматтер для логов
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            
            # Хендлер для файла с ротацией
            log_file = log_dir / f"sirius_{datetime.now().strftime('%Y%m%d')}.log"
            self._file_handler = RotatingFileHandler(
                log_file,
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5,
                encoding='utf-8'
            )
            self._file_handler.setFormatter(formatter)
            self._file_handler.setLevel(logging.INFO)
            
            # Хендлер для консоли
            self._console_handler = logging.StreamHandler(sys.stdout)
            self._console_handler.setFormatter(formatter)
            self._console_handler.setLevel(logging.INFO if not settings.debug else logging.DEBUG)
            
            # Добавляем хендлеры
            self.logger.addHandler(self._file_handler)
            self.logger.addHandler(self._console_handler)
            
            # Отключаем дублирование логов
            self.logger.propagate = False
            
            self._initialized = True
            
        except Exception as e:
            # Если не удалось инициализировать файловое логирование, используем только консоль
            print(f"Warning: Failed to initialize file logging: {e}")
            self._console_handler = logging.StreamHandler(sys.stdout)
            self._console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(self._console_handler)
            self._initialized = True
    
    def info(self, message: str, **kwargs):
        """Информационное сообщение"""
        self._ensure_initialized()
        self.logger.info(message, extra=kwargs)
    
    def error(self, message: str, **kwargs):
        """Сообщение об ошибке"""
        self._ensure_initialized()
        self.logger.error(message, extra=kwargs)
    
    def warning(self, message: str, **kwargs):
        """Предупреждение"""
        self._ensure_initialized()
        self.logger.warning(message, extra=kwargs)
    
    def debug(self, message: str, **kwargs):
        """Отладочное сообщение"""
        if settings.debug:
            self._ensure_initialized()
            self.logger.debug(message, extra=kwargs)
    
    def log_request(self, request: dict, user_id: str = None):
        """Логирование HTTP запросов"""
        self.info(
            f"HTTP {request.get('method', 'UNKNOWN')} {request.get('url', 'UNKNOWN')}",
            user_id=user_id,
            ip=request.get('client', 'UNKNOWN'),
            user_agent=request.get('headers', {}).get('user-agent', 'UNKNOWN')
        )
    
    def log_error(self, error: Exception, context: str = "", user_id: str = None):
        """Логирование ошибок"""
        self.error(
            f"Ошибка в {context}: {str(error)}",
            error_type=type(error).__name__,
            user_id=user_id,
            traceback=str(error)
        )
    
    def log_database_operation(self, operation: str, table: str, user_id: str = None):
        """Логирование операций с БД"""
        self.info(
            f"DB операция: {operation} в таблице {table}",
            operation=operation,
            table=table,
            user_id=user_id
        )
    
    def close(self):
        """Закрытие логгера и освобождение ресурсов"""
        if self._file_handler:
            self._file_handler.close()
        if self._console_handler:
            self._console_handler.close()
        self._initialized = False


# Создаем глобальный экземпляр логгера
logger = LoggerService()
