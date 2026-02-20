from shop.models import Dish, Drink, Desert
from .choices import STATUS_CHOICES

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
    total_price = models.DecimalField(
        "Общая сумма", max_digits=10,
        decimal_places=2, default=0
    )
    status = models.CharField(
        "Статус заказа", max_length=20,
        choices=STATUS_CHOICES, default="created"
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
    dish = models.ForeignKey(
        Dish, verbose_name="Позиция",
        on_delete= models.CASCADE
    )
    desert = models.ForeignKey(
        Desert, verbose_name="Позиция",
        on_delete=models.CASCADE
    )
    drink = models.ForeignKey(
        Drink, verbose_name="Позиция",
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField("Количество", default=1)
    price = models.DecimalField("Цена на момент заказа",
                                max_digits=10, decimal_places=2
                                )

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"

    def __str__(self):
        return f"{self.quantity} × {self.dish.title}"

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.dish.price
        super().save(*args, **kwargs)
        self.order.update_total_price()
