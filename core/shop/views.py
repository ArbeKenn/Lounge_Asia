from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, permissions

from .serializers import (
    CategorySer, DishSer, DishDetSer,
    DesertSer, DesertDetSer,
    DrinkSer, DrinkDetSer,
    )
from .models import Category, Dish, Desert, Drink

class Home(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySer

class DishViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]

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

    lookup_field = "slug"


class DesertViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]

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

    lookup_field = "slug"


class DrinkViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]

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

    lookup_field = "slug"
