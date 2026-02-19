from decimal import Decimal
from django.db import transaction
from rest_framework import serializers

from shop.models import Dish, Desert, Drink
from orders.models import Order, OrderItem

class OrderItemReadSer(serializers.ModelSerializer):
    dish_title = serializers.CharField(source=("dish.title", "desert.title", "drink.title"), read_only=True)

    class Meta:
        model = OrderItem
        field = "__all__"


class OrderItemWriteSer(serializers.Serializer):
    dish = serializers.PrimaryKeyRelatedField(queryset=Dish.objects.all())
    desert = serializers.PrimaryKeyRelatedField(queryset=Desert.objects.all())
    drink = serializers.PrimaryKeyRelatedField(queryset=Drink.objects.all())
    quantity = serializers.IntegerField(min_value=1)

    def validate(self, attrs):
        dish = attrs["dish"]
        desert = attrs["desert"]
        drink = attrs["drink"]
        qty = attrs["quantity"]

        if hasattr(dish, "is_available") and not dish.is_available:
            raise serializers.ValidationError("Товара нет в наличии")
        if hasattr(desert, "is_available") and not desert.is_available:
            raise serializers.ValidationError("Товара нет в наличии")
        if hasattr(drink, "is_available") and not drink.is_available:
            raise serializers.ValidationError("Товара нет в наличии")

        return attrs


class OrderReadSer(serializers.ModelSerializer):
    items = OrderItemReadSer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ("id", "status", "total_price", "created_at", "id_transition", "items")


class OrderCreateSer(serializers.ModelSerializer):
    items = OrderItemWriteSer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ("id", "items")

    def create(self, validated_data):
        request = self.context["request"]
        items_data = validated_data.pop("items")

        with transaction.atomic():
            order = Order.objects.create(user=request.user)

            bulk_items = []
            for item in items_data:
                dish = item["dish"]
                qty = item["quantity"]

                bulk_items.append(OrderItem(
                    order=order,
                    dish=dish,
                    quantity=qty,
                    price=dish.price,
                ))

            OrderItem.objects.bulk_create(bulk_items)

            order.update_total_price()

        return order


class OrderStatusUpdateSer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("status",)

