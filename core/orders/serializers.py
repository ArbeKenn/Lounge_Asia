from rest_framework import serializers
from orders.models import Order, OrderItem
class OrderSer(serializers.Serializer):
    class Meta:
        model = OrderItem
        field = "__all__"