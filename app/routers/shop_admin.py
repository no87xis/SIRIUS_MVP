from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import Optional
from app.db import get_db
from app.services.shop_orders import ShopOrderService
# MVP: QR-функционал отключен
from app.models import ShopOrderStatus
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(prefix="/shop/admin", tags=["shop_admin"])


@router.get("/orders", response_class=HTMLResponse)
async def shop_admin_orders(
    request: Request,
    status_filter: Optional[str] = None,
    phone_search: Optional[str] = None,
    code_search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Страница управления заказами магазина (админка)"""
    # Получаем все заказы
    orders = ShopOrderService.get_recent_orders(db, limit=1000)
    
    # Фильтрация по статусу
    if status_filter:
        orders = [order for order in orders if order.status == status_filter]
    
    # Фильтрация по телефону
    if phone_search:
        orders = [order for order in orders if phone_search.lower() in order.customer_phone.lower()]
    
    # Фильтрация по коду заказа
    if code_search:
        orders = [order for order in orders if code_search.upper() == order.order_code.upper()]
    
    # Получаем аналитику
    analytics = ShopOrderService.get_analytics(db)
    
    return templates.TemplateResponse("shop/admin/orders.html", {
        "request": request,
        "orders": orders,
        "analytics": analytics,
        "status_filter": status_filter,
        "phone_search": phone_search,
        "code_search": code_search,
            # MVP: QR-сервис отключен
    })


@router.get("/orders/{order_id:int}", response_class=HTMLResponse)
async def shop_admin_order_detail(
    request: Request,
    order_id: int,
    db: Session = Depends(get_db)
):
    """Страница детального просмотра заказа магазина (админка)"""
    from app.models import ShopOrder
    order = db.query(ShopOrder).filter(ShopOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    
    # QR функционал удалён
    
    return templates.TemplateResponse("shop/admin/order-detail.html", {
        "request": request,
        "order": order,
            # MVP: QR-сервис отключен
    })


@router.post("/orders/{order_id:int}/reserve")
async def shop_admin_reserve_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    """Резервирует товар для заказа (API)"""
    try:
        success = ShopOrderService.reserve_product_on_payment(db, order_id)
        return {"success": success}
    except Exception as e:
        return {"success": False, "message": f"Ошибка: {str(e)}"}


    # QR роуты удалены
