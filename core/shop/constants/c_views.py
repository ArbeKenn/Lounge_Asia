from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
import django_filters

from shop.models import Menu

class MenuBaseViewSet(viewsets.ModelViewSet):
    lookup_field = "slug"

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class MenuFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = Menu
        fields = ["min_price", "max_price", "is_bestseller"]
