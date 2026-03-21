from django.db import models

class DeliveryType(models.TextChoices):
    PICKUP = "pickup", "Самовывоз"
    DELIVERY = "delivery", "Доставка"


STATUS_CHOICES = [
    ("created", "Создан"),
    ("pending", "Ожидает оплаты"),
    ("paid", "Оплачен"),
    ("delivered", "Доставлен"),
    ("canceled", "Отменен"),
    ("failed", "Ошибка"),
]