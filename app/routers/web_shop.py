from fastapi import APIRouter, Depends, HTTPException, Request, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from typing import Optional
import uuid
from app.db import get_db
from app.models import PaymentMethodModel
from app.services.products import get_products
from app.services.shop_cart import ShopCartService
from app.services.shop_orders import ShopOrderService
from app.services.payments import PaymentService
# MVP: QR-функционал отключен
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(prefix="/shop", tags=["shop"])


def get_session_id(request: Request) -> str:
    """Получает или создаёт ID сессии для корзины"""
    session_id = request.session.get("cart_session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
        request.session["cart_session_id"] = session_id
    return session_id


@router.get("/", response_class=HTMLResponse)
async def shop_catalog(
    request: Request,
    db: Session = Depends(get_db)
):
    """Каталог товаров магазина"""
    products = get_products(db)
    
    # Получаем количество товаров в корзине
    session_id = get_session_id(request)
    cart_count = ShopCartService.get_cart_count(db, session_id)
    
    return templates.TemplateResponse("shop/catalog.html", {
        "request": request,
        "products": products,
        "cart_count": cart_count
    })


@router.get("/product/{product_id:int}", response_class=HTMLResponse)
async def shop_product_detail(
    request: Request,
    product_id: int,
    db: Session = Depends(get_db)
):
    """Страница товара в магазине"""
    from app.services.products import get_product
    
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    
    # Получаем количество товаров в корзине
    session_id = get_session_id(request)
    cart_count = ShopCartService.get_cart_count(db, session_id)
    
    return templates.TemplateResponse("shop/product.html", {
        "request": request,
        "product": product,
        "cart_count": cart_count
    })


@router.get("/cart", response_class=HTMLResponse)
async def shop_cart(
    request: Request,
    db: Session = Depends(get_db)
):
    """Корзина магазина"""
    session_id = get_session_id(request)
    cart_summary = ShopCartService.get_cart_summary(db, session_id)
    
    return templates.TemplateResponse("shop/cart.html", {
        "request": request,
        "cart": cart_summary
    })


@router.post("/cart/add")
async def add_to_cart_post(
    request: Request,
    product_id: int = Form(...),
    quantity: int = Form(1),
    db: Session = Depends(get_db)
):
    """Добавляет товар в корзину (POST)"""
    session_id = get_session_id(request)
    
    try:
        from app.schemas.shop_cart import ShopCartCreate
        cart_data = ShopCartCreate(session_id=session_id, product_id=product_id, quantity=quantity)
        result = ShopCartService.add_to_cart(db, cart_data)
        if result:
            return RedirectResponse(url="/shop/cart", status_code=303)
        else:
            return RedirectResponse(url="/shop/cart?error=add_failed", status_code=303)
    except Exception as e:
        return RedirectResponse(url=f"/shop/cart?error={str(e)}", status_code=303)


@router.post("/cart/remove")
async def remove_from_cart_post(
    request: Request,
    product_id: int = Form(...),
    db: Session = Depends(get_db)
):
    """Удаляет товар из корзины (POST)"""
    session_id = get_session_id(request)
    
    try:
        success = ShopCartService.remove_from_cart(db, session_id, product_id)
        return RedirectResponse(url="/shop/cart", status_code=303)
    except Exception as e:
        return RedirectResponse(url=f"/shop/cart?error={str(e)}", status_code=303)


@router.post("/cart/update")
async def update_cart_item_post(
    request: Request,
    product_id: int = Form(...),
    quantity: int = Form(...),
    db: Session = Depends(get_db)
):
    """Обновляет количество товара в корзине (POST)"""
    session_id = get_session_id(request)
    
    try:
        if quantity <= 0:
            # Удаляем товар из корзины
            success = ShopCartService.remove_from_cart(db, session_id, product_id)
            if success:
                return RedirectResponse(url="/shop/cart?success=Товар удалён из корзины", status_code=303)
            else:
                return RedirectResponse(url="/shop/cart?error=Товар не найден в корзине", status_code=303)
        
        # Обновляем количество
        cart_item = ShopCartService.update_cart_item(db, session_id, product_id, quantity)
        if not cart_item:
            return RedirectResponse(url="/shop/cart?error=Товар не найден в корзине", status_code=303)
        
        return RedirectResponse(url="/shop/cart?success=Количество обновлено", status_code=303)
    except Exception as e:
        return RedirectResponse(url=f"/shop/cart?error={str(e)}", status_code=303)


@router.get("/checkout", response_class=HTMLResponse)
async def shop_checkout(
    request: Request,
    db: Session = Depends(get_db)
):
    """Страница оформления заказа"""
    session_id = get_session_id(request)
    cart_summary = ShopCartService.get_cart_summary(db, session_id)
    
    if not cart_summary.items:
        return RedirectResponse(url="/shop/cart", status_code=303)
    
    # Получаем способы оплаты
    payment_methods = db.query(PaymentMethodModel).all()
    
    return templates.TemplateResponse("shop/checkout.html", {
        "request": request,
        "cart": cart_summary,
        "payment_methods": payment_methods
    })


@router.post("/checkout")
async def process_checkout(
    request: Request,
    customer_name: str = Form(...),
    customer_phone: str = Form(...),
    customer_city: str = Form(...),
    delivery_option: str = Form(...),
    delivery_city_other: Optional[str] = Form(None),
    payment_method_id: Optional[int] = Form(None),
    db: Session = Depends(get_db)
):
    """Обрабатывает оформление заказа с системой доставки"""
    session_id = get_session_id(request)
    cart_summary = ShopCartService.get_cart_summary(db, session_id)
    
    if not cart_summary.items:
        return RedirectResponse(url="/shop/cart", status_code=303)
    
    # Проверяем и обрабатываем город и доставку
    final_city = customer_city
    
    # Валидация полей доставки
    if delivery_option == 'COURIER_OTHER' and not delivery_city_other:
        return RedirectResponse(url="/shop/checkout?error=Укажите название города для доставки", status_code=303)
    
    # Устанавливаем город в зависимости от варианта доставки
    if delivery_option == 'COURIER_OTHER' and delivery_city_other:
        final_city = delivery_city_other.strip()
    elif delivery_option == 'SELF_PICKUP_GROZNY':
        final_city = 'Грозный'
    elif delivery_option == 'COURIER_GROZNY':
        final_city = 'Грозный'
    elif delivery_option == 'COURIER_MAK':
        final_city = 'Махачкала'
    elif delivery_option == 'COURIER_KHAS':
        final_city = 'Хасавюрт'
    
    try:
        from app.schemas.shop_order import ShopOrderCreate
        from app.constants.delivery import calculate_delivery_cost
        
        # Рассчитываем стоимость доставки
        delivery_cost = calculate_delivery_cost(delivery_option, cart_summary.total_items)
        
        # Создаем данные заказа
        order_data = ShopOrderCreate(
            customer_name=customer_name,
            customer_phone=customer_phone,
            customer_city=final_city,
            payment_method_id=payment_method_id,
            delivery_option=delivery_option,
            delivery_city_other=delivery_city_other if delivery_option == 'COURIER_OTHER' else None,
            delivery_cost_rub=delivery_cost,
            cart_items=cart_summary.items
        )
        
        # Создаем заказы
        orders = ShopOrderService.create_orders_from_cart(db, order_data)
        
        if orders:
            # Очищаем корзину
            ShopCartService.clear_cart(db, session_id)
            
            # Формируем коды заказов для редиректа
            order_codes = [order.order_code for order in orders]
            codes_param = ','.join(order_codes)
            
            return RedirectResponse(url=f"/shop/order-success?codes={codes_param}", status_code=303)
        else:
            return RedirectResponse(url="/shop/checkout?error=creation_failed", status_code=303)
            
    except Exception as e:
        return RedirectResponse(url=f"/shop/checkout?error={str(e)}", status_code=303)


def generate_whatsapp_message(orders, request, db=None):
    """Генерирует сообщение для WhatsApp"""
    if not orders:
        return "Здравствуйте! У меня есть вопрос по заказу."
    
    message_parts = ["🛍 Заказ в магазине SIRIUS_GROUPE"]
    message_parts.append("")
    message_parts.append("📋 Детали заказа:")
    
    for i, order in enumerate(orders, 1):
        message_parts.append(f"{i}. {order.product_name or 'Товар'}")
        message_parts.append(f"   Количество: {order.qty}")
        message_parts.append(f"   Стоимость: {order.unit_price_rub * order.qty} ₽")
        message_parts.append(f"   Код заказа: {order.order_code}")
        
        # MVP: QR-ссылки отключены
        
        message_parts.append(f"   Ссылка: {request.base_url}orders/{order.order_code}")
        message_parts.append("")
    
    total_amount = sum(order.unit_price_rub * order.qty for order in orders)
    message_parts.append(f"💰 Итого: {total_amount} ₽")
    message_parts.append(f"📱 Телефон: {orders[0].phone if orders else ''}")
    message_parts.append(f"👤 Имя: {orders[0].customer_name if orders else ''}")
    
    # Исправляем отображение города
    city = orders[0].client_city if orders and orders[0].client_city else ''
    if city == 'custom':
        city = 'Не указан'
    message_parts.append(f"🏙 Город: {city}")
    message_parts.append("")
    
    # Добавляем информацию о способе оплаты
    from datetime import datetime, timedelta
    
    # Получаем способ оплаты
    payment_method_name = "не указан"
    if orders and orders[0].payment_method_id:
        # Сначала пробуем получить из relationship
        if hasattr(orders[0], 'payment_method') and orders[0].payment_method:
            payment_method_name = orders[0].payment_method.name
        # Если не получилось, берем из поля payment_method_name
        elif hasattr(orders[0], 'payment_method_name') and orders[0].payment_method_name:
            payment_method_name = orders[0].payment_method_name
        # Если и это не работает, делаем запрос к базе
        elif db:
            try:
                from app.models import PaymentMethod as PaymentMethodEnum
                payment_method = db.query(PaymentMethodModel).filter(PaymentMethodModel.id == orders[0].payment_method_id).first()
                if payment_method:
                    payment_method_name = payment_method.name
            except Exception as e:
                payment_method_name = "не указан"
    
    if orders and hasattr(orders[0], 'created_at') and orders[0].created_at:
        created_at = orders[0].created_at
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
        reserve_until = created_at + timedelta(hours=48)
        message_parts.append(f"⏰ Резерв до {reserve_until.strftime('%H:%M %d.%m.%Y')}")
    else:
        now = datetime.now()
        reserve_until = now + timedelta(hours=48)
        message_parts.append(f"⏰ Резерв до {reserve_until.strftime('%H:%M %d.%m.%Y')}")
    
    message_parts.append(f"💳 Способ оплаты: {payment_method_name}")
    
    return "\n".join(message_parts)


@router.get("/order-success", response_class=HTMLResponse)
async def order_success(
    request: Request,
    codes: str,
    db: Session = Depends(get_db)
):
    """Страница успешного создания заказа"""
    order_codes = codes.split(',')
    
    # Получаем информацию о заказах из основной таблицы Order
    orders = []
    for code in order_codes:
        # Ищем заказ по коду в основной таблице Order
        from app.models import Order
        order = db.query(Order).filter(Order.order_code == code).first()
        if order:
            # MVP: QR-генерация отключена
            orders.append(order)
    
    return templates.TemplateResponse("shop/order-success.html", {
        "request": request,
        "orders": orders,
        "generate_whatsapp_message": generate_whatsapp_message,
        # MVP: QR-сервис отключен
    })


@router.get("/order/{order_code}", response_class=HTMLResponse)
async def view_order(
    request: Request,
    order_code: str,
    db: Session = Depends(get_db)
):
    """Просмотр заказа по коду"""
    from app.models import Order
    order = db.query(Order).filter(Order.order_code == order_code).first()
    
    if not order:
        return templates.TemplateResponse("shop/order-not-found.html", {
            "request": request,
            "order_code": order_code
        })
    
    # MVP: QR-генерация отключена
    
    return templates.TemplateResponse("shop/order-detail.html", {
        "request": request,
        "order": order,
        # MVP: QR-сервис отключен
    })


@router.get("/search-order", response_class=HTMLResponse)
async def search_order_page(request: Request):
    """Страница поиска заказа"""
    return templates.TemplateResponse("shop/search-order.html", {
        "request": request
    })


@router.post("/search-order")
async def search_order_post(
    request: Request,
    order_code: str = Form(...),
    phone: str = Form(...),
    db: Session = Depends(get_db)
):
    """Поиск заказа (POST)"""
    from app.services.orders import get_orders_by_phone
    from app.models import Order
    
    # Ищем заказы по телефону
    orders = get_orders_by_phone(db, phone)
    
    # Фильтруем по коду заказа
    if order_code:
        if len(order_code) == 4:
            # Поиск по последним 4 символам
            orders = [order for order in orders if order.order_code_last4 == order_code]
        else:
            # Поиск по полному коду
            orders = [order for order in orders if order.order_code == order_code]
    
    if not orders:
        return templates.TemplateResponse("shop/search-order.html", {
            "request": request,
            "error": "Заказы не найдены. Проверьте код заказа и номер телефона."
        })
    
    # Если найден один заказ, перенаправляем на его страницу
    if len(orders) == 1:
        return RedirectResponse(
            url=f"/shop/order/{orders[0].order_code}?phone={phone}", 
            status_code=303
        )
    
    # Если найдено несколько заказов, показываем список
    return templates.TemplateResponse("shop/orders-list.html", {
        "request": request,
        "orders": orders,
        "phone": phone
    })

# Публичный роут для доступа по QR-коду
@router.get("/o/{qr_token}", response_class=HTMLResponse)
async def public_order_view(
    request: Request,
    qr_token: str,
    db: Session = Depends(get_db)
):
    """Публичный просмотр заказа по QR-токену (без авторизации)"""
    # MVP: QR-функционал отключен
    return RedirectResponse(url="/shop?info=QR-ссылки отключены в MVP", status_code=302)

