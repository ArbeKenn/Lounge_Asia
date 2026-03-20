from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .constants.c_views import MenuBaseViewSet, DishFilter, DesertFilter, DrinkFilter
from .serializers import (
    CategorySer, MenuSer, MenuDetSer,
    )

from .models import Category, Menu


class HomeViewSet(MenuBaseViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySer


class MenuViewSet(MenuBaseViewSet):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = DishFilter
    search_fields = ["title", "category__title"]

    def get_queryset(self):
        qs = Menu.objects.select_related("category")
        category_slug = self.request.query_params.get("category")
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        return qs

    def get_serializer_class(self):
        if self.action == "retrieve":
            return MenuDetSer
        return MenuSer