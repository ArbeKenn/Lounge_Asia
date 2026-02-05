import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from users.choices import GENDER_CHOICES

class MyUsersManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, age, password=None):
        if not email:
            raise ValueError('Users must have email address')
        if not username:
            raise ValueError('Users must have username')

        user = self.model(
            email = email,
            username = username,
            first_name = first_name,
            last_name = last_name,
            age = age,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, age, password):
        user = self.create_user(
            email=email,
            password=password,
            username=username,
            first_name=first_name,
            last_name=last_name,
            age=age,
        )
        user.is_admin = True
        user.is_staff = True
        user.superuser = True

class User(AbstractBaseUser):
    email = models.EmailField(max_length=60, unique=True)
    username = models.CharField(max_length=16, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    bio = models.TextField(max_length=2000)
    age = models.DateField(default=datetime.date.today)
    gender = models.CharField(choices=GENDER_CHOICES,)
    profile_pic = models.ImageField(
        upload_to='image/user_profile',
        blank=True, null=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name','age']

    objects = MyUsersManager()

    def __str__(self):
        return self.username + ',' + self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True