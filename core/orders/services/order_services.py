from django.db import transaction
from rest_framework.exceptions import NotFound, PermissionDenied
from orders.models import OrderItem

def check_order_access(user, order):
    if not user.is_staff and order.user_id != user.id:
        raise PermissionDenied("Нет доступа")

@transaction.atomic
def add_item(order, menu, quantity):
    item, created = OrderItem.objects.get_or_create(
        order=order,
        menu=menu,
        defaults={"quantity": quantity, "price": menu.price},
    )
    if not created:
        item.quantity += quantity
        item.save(update_fields=["quantity"])

    order.update_total_price()
    return order


@transaction.atomic
def set_item(order, item_id, quantity):
    item = order.items.filter(id=item_id).first()

    if not item:
        raise NotFound("Item not found")

    item.quantity = quantity
    item.save(update_fields=["quantity"])

    order.update_total_price()
    return order

@transaction.atomic
def remove_item(order, item_id):
    deleted, _ = order.items.filter(id=item_id).delete()
    if not deleted:
        raise NotFound("Item not found")

    order.update_total_price()
    return order