from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category
from django.db.models.functions import Lower


# Create your views here.
def all_products(request):
    ''' a virw to show all products, inc sorting and search query'''

    products = Product.objects.all()  # get all products

    query = None
    categories = None
    direction = None
    sort = None

    if request.GET:

        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey

            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
                #  note1: no call to sort by name yet implented on front end
                #  note2: you must import the Lower function from django.db.models.functions
                #  note3: the annotate method (as I understand it) here is adding another field to the in memory model called 'lower_name'
                #           the Lower function is then returning lower case name to lower_name field.
                #           the sort is carried out on the lower case version of the string - making the sort case in-sensitive.
            
            if sortkey == 'category':
                sortkey = 'category__name' #  the double underscore tells django to do a foreign key filed lookup. otherwise we are sorting on category.id.

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'         #  if desc sort then add '-' in front of sortkey, which is the field to sort
            products = products.order_by(sortkey)   #  django then sorts desc on that field

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)  # convert list of string categories to category objects to be used on the page later.

        # if GET REQUEST - Search Called
        if 'q' in request.GET:
            # if 'q' in query param. set query = q
            query = request.GET['q']
            if not query:
                # if q = emmpty ---- note not sure how to call to get empty q? page errors if no value passed to q in querystring
                messages.error(request, 'You did not enter search criteria')
                return redirect(reverse('products'))
            
            # else use special helper function Q to help build filter object.
            # query the name OR description field. 'i' indicates case insensitive
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,  
        'current_categories': categories, # passing this in context so that we can list the 'sub' categories of the cat selected. e.g. Special Offers > New Arrivals/Deals/Sale/Clear etc..
        'current_sorting': current_sorting, # passing this in context so that we can set the valueof the sort select box
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
    