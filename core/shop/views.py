from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .constants.c_views import MenuBaseViewSet, DishFilter, DesertFilter, DrinkFilter
from .serializers import (
    CategorySer, DishSer, DishDetSer,
    DesertSer, DesertDetSer,
    DrinkSer, DrinkDetSer,
    )

from .models import Category, Dish, Desert, Drink


class Home(MenuBaseViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySer


class DishViewSet(MenuBaseViewSet):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = DishFilter
    search_fields = ["title", "category__title"]

    def get_queryset(self):
        qs = Dish.objects.select_related("category")
        category_slug = self.request.query_params.get("category")
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        return qs

    def get_serializer_class(self):
        if self.action == "retrieve":
            return DishDetSer
        return DishSer


class DesertViewSet(MenuBaseViewSet):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filter_class = DesertFilter
    search_fields = ["title", "category__title"]

    def get_queryset(self):
        qs = Desert.objects.select_related("category")
        category_slug = self.request.query_params.get("category")
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        return qs

    def get_serializer_class(self):
        if self.action == "retrieve":
            return DesertDetSer
        return DesertSer


class DrinkViewSet(MenuBaseViewSet):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filter_class = DrinkFilter
    search_fields = ["title", "category__title"]

    def get_queryset(self):
        qs = Drink.objects.select_related("category")
        category_slug = self.request.query_params.get("category")
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        return qs

    def get_serializer_class(self):
        if self.action == "retrieve":
            return DrinkDetSer
        return DrinkSer
