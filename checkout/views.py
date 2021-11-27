from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51K0ZuLGc2X9Nm4M2l45fWyPvOUNhNfwIvHdIQV2hCcc9uxdBwjRciYsIpUW8KX42QdGdXc9viedqGEF1PBF6GRQ8004qOoKrSs',
        'client_secret': 'sk_test_51K0ZuLGc2X9Nm4M21aXjR765tUUCNaMyL6CEbVILac15e9plRiszP25DExP0vifSijVkdXD3FLknq0GnD5JjeOoT00QH0dyqT7',
    }

    return render(request, template, context)
