from django.utils import timezone
from pay.choices import PaymentStatus

def mark_paid(self, by=None, note: str = ""):
    self.status = PaymentStatus.PAID
    self.confirmed_by = by
    self.confirmed_at = timezone.now()
    if note:
        self.note = note
    self.save(update_fields=["status", "confirmed_by", "confirmed_at", "note", "paid_at", "updated_at"])

    self.order.is_paid = True
    if not self.order.paid_at:
        self.order.paid_at = self.paid_at or timezone.now()
    self.order.paid_confirmed_by = by


    if self.order.status == "created":
        self.order.status = "accepted"

    self.order.save(update_fields=["is_paid", "paid_at", "paid_confirmed_by", "status", "updated_at"])