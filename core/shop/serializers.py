from rest_framework import serializers
from .models import Category, Dish, Desert, Drink

class CategorySer(serializers.ModelSerializer):
    model = Category
    fields = "__all__"


class BaseSer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Category.objects.all()
    )


class DishSer(BaseSer):
    class Meta:
        model = Dish
        fields = ('title','weight','image','price')


class DishDetSer(BaseSer):
    def validate(self, data):
        price = data.get("price", getattr(self.instance, "price", None))
        weight = data.get("weight", getattr(self.instance, "weight", None))

        if price>1000 and weight<50:
            raise serializers.ValidationError("Нелогичные данные")

        return data

    class Meta:
        model = Dish
        fields = "__all__"


class DesertSer(BaseSer):
    class Meta:
        model = Desert
        fields = ('title','weight','calories','image','price')

class DesertDetSer(serializers.ModelSerializer):
    def validate(self, data):
        price = data.get("price", getattr(self.instance, "price", None))
        weight = data.get("weight", getattr(self.instance, "weight", None))

        if price>1000 and weight<50:
            raise serializers.ValidationError("Нелогичные данные")

        return data

    class Meta:
        model = Desert
        fields = "__all__"


class DrinkSer(BaseSer):
    class Meta:
        model = Drink
        fields = ('title','weight','tea_type','volume','image','price')


class DrinkDetSer(serializers.ModelSerializer):
    def validate(self, data):
        price = data.get("price", getattr(self.instance, "price", None))
        volume = data.get("volume", getattr(self.instance, "volume", None))

        if price > 1000 and volume < 50:
            raise serializers.ValidationError("Нелогичные данные")

        return data

    class Meta:
        model = Drink
        fields = "__all__"
