from django.contrib import admin
from .models import Order, OrderLineItem


# This inline item is going to allow us to add and edit line items in the admin from inside the model
# So when we look at an order. We'll see a list of editable line items on the same page.
class OrderLineitemAdminInLine(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)

class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineitemAdminInLine,)

    readonly_fields = ('order_number', 'date', 
                        'delivery_cost','order_total',
                        'grand_total','original_bag','stripe_pid')
    
    # will allow us to specify the order of the fields in the admin interface
    fields = ('order_number', 'date', 'full_name','email',
                'phone_number', 'country', 'postcode', 'town_or_city',
                'street_address1','street_address2',
                'county', 'delivery_cost',
                'order_total', 'grand_total',
                'original_bag','stripe_pid')
    

    # To restrict the columns that show up in the order list to only a few key items.
    list_display = ('order_number', 'date', 'full_name','order_total', 'delivery_cost', 'grand_total')

    ordering = ('-date',)

admin.site.register(Order, OrderAdmin)