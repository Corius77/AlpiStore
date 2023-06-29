from django.contrib import admin

from .models import Category, Currency, Product, OrderItem, Order, Delivery ,ShippingDetails, Color, Size

admin.site.register(Category)
admin.site.register(Currency)
admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Delivery)
admin.site.register(ShippingDetails)
admin.site.register(Color)
admin.site.register(Size)


