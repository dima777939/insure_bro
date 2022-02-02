from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from .forms import ProductForm
from .models import Product, Response


class CreateProductView(View):
    def get(self, request):
        form = ProductForm()
        return render(request, "cabinet/create_product.html", {"space": "cabinet", "form": form})

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.company = request.user
            new_form.save()
            return redirect(reverse("cabinet:create"))


class ListProductView(View):
    def get(self, request):
        company = request.user
        products = Product.objects.filter(company_id=company.pk)
        return render(request, "cabinet/list_product.html", {"space": "cabinet", "products": products})


class ListResponseView(View):
    def get(self, request):
        company = request.user
        responses = Response.objects.filter(product__company_id=company.pk)
        return render(
            request, "cabinet/responses_to_product.html", {"space": "cabinet", "responses": responses}
        )

