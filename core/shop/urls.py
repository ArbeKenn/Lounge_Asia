from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import Home, DishViewSet, DesertViewSet, DrinkViewSet

router = DefaultRouter()
router.register(r"menu/dishes", DishViewSet, basename="dish")
router.register(r"menu/deserts", DesertViewSet, basename="desert")
router.register(r"menu/drinks", DrinkViewSet, basename="drink")

urlpatterns = [
    path("", Home.as_view(), name="home"),
]

urlpatterns += router.urls

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

