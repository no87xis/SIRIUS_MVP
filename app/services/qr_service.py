# MVP: QR-функционал полностью отключен
import logging
from typing import Optional
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class QRService:
    """MVP: Заглушка для QR-сервиса (функционал отключен)"""
    
    @classmethod
    def generate_token(cls) -> str:
        """MVP: Заглушка - не генерирует токены"""
        logger.warning("QR-функционал отключен в MVP")
        return ""
    
    @classmethod
    def generate_qr_payload(cls, order) -> str:
        """MVP: Заглушка - не генерирует QR"""
        logger.warning("QR-функционал отключен в MVP")
        return ""
    
    @classmethod
    def generate_qr_image(cls, order) -> str:
        """MVP: Заглушка - не генерирует изображения"""
        logger.warning("QR-функционал отключен в MVP")
        return ""
    
    @classmethod
    async def generate_qr_image_async(cls, order) -> str:
        """MVP: Заглушка - не генерирует изображения асинхронно"""
        logger.warning("QR-функционал отключен в MVP")
        return ""
    
    @classmethod
    def generate_qr_for_order(cls, db: Session, order) -> bool:
        """MVP: Заглушка - не генерирует QR для заказов"""
        logger.warning("QR-функционал отключен в MVP")
        return True  # Возвращаем True, чтобы не ломать логику
    
    @classmethod
    async def generate_qr_for_order_async(cls, db: Session, order) -> bool:
        """MVP: Заглушка - не генерирует QR для заказов асинхронно"""
        logger.warning("QR-функционал отключен в MVP")
        return True  # Возвращаем True, чтобы не ломать логику
    
    @classmethod
    def get_order_by_qr_token(cls, db: Session, token: str) -> Optional[object]:
        """MVP: Заглушка - не ищет заказы по QR токенам"""
        logger.warning("QR-функционал отключен в MVP")
        return None
    
    @classmethod
    def is_valid_qr_token(cls, token: str) -> bool:
        """MVP: Заглушка - не валидирует QR токены"""
        logger.warning("QR-функционал отключен в MVP")
        return False
    
    @classmethod
    def revoke_qr_token(cls, db: Session, order) -> bool:
        """MVP: Заглушка - не отзывает QR токены"""
        logger.warning("QR-функционал отключен в MVP")
        return True
    
    @classmethod
    def get_qr_image_url(cls, order) -> Optional[str]:
        """MVP: Заглушка - не возвращает URL QR изображений"""
        logger.warning("QR-функционал отключен в MVP")
        return None
    
    @classmethod
    def get_qr_public_url(cls, order) -> Optional[str]:
        """MVP: Заглушка - не возвращает публичные URL QR"""
        logger.warning("QR-функционал отключен в MVP")
        return None