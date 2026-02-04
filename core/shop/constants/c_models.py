from django.db import models

class Base(models.Model):
    class Meta:
        abstract = True

    category = models.ForeignKey(
        'shop.Category',
        on_delete=models.CASCADE,
        related_name="%(class)s_items",
        verbose_name="Категория"
    )
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    ingredients = models.TextField(blank=True, verbose_name="Состав")
    mass_ingredients = models.TextField(
        null=True, blank=True,
        verbose_name="Состав/Вес (г)",
    )
    weight = models.PositiveIntegerField(
        null=True, blank=True,
        verbose_name="Вес (г)",
    )

    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        verbose_name="Цена",
    )
    discount_price = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True,
        verbose_name="Цена со скидкой"
    )

    is_available = models.BooleanField(
        default=True, verbose_name="В наличии",
    )
    quantity = models.PositiveIntegerField(
        default=0, verbose_name="Остаток на складе",
    )
    is_bestseller = models.BooleanField(
        default=False, verbose_name="Хит продаж",
    )

    image = models.ImageField(
        upload_to='products/%Y/%m/', blank=True,
        verbose_name="Фото",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.is_available = self.stock > 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} — {self.price} сом"


class TeaType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Тип чая")

    class Meta:
        verbose_name = "Тип чая"
        verbose_name_plural = "Типы чая"

    def __str__(self):
        return self.name