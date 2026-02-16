from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserRegisterView, MyProfileView, EmailTokenObtainPairView

urlpatterns = [
    path("reg/", UserRegisterView.as_view(), name="register"),
    path("my_profile/", MyProfileView.as_view(), name="my_profile"),

    path("token/", EmailTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
