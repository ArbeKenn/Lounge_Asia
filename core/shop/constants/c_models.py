from django.db import models

class Base(models.Model):
    CATEGORY_CHOICES = (
        ("dish", "Блюдо"),
        ("desert", "Десерт"),
        ("drink", "Напиток"),
    )

    category = models.ForeignKey(
        'shop.Category',
        on_delete=models.CASCADE,
        related_name="menu_items",
        verbose_name="Категория"
    )
    item_type = models.CharField(
        max_length=10,
        choices=CATEGORY_CHOICES,
        verbose_name='Тип товара'
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
    calories = models.PositiveIntegerField(
        null=True, blank=True,
        verbose_name="Калорийность (ккал/100г)",
    )
    pieces = models.PositiveIntegerField(
        null=True, blank=True,
        default=1,
        verbose_name="Количество кусочков/порций",
    )
    brand = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        verbose_name="Бренд напитка",
    )
    volume = models.PositiveIntegerField(
        null=True, blank=True,
        verbose_name="Объём (мл)"
    )
    sugar_level = models.IntegerField(
        default=0,
        choices=[(0, 'Без сахара'), (25, '25%'), (50, '50%'), (100, '100%')],
        verbose_name="Уровень сахара",
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
        self.is_available = self.quantity > 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} — {self.price} сом"
