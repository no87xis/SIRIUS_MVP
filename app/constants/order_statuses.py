from .order_status_enum import OrderStatus

# MVP: Отображаемые названия статусов (только 4 статуса)
ORDER_STATUS_DISPLAY = {
    OrderStatus.UNPAID: "Не оплачен",
    OrderStatus.PAID_NOT_ISSUED: "Оплачен, не выдан",
    OrderStatus.PAID_ISSUED: "Оплачен и выдан",
    OrderStatus.COURIER_NOT_PAID: "Курьер не оплачен"
}

# MVP: Цвета для статусов (только 4 статуса)
ORDER_STATUS_COLORS = {
    OrderStatus.UNPAID: "bg-red-100 text-red-800",
    OrderStatus.PAID_NOT_ISSUED: "bg-orange-100 text-orange-800",
    OrderStatus.PAID_ISSUED: "bg-green-100 text-green-800",
    OrderStatus.COURIER_NOT_PAID: "bg-purple-100 text-purple-800"
}

# MVP: Иконки для статусов (только 4 статуса)
ORDER_STATUS_ICONS = {
    OrderStatus.UNPAID: "fas fa-times-circle",
    OrderStatus.PAID_NOT_ISSUED: "fas fa-check-circle",
    OrderStatus.PAID_ISSUED: "fas fa-check-double",
    OrderStatus.COURIER_NOT_PAID: "fas fa-motorcycle"
}

def get_status_display(status: OrderStatus) -> str:
    """Получает отображаемое название статуса"""
    return ORDER_STATUS_DISPLAY.get(status, str(status))

def get_status_color(status: OrderStatus) -> str:
    """Получает CSS классы для цвета статуса"""
    return ORDER_STATUS_COLORS.get(status, "bg-gray-100 text-gray-800")

def get_status_icon(status: OrderStatus) -> str:
    """Получает иконку для статуса"""
    return ORDER_STATUS_ICONS.get(status, "fas fa-question")

def get_all_statuses() -> list:
    """MVP: Получает список всех статусов для фильтрации (только 4 статуса)"""
    return [
        (OrderStatus.UNPAID, get_status_display(OrderStatus.UNPAID)),
        (OrderStatus.PAID_NOT_ISSUED, get_status_display(OrderStatus.PAID_NOT_ISSUED)),
        (OrderStatus.PAID_ISSUED, get_status_display(OrderStatus.PAID_ISSUED)),
        (OrderStatus.COURIER_NOT_PAID, get_status_display(OrderStatus.COURIER_NOT_PAID))
    ]

