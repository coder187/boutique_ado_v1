from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages

from products.models import Product

# Create your views here.
def view_bag(request):
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """
    
    #  product = Product.objects.get(pk=item_id)  # for toast message only
    product = get_object_or_404(Product, pk=item_id)  # for toast message only

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    
    bag = request.session.get('bag', {})
    if 'product_size' in request.POST:
        size = request.POST.get('product_size')

    if size:
        if item_id in list(bag.keys()):
            if size in bag[item_id]['items_by_size'].keys():
                bag[item_id]['items_by_size'][size] += quantity
                messages.success(request, f'Updated {size.upper()} {product.name} quantity to { bag[item_id]["items_by_size"][size] }')
            else:
                bag[item_id]['items_by_size'][size] = quantity
                messages.success(request, f'Added {size.upper()} {product.name} to your bag.')
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
            messages.success(request, f'Added {size.upper()} {product.name} to your bag.')
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
            messages.success(request, f'Updated {product.name} to {bag[item_id]}.') # note item_is holds tje qty for items with no sizes option
        else:
            bag[item_id] = quantity
            
            # show success msg via boostrap toast.
            messages.success(request, f'Added {product.name} to your bag.')

    # create a dictionary to hold the session variable 'bag'. If there is no bag session var, create an empty one.
    # if the current item_id exists in the session var, increment by quantiy else set bag.item_id = quantity
    # if item_id in list(bag.keys()):
    #     bag[item_id] += quantity
    # else:
    #    bag[item_id] = quantity

    # overwrite session bag var with updated bag
    request.session['bag'] = bag
    print(request.session['bag'])
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """ Adjust the quantity of the specified product to the specified amount """
    
    product = get_object_or_404(Product, pk=item_id)  # for toast message only

    quantity = int(request.POST.get('quantity'))
  
    size = None
    
    bag = request.session.get('bag', {})

    if 'product_size' in request.POST:
        size = request.POST.get('product_size')
        
    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
            messages.success(request, f'Updated {size.upper()} {product.name} quantity to { bag[item_id]["items_by_size"][size] }')
        else:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size'][size]:
                bag.pop(item_id)
            messages.success(request, f'Removed {size.upper()} {product.name} from your bag.')
    else:
        if quantity > 0:
            bag[item_id] = quantity
            messages.success(request, f'Updated {product.name} to {bag[item_id]}.') # note item_is holds tje qty for items with no sizes option
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from to your bag.')


    request.session['bag'] = bag
    return redirect(reverse('view_bag'))
    

def remove_from_bag(request, item_id):
    """Remove the item from shopping bag"""
   
    try:
        product = get_object_or_404(Product, pk=item_id)  # for toast message only
        size = None
        bag = request.session.get('bag', {})

        if 'product_size' in request.POST:
            size = request.POST.get('product_size')
        if size:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.success(request, f'Removed size {size.upper()} {product.name} from your bag')
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')
        
        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)

