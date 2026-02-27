import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone

from pay.choices import PaymentProvider, PaymentStatus
from orders.models import Order


class Payment(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Заказ",
    )

    reference = models.CharField(
        "Код платежа",
        max_length=16,
        unique=True,
        editable=False,
        db_index=True,
    )

    provider = models.CharField(
        "Провайдер",
        max_length=32,
        choices=PaymentProvider.choices,
        default=PaymentProvider.MANUAL_TRANSFER,
    )
    status = models.CharField(
        "Статус",
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        db_index=True,
    )

    amount = models.DecimalField("Сумма", max_digits=10, decimal_places=2)
    currency = models.CharField("Валюта", max_length=3, default="KGS")

    provider_ref = models.CharField(
        "ID у провайдера",
        max_length=128,
        null=True,
        blank=True,
        db_index=True,
    )

    receipt = models.FileField(
        "Чек/скрин",
        upload_to="payments/receipts/",
        null=True,
        blank=True,
    )

    paid_at = models.DateTimeField("Оплачено в", null=True, blank=True)

    confirmed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="confirmed_payments",
        verbose_name="Подтвердил",
    )
    confirmed_at = models.DateTimeField("Подтверждено в", null=True, blank=True)

    note = models.CharField("Комментарий", max_length=255, blank=True)

    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["provider", "provider_ref"],
                name="uniq_payment_provider_providerref",
            ),
        ]
        indexes = [
            models.Index(fields=["order", "status"]),
            models.Index(fields=["provider", "status"]),
        ]

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = uuid.uuid4().hex[:12].upper()

        if self.provider_ref == "":
            self.provider_ref = None

        if self.status == PaymentStatus.PAID and not self.paid_at:
            self.paid_at = timezone.now()

        super().save(*args, **kwargs)

    def mark_paid(self, by=None, note: str = ""):
        self.status = PaymentStatus.PAID
        self.confirmed_by = by
        self.confirmed_at = timezone.now()
        if note:
            self.note = note
        self.save()

        # если у Order есть поле status и значение 'paid'
        if hasattr(self.order, "status"):
            try:
                self.order.status = "paid"
                self.order.save(update_fields=["status"])
            except Exception:
                pass

