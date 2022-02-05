from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View

from .forms import ProductForm, ResponseForm
from .models import Product, Response, Category


class CreateProductView(View):
    def get(self, request):
        form = ProductForm()
        return render(
            request, "cabinet/create_product.html", {"space": "cabinet", "form": form}
        )

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
        return render(
            request,
            "cabinet/list_product.html",
            {"space": "cabinet", "products": products},
        )


class ListResponseView(View):
    def get(self, request, completed=None):
        company = request.user
        responses = Response.objects.filter(product__company_id=company.pk, finished=False)
        if completed:
            responses = Response.objects.filter(product__company_id=company.pk, finished=True)
        return render(
            request,
            "cabinet/responses_to_company.html",
            {"space": "cabinet", "responses": responses},
        )


class MainResponseView(View):
    def get(self, request, category_slug=None):
        category = None
        categories = Category.objects.all()
        products = Product.objects.all()
        response_form = ResponseForm()
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)
        return render(
            request,
            "cabinet/responses_to_product.html",
            {
                "category": category,
                "categories": categories,
                "products": products,
                "response_form": response_form,
            },
        )

    def post(self, request, product_id):
        form = ResponseForm(request.POST)
        product = get_object_or_404(Product, id=product_id)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.product = product
            new_form.save()
            return redirect(reverse("cabinet:responses_list"))

