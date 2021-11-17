from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category


# Create your views here.
def all_products(request):
    ''' a virw to show all products, inc sorting and search query'''

    products = Product.objects.all()  # get all products

    query = None
    categories = None

    if request.GET:

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)  # convert list of string categories to category objects to be used on the page later.

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
        'search_term': query,  # why is this added here? perhaps to use the search term on the page?
        'categories': categories,
    }

    # note combine the query with
    # https://8000-rose-firefly-8vglw7e2.ws-eu18.gitpod.io/products/?category=jeans&q=boot
    return render(request, 'products/products.html', context)
    

def product_detail(request, product_id):
    ''' a virw to show individual product'''

    product = get_object_or_404(Product, pk=product_id)
    context = {
        'product': product,
    }
    
    return render(request, 'products/product_detail.html', context)
    