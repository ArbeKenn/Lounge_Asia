from django.db import transaction
from rest_framework import serializers

from shop.models import Menu
from orders.models import Order, OrderItem

class OrderItemReadSer(serializers.ModelSerializer):
    menu_title = serializers.CharField(
        source="menu.title",
        read_only=True
    )
    menu_price = serializers.DecimalField(
        source="menu.price",
        max_digits=10, decimal_places=2,
        read_only=True
    )

    class Meta:
        model = OrderItem
        fields = ("id", "menu", "menu_title","menu_price","quantity", "price")


class OrderItemWriteSer(serializers.Serializer):
    menu = serializers.PrimaryKeyRelatedField(queryset=Menu.objects.all())
    quantity = serializers.IntegerField(min_value=1)

    def validate_menu(self, menu):
        if not menu.is_available:
            raise serializers.ValidationError("Товара нет в наличии")
        return menu


class OrderReadSer(serializers.ModelSerializer):
    items = OrderItemReadSer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "delivery_type",
            "status",
            "total_price",
            "created_at",
            "id_transition",
            "paid_at",
            "items",
        )


class OrderCreateSer(serializers.ModelSerializer):
    items = OrderItemWriteSer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ("id", "delivery_type", "items")

    def create(self, validated_data):
        request = self.context["request"]
        items_data = validated_data.pop("items")

        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                **validated_data
            )

            order_items = []
            for item in items_data:
                menu = item["menu"]
                quantity = item["quantity"]

                order_items.append(
                    OrderItem(
                        order=order,
                        menu=menu,
                        quantity=quantity,
                        price=menu.price,
                    )
                )

            OrderItem.objects.bulk_create(order_items)
            order.update_total_price()

        return order


class OrderStatusUpdateSer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("status",)


class OrderItemAddSer(serializers.Serializer):
    menu = serializers.PrimaryKeyRelatedField(queryset=Menu.objects.all())
    quantity = serializers.IntegerField(min_value=1)

    def validate_menu(self, menu):
        if not menu.is_available:
            raise serializers.ValidationError("Товара нет в наличии")
        return menu


class OrderItemSetQuantitySer(serializers.Serializer):
    item_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
