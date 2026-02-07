from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets
from serializers import UserRegSer, EmailTokenObtainPairSerializer
from models import MyUsersManager, User

class UserRegView(viewsets):
    pass

class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer