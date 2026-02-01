from rest_framework import serializers
from .models import Category, Dish, Desert, Drink

class CategorySer(serializers.ModelSerializer):
    class Meta:
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
        discount_price = data.get("discount_price", getattr(self.instance, "discount_price", None))
        weight = data.get("weight", getattr(self.instance, "weight", None))


        if price is not None and weight is not None and price > 1000 and weight < 50:
            raise serializers.ValidationError("Нелогичные данные")

        if discount_price >= price:
            if price is not None and weight is not None and discount_price > 1000 and weight < 50:
                raise serializers.ValidationError("Скидочная цена должна быть меньше основной")

        return data

    class Meta:
        model = Dish
        fields = "__all__"


class DesertSer(BaseSer):
    class Meta:
        model = Desert
        fields = ('title','weight','calories','image','price')

class DesertDetSer(BaseSer):
    def validate(self, data):
        price = data.get("price", getattr(self.instance, "price", None))
        weight = data.get("weight", getattr(self.instance, "weight", None))

        if price is not None and weight is not None and price > 1000 and weight < 50:
            raise serializers.ValidationError("Нелогичные данные")

        return data

    class Meta:
        model = Desert
        fields = "__all__"


class DrinkSer(BaseSer):
    class Meta:
        model = Drink
        fields = ('title','weight','tea_type','volume','image','price')


class DrinkDetSer(BaseSer):
    def validate(self, data):
        price = data.get("price", getattr(self.instance, "price", None))
        volume = data.get("volume", getattr(self.instance, "volume", None))

        if price is not None and volume is not None and price > 1000 and volume < 50:
            raise serializers.ValidationError("Нелогичные данные")

        return data

    class Meta:
        model = Drink
        fields = "__all__"
