from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from orders.models import Order
from orders.serializers import (
    OrderCreateSer,
    OrderReadSer,
    OrderStatusUpdateSer,
    OrderItemAddSer,
    OrderItemSetQuantitySer,
)
from orders.services import order_services


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

    order_services.check_order_access(request.user, order)

    serializer = OrderItemAddSer(data=request.data)
    serializer.is_valid(raise_exception=True)

    updated_order = order_services.add_item(
        order=order,
        menu=serializer.validated_data["menu"],
        quantity=serializer.validated_data["quantity"],
    )

    order.update_total_price()
    return Response(OrderReadSer(updated_order).data, status=status.HTTP_200_OK)

@action(detail=True, methods=["patch"], url_path="set-item")
def set_item(self, request, pk=None):
    order = self.get_object()

    order_services.check_order_access(request.user, order)

    serializer = OrderItemSetQuantitySer(data=request.data)
    serializer.is_valid(raise_exception=True)

    updated_order = order_services.set_item(
        order=order,
        item_id=serializer.validated_data["item_id"],
        quantity=serializer.validated_data["quantity"],
    )

    return Response(OrderReadSer(updated_order).data, status=status.HTTP_200_OK)

@action(detail=True, methods=["delete"], url_path="remove-item")
def remove_item(self, request, pk=None):
    order = self.get_object()
    item_id = request.query_params.get("item_id")

    if not item_id:
        return Response(
            {"detail": "item_id query parameter is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    order_services.check_order_access(request.user, order)
    order_services.remove_item(order, item_id)

    return Response(status=status.HTTP_204_NO_CONTENT)