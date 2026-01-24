from rest_framework import serializers
from .models import Category, Dish

class CategorySer(serializers.Serializer):
    model = Category
    fields = '__all__'

class DishSer(serializers.Serializer):
    model = Dish
    fields = ['title','category','image','price']


class DishDetailSer(serializers.Serializer):
    models = Dish
    fields = '__all__'