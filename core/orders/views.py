from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from orders.models import Order, OrderItem
from orders.serializers import (
    OrderReadSer, OrderCreateSer, OrderStatusUpdateSer,
    OrderItemReadSer
)

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Order.objects.prefetch_related("items__dish").select_related("user")
        if self.request.user.is_staff:
            return qs
        return qs.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return OrderCreateSer
        if self.action in ("partial_update", "update") and self.request.user.is_staff:
            return OrderStatusUpdateSer
        return OrderReadSer

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=["post"], url_path="add-item")
    def add_item(self, request, pk=None):
        order = self.get_object()
        if not request.user.is_staff and order.user_id != request.user.id:
            return Response({"detail": "Нет доступа."}, status=403)

        dish_id = request.data.get("dish")
        quantity = int(request.data.get("quantity", 1))
        if quantity < 1:
            return Response({"detail": "quantity >= 1"}, status=400)

        # если такая позиция уже есть — увеличиваем quantity
        item, created = OrderItem.objects.get_or_create(
            order=order,
            dish_id=dish_id,
            defaults={"quantity": quantity},
        )
        if not created:
            item.quantity += quantity
            item.save(update_fields=["quantity"])
        if not item.price:
            item.price = item.dish.price
            item.save(update_fields=["price"])

        order.update_total_price()
        return Response(OrderReadSer(order).data, status=200)

    @action(detail=True, methods=["patch"], url_path="set-item")
    def set_item(self, request, pk=None):

        order = self.get_object()
        if not request.user.is_staff and order.user_id != request.user.id:
            return Response({"detail": "Нет доступа."}, status=403)

        item_id = request.data.get("item_id")
        quantity = int(request.data.get("quantity", 1))
        if quantity < 1:
            return Response({"detail": "quantity >= 1"}, status=400)

        item = order.items.filter(id=item_id).first()
        if not item:
            return Response({"detail": "Item not found"}, status=404)

        item.quantity = quantity
        item.save(update_fields=["quantity"])
        order.update_total_price()
        return Response(OrderReadSer(order).data, status=200)

    @action(detail=True, methods=["delete"], url_path="remove-item")
    def remove_item(self, request, pk=None):

        order = self.get_object()
        if not request.user.is_staff and order.user_id != request.user.id:
            return Response({"detail": "Нет доступа."}, status=403)

        item_id = request.query_params.get("item_id")
        deleted, _ = order.items.filter(id=item_id).delete()
        if not deleted:
            return Response({"detail": "Item not found"}, status=404)

        order.update_total_price()
        return Response(status=status.HTTP_204_NO_CONTENT)