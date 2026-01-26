from rest_framework import serializers
from .models import Category, Dish, Desert, Drink

class CategorySer(serializers.Serializer):
    model = Category
    fields = '__all__'

class DishSer(serializers.Serializer):
    category = serializers.SlugRelatedField(
        slug_field="slug",
        read_only=True
    )

    class Meta:
        model = Dish
        fields = "__all__"


class DishDetailSer(serializers.Serializer):
    models = Dish
    fields = '__all__'