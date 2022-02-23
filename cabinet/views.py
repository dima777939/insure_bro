import redis
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View

from .forms import ProductForm, ResponseForm, FilterProductForm
from .models import Product, Response, Category
from .filter import Filter
from django.conf import settings
from .tasks import sendgrid_email

r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB,
                      decode_responses=True)


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
        products = self.get_products_with_views(products)
        return render(
            request,
            "cabinet/list_product.html",
            {"space": "cabinet", "products": products},
        )

    @staticmethod
    def get_products_with_views(products_queryset):
        products = []
        product = {}
        for product_queryset in products_queryset:
            product_views = r.get(f"product:{product_queryset.id}:views")
            product["category"] = product_queryset.category.name
            product["name"] = product_queryset.name
            product["period"] = product_queryset.period
            product["interest_rate"] = product_queryset.interest_rate
            product["price"] = product_queryset.price
            product["views"] = product_views if product_views else 0
            products.append(product.copy())
        return products


class ListResponseView(View):
    def get(self, request, completed=None):
        company = request.user
        responses = Response.objects.filter(
            product__company_id=company.pk, finished=False
        )
        if completed:
            responses = Response.objects.filter(
                product__company_id=company.pk, finished=True
            )
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
        form_filter = FilterProductForm()
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)
            form_filter = FilterProductForm(initial={"category": category})
        return render(
            request,
            "cabinet/responses_to_product.html",
            {
                "category": category,
                "categories": categories,
                "products": products,
                "form_filter": form_filter,
            },
        )


class PageResponseView(View):

    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        response_form = ResponseForm()
        response_views = r.incr(f"product:{product_id}:views")
        return render(
            request,
            "cabinet/response_page.html",
            {
                "product": product,
                "response_form": response_form
            },
        )

    def post(self, request, product_id):
        form = ResponseForm(request.POST)
        product = get_object_or_404(Product, id=product_id)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.product = product
            new_form.save()
            sendgrid_email.delay(new_form.id)
            return redirect(reverse("cabinet:responses_list"))
        form = ResponseForm(request.POST)
        return render(request, "cabinet/response_page.html", {"response_form": form, "product": product})


class FilterProductView(View):
    def get(
        self,
        request,
    ):
        form = FilterProductForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            if cd["check_elastic"]:
                products = Filter.get_products_elasticsearch_main(cd)
            else:
                products = Filter.get_products_filter_main(cd)
            category = cd["category"]
            categories = Category.objects.all()
            response_form = ResponseForm()
            form_filter = FilterProductForm(request.GET)
            return render(
                request,
                "cabinet/responses_to_product.html",
                {
                    "products": products,
                    "category": category,
                    "categories": categories,
                    "response_form": response_form,
                    "form_filter": form_filter,
                },
            )
        products = None
        category = None
        categories = Category.objects.all()
        response_form = ResponseForm()
        form_filter = FilterProductForm(request.GET)
        return render(
            request,
            "cabinet/responses_to_product.html",
            {
                "products": products,
                "category": category,
                "categories": categories,
                "response_form": response_form,
                "form_filter": form_filter,
            },
        )
