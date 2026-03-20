from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .constants.c_views import MenuBaseViewSet, MenuFilter
from .serializers import (
    CategorySer, MenuSer, MenuDetSer,
    )

from .models import Category, Menu


class HomeViewSet(MenuBaseViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySer


class MenuViewSet(MenuBaseViewSet):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = MenuFilter
    search_fields = ["title", "category__title"]

    def get_queryset(self):
        qs = Menu.objects.select_related("category").all()

        item_type = self.request.query_params.get("item_type")
        category = self.request.query_params.get("category")

        if item_type:
            qs = qs.filter(item_type=item_type)

        if category:
            qs = qs.filter(category_id=category)

        return qs.order_by("id")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return MenuDetSer
        return MenuSer