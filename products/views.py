from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.db.models import Q
from .models import Product


# Create your views here.
def all_products(request):
    ''' a virw to show all products, inc sorting and search query'''

    products = Product.objects.all()  # get all products
    query = None

    if request.GET:
        # if GET REQUEST - Search Called
        if 'q' in request.GET:
            # if 'q' in query param. set query = q
            query = request.GET['q']
            if not query:
                # if q = emmpty
                messages.error(request, 'You did not enter search criteria')
                return redirect(reverse('products'))
            
            # else use special helper function Q to help build filter object.
            # query the name OR description field. 'i' indicates case insensitive
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query,
    }

    return render(request, 'products/products.html', context)
    

def product_detail(request, product_id):
    ''' a virw to show individual product'''

    product = get_object_or_404(Product, pk=product_id)
    context = {
        'product': product,
    }
    
    return render(request, 'products/product_detail.html', context)
    