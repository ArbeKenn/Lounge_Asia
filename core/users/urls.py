# urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserRegisterView, MyProfileView, EmailTokenObtainPairView

urlpatterns = [
    path("api/reg/", UserRegisterView.as_view(), name="register"),
    path("api/my_profile/", MyProfileView.as_view(), name="my_profile"),

    path("api/token/", EmailTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
