from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import User
# просто имитация!

class Card(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="card",
        null=True, blank=True,
        verbose_name="Пользователь",
    )
    name = models.CharField(max_length=50)
    number = models.IntegerField(
        unique=True,
        null=True,
        blank=True,
        validators=[MinValueValidator(1000000000000000), MaxValueValidator(9999999999999999)]
    )
    money = models.DecimalField(max_digits=10, decimal_places=2)
    password = models.CharField
    date = models.DateField()
    cvs = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(999)]
    )
    email = models.EmailField()


