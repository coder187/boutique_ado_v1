from django.shortcuts import render,get_object_or_404
from .models import Product


# Create your views here.
def all_products(request):
    ''' a virw to show all products, inc sorting and search query'''

    products = Product.objects.all()  # get all products

    context = {
        'products': products,
    } 

    return render(request, 'products/products.html', context)
    

def product_detail(request, product_id):
    ''' a virw to show individual product'''

    product = get_object_or_404(Product, pk=product_id)
    context = {
        'product': product,
    }
    
    return render(request, 'products/product_detail.html', context)
    