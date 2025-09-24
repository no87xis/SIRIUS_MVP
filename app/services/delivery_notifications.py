# MVP: Уведомления полностью отключены
import logging
from typing import List, Optional
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class DeliveryNotificationService:
    """MVP: Заглушка для сервиса уведомлений о доставке (функционал отключен)"""
    
    @staticmethod
    def get_upcoming_deliveries(db: Session, days_ahead: int = 5) -> List[dict]:
        """MVP: Заглушка - не возвращает уведомления о предстоящих доставках"""
        logger.warning("Уведомления отключены в MVP")
        return []
    
    @staticmethod
    def get_overdue_deliveries(db: Session) -> List[dict]:
        """MVP: Заглушка - не возвращает просроченные доставки"""
        logger.warning("Уведомления отключены в MVP")
        return []
    
    @staticmethod
    def send_delivery_notifications(db: Session, delivery_ids: List[int]) -> dict:
        """MVP: Заглушка - не отправляет уведомления"""
        logger.warning("Уведомления отключены в MVP")
        return {"success": False, "message": "Уведомления отключены в MVP"}
    
    @staticmethod
    def mark_delivery_as_delivered(db: Session, delivery_id: int) -> bool:
        """MVP: Заглушка - не отмечает доставки как выполненные"""
        logger.warning("Уведомления отключены в MVP")
        return False