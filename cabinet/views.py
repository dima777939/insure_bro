from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View

from .forms import ProductForm, ResponseForm, FilterProductForm
from .models import Product, Response, Category
from .filter import Filter
from .tasks import sendgrid_email
from .redis_data import RedisData

r = RedisData()


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
            product = get_object_or_404(Product, id=new_form.id)
            r.add_key_product_url(product)
            return redirect(reverse("cabinet:create"))


class ListProductView(View):
    def get(self, request):
        company = request.user
        products = Product.objects.filter(company_id=company.pk)
        products = r.get_products_with_views(products)
        return render(
            request,
            "cabinet/list_product.html",
            {"space": "cabinet", "products": products},
        )


class ListResponseView(View):
    def get(self, request, completed=None):
        company = request.user
        responses = Response.objects.filter(
            product__company_id=company.pk, finished=False
        )
        button = "active"
        if completed == "completed":
            responses = Response.objects.filter(
                product__company_id=company.pk, finished=True
            )
            button = "completed"
        return render(
            request,
            "cabinet/responses_to_company.html",
            {"space": "cabinet", "responses": responses, "button": button},
        )


class ResponseAction(View):
    def get(self, request, response_id, delete=None):
        if request.user.is_authenticated:
            company_id = request.user.id
            response = get_object_or_404(Response, id=response_id)
            response_company_id = response.product.company.id
            if company_id == response_company_id:
                if delete == "delete":
                    response.delete()
                    r.delete_product_key("response", response_id)
                    return redirect(
                        reverse("cabinet:responses_completed", args=["completed"])
                    )
                else:
                    Response.objects.filter(id=response_id).update(finished=True)
                    return redirect(reverse("cabinet:responses_active"))
            return redirect(reverse("cabinet:responses_list"))


class ProductDeleteView(View):
    def get(self, request, product_id):
        if request.user.is_authenticated:
            company_id = request.user.id
            product = get_object_or_404(Product, id=product_id)
            product_company_id = product.company.id
            if company_id == product_company_id:
                product.delete()
                r.delete_product_key("product_views", product_id)
                r.delete_product_key("product_url", product_id)
                return redirect(reverse("cabinet:list_product"))
            return redirect(reverse("cabinet:responses_list"))


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
        products = r.get_products_with_url(products)
        return render(
            request,
            "cabinet/responses_to_product.html",
            {
                "category": category,
                "categories": categories,
                "products": products,
                "form_filter": form_filter,
                "products_count": len(products),
            },
        )


class PageResponseView(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        response_form = ResponseForm()
        r.incr_key("product_views", product_id)
        return render(
            request,
            "cabinet/response_page.html",
            {"product": product, "response_form": response_form},
        )

    def post(self, request, product_id):
        form = ResponseForm(request.POST)
        product = get_object_or_404(Product, id=product_id)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.product = product
            new_form.save()
            sendgrid_email.delay(new_form.id)
            r.incr_key("response", product_id)
            return redirect(reverse("cabinet:responses_list"))
        form = ResponseForm(request.POST)
        return render(
            request,
            "cabinet/response_page.html",
            {"response_form": form, "product": product},
        )


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
            products = r.get_products_with_url(products)
            return render(
                request,
                "cabinet/responses_to_product.html",
                {
                    "products": products,
                    "category": category,
                    "categories": categories,
                    "response_form": response_form,
                    "form_filter": form_filter,
                    "products_count": len(products),
                },
            )
        products = None
        category = None
        categories = Category.objects.all()
        response_form = ResponseForm()
        form_filter = FilterProductForm(request.GET)
        products = r.get_products_with_url(products)
        return render(
            request,
            "cabinet/responses_to_product.html",
            {
                "products": products,
                "category": category,
                "categories": categories,
                "response_form": response_form,
                "form_filter": form_filter,
                "products_count": len(products),
            },
        )
