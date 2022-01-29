from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from .forms import ProductForm


class CreateProductView(View):

    def get(self, request):
        form = ProductForm()
        return render(request, 'cabinet/create_product.html', {'form': form})

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('cabinet:create'))



