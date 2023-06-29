from django import forms

from .models import Delivery

class ShippingDetailsForm(forms.Form):
    name = forms.CharField(label="Name", max_length=200, widget=forms.TextInput())
    surname = forms.CharField(label="Surname", max_length=200, widget=forms.TextInput())
    email = forms.EmailField(label="Email", max_length=200, widget=forms.TextInput())
    phone_number = forms.CharField(label="Phone Number", max_length=10, widget=forms.TextInput())
    address = forms.CharField(label="Address", max_length=200, widget=forms.TextInput())
    city = forms.CharField(label="City", max_length=200, widget=forms.TextInput())
    state = forms.CharField(label="State", max_length=200, widget=forms.TextInput())
    zipcode = forms.CharField(label="Zipcode", max_length=200, widget=forms.TextInput())
    delivery = forms.ModelChoiceField(queryset=Delivery.objects.all())