from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Order

@receiver(pre_save, sender=Order)
def update_order_items(sender, instance, **kwargs):
    if instance.pk:
        original_order = Order.objects.get(pk=instance.pk)
        if original_order.payed != instance.payed:
            instance.orderitems.all().update(payed=instance.payed)