from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from orders.models import Order, OrderItem
from orders.serializers import OrderSer

class OrderView(generics.ListAPIView):
    queryset = Order
    serializer_class = OrderSer