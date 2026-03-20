from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import HomeViewSet, MenuViewSet

router = DefaultRouter()
router.register(r"menu/dishes", MenuViewSet, basename="dish")

urlpatterns = [
    path("", HomeViewSet.as_view({"get": "list"}), name="home"),
]
urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)