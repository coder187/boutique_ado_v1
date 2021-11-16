from django.shortcuts import render
from .models import Product


# Create your views here.
def all_products(request):
    ''' a virw to show all products, inc sorting and search query'''

    products = Product.objects.all()  # get all products

    context = {
        'products': products,
    } 

    return render(request, 'products/products.html', context)
    