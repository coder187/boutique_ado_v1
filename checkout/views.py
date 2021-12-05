from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    print('keys:') 
    print(stripe_public_key)
    print(stripe_secret_key)


    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))


    stripe_total = round(total * 100)

    stripe.api_key = stripe_secret_key
    #intent = stripe.PaymentIntent.create(
    #        amount=stripe_total,
    #        currency=settings.STRIPE_CURRENCY,
    #        )
    #print(intent)

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51K0ZuLGc2X9Nm4M2l45fWyPvOUNhNfwIvHdIQV2hCcc9uxdBwjRciYsIpUW8KX42QdGdXc9viedqGEF1PBF6GRQ8004qOoKrSs',
        'client_secret': 'sk_test_51K0ZuLGc2X9Nm4M21aXjR765tUUCNaMyL6CEbVILac15e9plRiszP25DExP0vifSijVkdXD3FLknq0GnD5JjeOoT00QH0dyqT7',
    }

    return render(request, template, context)
