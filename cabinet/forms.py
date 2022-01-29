from django import forms

from .models import Product


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['category', 'name', 'price', 'interest_rate', 'period']