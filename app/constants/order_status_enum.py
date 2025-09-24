import enum

class OrderStatus(str, enum.Enum):
    # MVP: Только 4 статуса заказов
    UNPAID = "unpaid"                   # Не оплачен
    PAID_NOT_ISSUED = "paid_not_issued" # Оплачен, не выдан
    PAID_ISSUED = "paid_issued"         # Оплачен и выдан
    COURIER_NOT_PAID = "courier_not_paid" # Курьер не оплачен




