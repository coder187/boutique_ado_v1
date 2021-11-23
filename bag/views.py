from django.shortcuts import render, redirect


# Create your views here.
def view_bag(request):
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')

    bag = request.session.get('bag', {})

    # create a dictionary to hold the session variable 'bag'. If there is no bag session var, create an empty one.
    # if the current item_id exists in the session var, increment by quantiy else set bag.item_id = quantity
    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity

    # overwrite session bag var with updated bag
    request.session['bag'] = bag
    print(request.session['bag'])
    return redirect(redirect_url)
