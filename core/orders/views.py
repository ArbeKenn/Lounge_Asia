from django.db import transaction
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from orders.models import Order, OrderItem
from orders.serializers import (
    OrderCreateSer,
    OrderReadSer,
    OrderStatusUpdateSer,
    OrderItemAddSer,
    OrderItemSetQuantitySer,
)


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = (
            Order.objects
            .select_related("user")
            .prefetch_related("items__menu")
        )
        if self.request.user.is_staff:
            return qs
        return qs.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return OrderCreateSer
        if self.action in ("update", "partial_update"):
            if self.request.user.is_staff:
                return OrderStatusUpdateSer
            return OrderReadSer
        return OrderReadSer

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=["post"], url_path="add-item")
    def add_item(self, request, pk=None):
        order = self.get_object()

        if not request.user.is_staff and order.user_id != request.user.id:
            return Response({"detail": "Нет доступа."}, status=status.HTTP_403_FORBIDDEN)

        serializer = OrderItemAddSer(data=request.data)
        serializer.is_valid(raise_exception=True)

        menu = serializer.validated_data["menu"]
        quantity = serializer.validated_data["quantity"]

        item, created = OrderItem.objects.get_or_create(
            order=order,
            menu=menu,
            defaults={
                "quantity": quantity,
                "price": menu.price,
            },
        )

        if not created:
            item.quantity += quantity
            item.save(update_fields=["quantity"])

        order.update_total_price()
        return Response(OrderReadSer(order).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["patch"], url_path="set-item")
    def set_item(self, request, pk=None):
        order = self.get_object()

        if not request.user.is_staff and order.user_id != request.user.id:
            return Response({"detail": "Нет доступа."}, status=status.HTTP_403_FORBIDDEN)

        serializer = OrderItemSetQuantitySer(data=request.data)
        serializer.is_valid(raise_exception=True)

        item_id = serializer.validated_data["item_id"]
        quantity = serializer.validated_data["quantity"]

        item = order.items.filter(id=item_id).first()
        if not item:
            return Response({"detail": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        item.quantity = quantity
        item.save(update_fields=["quantity"])
        order.update_total_price()

        return Response(OrderReadSer(order).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["delete"], url_path="remove-item")
    def remove_item(self, request, pk=None):
        order = self.get_object()

        if not request.user.is_staff and order.user_id != request.user.id:
            return Response({"detail": "Нет доступа."}, status=status.HTTP_403_FORBIDDEN)

        item_id = request.query_params.get("item_id")
        deleted, _ = order.items.filter(id=item_id).delete()

        if not deleted:
            return Response({"detail": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        order.update_total_price()
        return Response(status=status.HTTP_204_NO_CONTENT)