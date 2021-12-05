from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from bag.contexts import bag_contents

import datetime


import stripe

def checkout(request):
    # 1 PAGE LOADS AND CREATES AN INTENT WITH STRIPE
    # 2 USER FILLS IN FORM AND CC DETAILS AND SUBMITS FORM
    # 3 PAGE RELOADS (POST)
    #   3.1 JAVASCRIPT LISTENER INTERCEPTS SUBMIT AND VALIDATES CARD AND PROCOESS CC TRANSACTION
    #   3.2 FORM IS SUBMITTED IF ALL OK
    #       3.2.1 FORM DATA IS VALIDATED
    #       3.2.2 ORDER HEADER IS WRITTEN TO ORDER TABLE IN DB
    #       3.2.3 EACH BAG ITEM IS WRITTEN TO ORDERLINEITEMS
    #   3.3 IF ALL OK DELETE ORDER FROM BAG AND REDIRECT TO SUCCESS.HTML
    

    print('checkout started')
    print(datetime.datetime.now())

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    # print('keys:') 
    # print(stripe_public_key)
    # print(stripe_secret_key)

    if request.method == 'POST':
        print('POST VALIDATNG FORM')
        print(datetime.datetime.now())
        bag = request.session.get('bag', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save()
            for item_id, item_data in bag.items():
                try:
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        for size, quantity in item_data['items_by_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            order_line_item.save()
                except EventList.DoesNotExist:
                    messages.error(request, (
                        "One of the events in your bag wasn't found in our database. "
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_bag'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')
    else:
        print('START STRIPE INTENT')
        print(datetime.datetime.now())
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, "There's nothing in your bag at the moment")
            return redirect(reverse('products'))


        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        stripe_total = round(total * 100)

        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
                amount=stripe_total,
                currency=settings.STRIPE_CURRENCY,
                )
        # print(intent)

        order_form = OrderForm()
    
    if not stripe_public_key:
        message.warning(request,'Stripe Public Key missing. Did you forget to set an environment variable ?')
    
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
