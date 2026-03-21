from shop.models import Menu
from .choices import DeliveryType, STATUS_CHOICES

from decimal import Decimal
from django.db import models
from django.db.models import Sum, F, DecimalField, ExpressionWrapper

from users.models import User
class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders",
        null=True, blank=True,
        verbose_name="Пользователь",
    )
    delivery_type = models.CharField(
        "Тип", max_length=16,
        choices=DeliveryType.choices,
        default=DeliveryType.PICKUP,
        db_index=True,
    )
    total_price = models.DecimalField(
        "Общая сумма", max_digits=10,
        decimal_places=2, default=0
    )
    status = models.CharField(
        "Статус заказа", max_length=20,
        choices=STATUS_CHOICES, default="created"
    )
    paid_at = models.DateTimeField(
        "Оплачен в", null=True, blank=True
    )
    created_at = models.DateTimeField(
        "Время создания", auto_now_add=True
    )
    id_transition = models.IntegerField(
        "ID транзакции", null=True, blank=True
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"заказ №{self.id} от {self.user}"

    def update_total_price(self):
        total = self.items.aggregate(
            total=Sum(
                ExpressionWrapper(
                    F("quantity") * F("price"),
                    output_field=DecimalField(max_digits=12, decimal_places=2),
                )
            )
        )["total"] or Decimal("0.00")

        self.total_price = total
        self.save(update_fields=["total_price"])
        return self.total_price


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, verbose_name="Заказ",
        on_delete=models.CASCADE, related_name="items"
    )
    menu = models.ForeignKey(
        Menu, verbose_name="Заказ",
        on_delete=models.CASCADE, related_name="order_items"
    )
    quantity = models.PositiveIntegerField(
        verbose_name="Количество", default=1
    )
    price = models.DecimalField(
        verbose_name="Цена на момент заказа",
        max_digits=10, decimal_places=2
    )

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"
        constraints = [
            models.UniqueConstraint(
                fields=["order", "menu"],
                name="unique_menu_per_order",
            )
        ]

    def __str__(self):
        return f"{self.quantity} × {self.menu.title}"
