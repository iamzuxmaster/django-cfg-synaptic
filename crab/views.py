from django.shortcuts import render
from control.models import Office
from crab.models import Order, Task

def base_context(request):
    try: 
        code = request.build_absolute_uri().split('?')[1]
    except: 
        code = None
    office = Office.objects.last()
    with_order_item = False
    context = {
        "office": office,
        "code": code, 
        'with_orderitem': with_order_item
    }
    return context

def crab_index(request): 
    new_orders = Order.objects.filter(checkout=True)
    ls = []
    for new_order in new_orders:
        if new_order.moderator is not None:
            ls.append(new_order)
    context = {
        "base": base_context(request),
        "new_orders": ls
    }
    return render(request, "crab/index.html", context)
