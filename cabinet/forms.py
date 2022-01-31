from django import forms

from .models import Product, Response


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["category", "name", "price", "interest_rate", "period"]


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ["first_name", "last_name", "phone", "email"]
