from decimal import Decimal
from django.db import transaction
from rest_framework import serializers

from shop.models import Menu
from orders.models import Order, OrderItem

class OrderItemReadSer(serializers.ModelSerializer):
    menu_title = serializers.CharField(source="menu.title", read_only=True)

    class Meta:
        model = OrderItem
        fields = ("id", "menu", "menu_title", "quantity", "price")


class OrderItemWriteSer(serializers.Serializer):
    menu = serializers.PrimaryKeyRelatedField(queryset=Menu.objects.all())
    quantity = serializers.IntegerField(min_value=1)

    def validate(self, attrs):
        menu = attrs["menu"]
        qty = attrs["quantity"]

        if hasattr(menu, "is_available") and not menu.is_available:
            raise serializers.ValidationError("Товара нет в наличии")
        return attrs


class OrderReadSer(serializers.ModelSerializer):
    items = OrderItemReadSer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ("id", "delivery_type", "status", "total_price", "created_at", "id_transition", "items")


class OrderCreateSer(serializers.ModelSerializer):
    items = OrderItemWriteSer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ("id", "delivery_type", "items")

    def create(self, validated_data):
        request = self.context["request"]
        items_data = validated_data.pop("items")

        with transaction.atomic():
            order = Order.objects.create(user=request.user, **validated_data)

            OrderItem.objects.bulk_create([
                OrderItem(
                    order=order,
                    menu=item["menu"],
                    quantity=item["quantity"],
                    price=item["menu"].price,
                )
                for item in items_data
            ])

            order.update_total_price()

        return order

class OrderStatusUpdateSer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("status",)

