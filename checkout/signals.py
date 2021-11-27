from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import OrderLineItem

# a bit like sql trigger

# we  access instance.order which refers to the order this specific line item is related to.
# And call the update_total method on it.
# Now to execute this function anytime the post_save signal is sent.
# use the receiver decorator. Telling it we're receiving post saved signals.
@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    '''
    Update order total on lineitem update/create
    '''

    instance.order.update_total()

@receiver(post_delete, sender=OrderLineItem)
def update_on_delete(sender, instance, **kwargs):
    '''
    Update order total on lineitem delete
    '''

    instance.order.update_total()



# update app.py
# Overriding the ready method and importing our signals module.