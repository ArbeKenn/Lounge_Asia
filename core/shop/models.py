from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name="Категория")

    class Meta:
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title


class Dish(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='dishes')
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание/Состав")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")

    weight = models.PositiveIntegerField(null=True, blank=True, verbose_name="Вес (г)")
    volume = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Объем (л)")
    image = models.ImageField(upload_to='dishes/', blank=True, verbose_name="Фото")

    def __str__(self):
        return f"{self.title} - {self.price} сом."