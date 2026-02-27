from django.db import models


class PaymentProvider(models.TextChoices):
    MANUAL_TRANSFER = "manual_transfer", "Перевод (вручную)"
    CASH_ON_DELIVERY = "cod", "Оплата при получении"
    MOCK = "mock", "Тестовая оплата"


class PaymentStatus(models.TextChoices):
    PENDING = "pending", "Ожидает оплаты"
    UNDER_REVIEW = "under_review", "На проверке"
    PAID = "paid", "Оплачено"
    FAILED = "failed", "Ошибка"
    CANCELED = "canceled", "Отменено"