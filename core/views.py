from django.shortcuts import render

from .models import Message
from .forms import MessageForm

from product.models import Category, Currency, Product, OrderItem

def index(request):
    products = Product.objects.all()[0:4]
    device = request.COOKIES.get('device')
    orderitems = OrderItem.objects.filter(device=device, payed=False)
    orderitems_count = orderitems.count()

    return render(request, 'core/index.html', {
        'products': products,
        'orderitems_count': orderitems_count
    })

def contact(request):
    device = request.COOKIES.get('device')
    orderitems = OrderItem.objects.filter(device=device, payed=False)
    orderitems_count = orderitems.count()

    if request.method == 'POST':
        form = MessageForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            topic = form.cleaned_data['topic']

            message = Message(name=name, email=email, message=message, topic=topic)
            message.save()
    else:
        form = MessageForm()

    return render(request, 'core/contact.html', {
        'orderitems_count': orderitems_count,
        'form': form
    })
