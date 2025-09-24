# MVP: Уведомления полностью отключены
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from ..db import get_db

router = APIRouter()


@router.get("/admin/delivery-notifications")
async def delivery_notifications_page(request: Request, db: Session = Depends(get_db)):
    """MVP: Уведомления отключены"""
    return RedirectResponse(url="/admin?error=Уведомления отключены в MVP", status_code=302)


@router.post("/admin/delivery-notifications/send")
async def send_delivery_notifications(request: Request, db: Session = Depends(get_db)):
    """MVP: Отправка уведомлений отключена"""
    return RedirectResponse(url="/admin?error=Уведомления отключены в MVP", status_code=302)


@router.post("/admin/delivery-notifications/mark-delivered")
async def mark_delivered(request: Request, db: Session = Depends(get_db)):
    """MVP: Отметка доставки отключена"""
    return RedirectResponse(url="/admin?error=Уведомления отключены в MVP", status_code=302)