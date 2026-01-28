from django.db import models
from shop.constants.models import Base, TeaType

class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name="Категория")
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title


class Dish(Base):
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Блюда"
        verbose_name_plural = "Блюда"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.price} сом."


class Desert(Base):
    slug = models.SlugField(unique=True, verbose_name="URL-адрес (slug)")
    calories = models.PositiveIntegerField(
        null=True, blank=True,
        verbose_name="Калорийность (ккал/100г)",
    )
    pieces = models.PositiveIntegerField(
        null=True, blank=True,
        default=1,
        verbose_name="Количество кусочков/порций",
    )

    class Meta:
        verbose_name = "Десерт"
        verbose_name_plural = "Десерты"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.price} сом."


class Drink(Base):
    slug = models.SlugField(unique=True, verbose_name="URL-адрес (slug)")
    tea_type = models.ForeignKey(
        TeaType,
        on_delete=models.PROTECT,
        verbose_name="Вид чая",
        related_name="drinks",
    )
    brand = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        verbose_name="Бренд напитка",
    )
    volume = models.PositiveIntegerField(null=True, blank=True, verbose_name="Объём (мл)")
    sugar_level = models.IntegerField(
        default=0,
        choices=[(0, 'Без сахара'), (25, '25%'), (50, '50%'), (100, '100%')],
        verbose_name="Уровень сахара",
    )

    class Meta:
        verbose_name = "Напиток"
        verbose_name_plural = "Напитки"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.price} сом."