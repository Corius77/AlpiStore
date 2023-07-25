import json

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.db.models import Max, Min, Q
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required

from paypal.standard.forms import PayPalPaymentsForm

from .models import Category, OrderItem, Product, Size, Color, ShippingDetails, Order
from .forms import ShippingDetailsForm

def list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    device = request.COOKIES.get('device')
    orderitems = OrderItem.objects.filter(device=device, payed=False)
    orderitems_count = orderitems.count()
    sizes = Size.objects.all()
    colors = Color.objects.all()

    max_price_product = Product.objects.aggregate(max_price=Max('price'))
    max_price = max_price_product['max_price']
    min_price_product = Product.objects.aggregate(min_price=Min('price'))
    min_price = min_price_product['min_price']
    filter_sizes = request.GET.getlist('sizes')
    filter_color = request.GET.getlist('colors')
    filter_category = request.GET.getlist('categories')

    if 'min_price' in request.GET:    
        filter_price1 = request.GET.get('min_price')
        filter_price2 = request.GET.get('max_price')
        if filter_price1 =='':
            filter_price1=0
        products = products.filter(price__range=(filter_price1, filter_price2))

    if filter_sizes:
        products = products.filter(sizes__id__in=filter_sizes).distinct()

    if filter_color:
        products = products.filter(color__id__in=filter_color)

    if filter_category:
        products = products.filter(category__id__in=filter_category)
    
    return render(request, 'product/list.html', {
        'products': products,
        'orderitems_count': orderitems_count,
        'categories': categories,
        'max_price': max_price,
        'min_price': min_price,
        'sizes': sizes,
        'colors': colors
    })

def detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    sizes = product.sizes.all()
    device = request.COOKIES.get('device')
    orderitems = OrderItem.objects.filter(device=device, payed=False)
    orderitems_count = orderitems.count()
    smallest_id = product.sizes.order_by('id').values_list('id', flat=True).first()

    print(request)

    return render(request, 'product/detail.html', {
        'product': product,
        'orderitems_count': orderitems_count,
        'sizes': sizes,
        'smallest_id': smallest_id
    })

def cart(request):
    cart = json.loads(request.COOKIES.get('cart'))
    device = request.COOKIES.get('device')
    
    for i in cart:
        product_id = i.split('-')[0]
        size_id = i.split('-')[1]
        product = Product.objects.get(id=product_id)
        size = Size.objects.get(id=size_id)
        orderitem, created = OrderItem.objects.get_or_create(product=product, device=device, size=size, code=i, payed=False)

        orderitem.quantity = cart[i]["quantity"]

        if orderitem.quantity > 0:
            orderitem.save()     
        else:
            orderitem.delete()

    orderitems = OrderItem.objects.filter(device=device, payed=False)
    orderitems_count = orderitems.count()

    totalprice = 0
    for tp in orderitems:
        totalprice += tp.get_total

    itemscount = 0
    for ic in orderitems:
        itemscount += ic.quantity

    return render(request, 'product/cart.html', {
        'orderitems': orderitems,
        'totalprice': totalprice,
        'orderitems_count': orderitems_count,
        'itemscount': itemscount
    })

def details(request):
    device = request.COOKIES.get('device')
    orderitems = OrderItem.objects.filter(device=device, payed=False)
    orderitems_count = orderitems.count()
    shipping_details, created = ShippingDetails.objects.get_or_create(device=device)

    itemsprice = 0
    for ip in orderitems:
        itemsprice += ip.get_total

    itemscount = 0
    for ic in orderitems:
        itemscount += ic.quantity    

    totalprice = 0
    try:
        totalprice = itemsprice + shipping_details.delivery.price
    except:
        totalprice = itemsprice

    if request.method == 'POST':
        form = ShippingDetailsForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            delivery = form.cleaned_data['delivery']

            shipping_details.customer_name = name
            shipping_details.customer_surname = surname
            shipping_details.email = email
            shipping_details.phone_number = phone_number
            shipping_details.address = address
            shipping_details.city = city
            shipping_details.state = state
            shipping_details.zipcode = zipcode
            shipping_details.device = device
            shipping_details.delivery = delivery

            shipping_details.save()

            return redirect('/products/checkout')
    else:
        form = ShippingDetailsForm()

    return render(request, 'product/details.html', {
        'shipping_details': shipping_details,
        'orderitems': orderitems,
        'form': form,
        'orderitems_count': orderitems_count,
        'itemsprice': itemsprice,
        'itemscount': itemscount,
        'totalprice': totalprice
    })

def checkout(request):
    device = request.COOKIES.get('device')
    shipping_details = ShippingDetails.objects.get(device=device)
    orderitems = OrderItem.objects.filter(device=device, payed=False)

    itemsprice = 0
    for ip in orderitems:
        itemsprice += ip.get_total

    itemscount = 0
    for ic in orderitems:
        itemscount += ic.quantity    

    totalprice = 0
    try:
        totalprice = itemsprice + shipping_details.delivery.price
    except:
        totalprice = itemsprice
    
    order, created = Order.objects.get_or_create(device=device, shipping_details=shipping_details, payed=False)
    order.save()
    order.orderitems.set(orderitems)
    order = Order.objects.get(device=device, payed=False)

    orderitems_count = order.get_cart_items

    orderitems_list = order.orderitems.all()

    return render(request, 'product/checkout.html', {
        'order': order,
        'orderitems_list': orderitems_list,
        'orderitems': orderitems,
        'shipping_details': shipping_details,
        'itemsprice': itemsprice,
        'itemscount': itemscount,
        'totalprice': totalprice,
        'orderitems_count': orderitems_count,
    })

def paypal_success(request):
    device = request.COOKIES.get('device')
    order = Order.objects.get(device=device, payed=False)

    order.payed = True
    order.save()

    return HttpResponse('Płatność zatwierdzona. Status zamówienia został zaktualizowany.')

@staff_member_required
def payed_orders(request):
    device = request.COOKIES.get('device')
    orders = Order.objects.filter(payed=True, complete=False)
    orderitems = OrderItem.objects.filter(order__in=orders)
    order_status = request.POST.get('order_status')
    orders_count = orders.count()

    if order_status:
        order_id = int(order_status)
        order = get_object_or_404(Order, id=order_id)

        order.complete = True
        order.save()


    return render(request, 'product/orders.html', {
        'orders': orders,
        'orderitems': orderitems,
        'orders_count': orders_count
    })