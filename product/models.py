from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Currency(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    symbol = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Currencies'

    def __str__(self):
        return self.name
    
class Color(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Size(models.Model):
    name = models.CharField(max_length=255)
    shortcut = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    color = models.ForeignKey(Color, on_delete=models.SET_DEFAULT, default=1)
    sizes = models.ManyToManyField(Size)
    currency = models.ForeignKey(Currency, related_name='items', on_delete=models.CASCADE, default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images', blank=True, null=True)
    available_quantity = models.IntegerField(default=0, blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    size = models.ForeignKey(Size, on_delete=models.SET_DEFAULT, default=1)
    device = models.CharField(max_length=255, null=True, blank=True)
    payed = models.BooleanField(default=False)
    code = models.CharField(max_length=255, null=True, blank=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class Delivery(models.Model):
    name = models.CharField(max_length=200, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, default=1)

    class Meta:
        verbose_name_plural = 'Deliveries'

    def __str__(self):
        return f'{self.name} - {self.currency.symbol}{self.price}'
    
class ShippingDetails(models.Model):
    customer_name = models.CharField(max_length=200, null=False)
    customer_surname = models.CharField(max_length=200, null=False)
    email = models.EmailField(max_length=200, null=False, default='email@email.com')
    phone_number = models.CharField(max_length=12, default='000000000000')
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)
    delivery = models.ForeignKey(Delivery, on_delete=models.SET_NULL, null=True)
    device = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Shipping detail'

    def __str__(self):
        return self.address
    
class Order(models.Model):
    device = models.CharField(max_length=255, null=True, blank=True)
    shipping_details = models.ForeignKey(ShippingDetails, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, null=True)
    orderitems = models.ManyToManyField(OrderItem)
    payed = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        total = self.orderitems.aggregate(total=Sum('quantity'))['total'] + self.shipping_details.delivery.price 
        return total if total else 0

    @property
    def get_cart_items(self):
        items_count = self.orderitems.count()
        return items_count
