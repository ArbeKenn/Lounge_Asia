from django.db import models
from shop.constants.c_models import Base
class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name="Категория")
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title


class Menu(Base):
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Блюда"
        verbose_name_plural = "Блюда"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.price} сом."
