from rest_framework import serializers
from .models import Category, Menu

class CategorySer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class BaseSer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Category.objects.all()
    )


class MenuSer(BaseSer):
    class Meta:
        model = Menu
        fields = ("title","weight","volume","image","price")


class MenuDetSer(BaseSer):
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
        model = Menu
        fields = "__all__"