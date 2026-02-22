from django.db import models
from users.models import User
# просто имитация!

class Card(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders",
        null=True, blank=True,
        verbose_name="Пользователь",
    )
    name = models.CharField(max_length=50)
    number = models.IntegerField(
        max_length=16,
        unique=True, null=True, blank=True,
    )
    money = models.DecimalField(max_digits=10, decimal_places=2)
    password = models.CharField
    date = models.DateField()
    cvs = models.PositiveSmallIntegerField(max_length=3)
    email = models.EmailField()


