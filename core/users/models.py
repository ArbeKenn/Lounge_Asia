from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from users.choices import GENDER_CHOICES

class MyUsersManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, age, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have email address")
        if not username:
            raise ValueError("Users must have username")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            age=age,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, age, password=None, **extra_fields):
        user = self.create_user(email, username, first_name, last_name, age, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=60, unique=True)
    username = models.CharField(max_length=16, unique=True)
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    bio = models.TextField(max_length=2000, blank=True)
    age = models.PositiveSmallIntegerField()

    gender = models.CharField(choices=GENDER_CHOICES, max_length=1, blank=True, null=True)
    profile_pic = models.ImageField(upload_to="image/user_profile", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name", "age"]

    objects = MyUsersManager()

    def __str__(self):
        return f"{self.username}, {self.email}"
