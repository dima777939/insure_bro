from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from django.views.generic import ListView

from .forms import ProductForm, ResponseForm, FilterProductForm
from .models import Product, Response, Category
from .filter import Filter
from .tasks import send_email
from .redis_data import RedisData

r = RedisData()


@method_decorator(login_required, name="dispatch")
class CreateProductView(View):
    """
    Представление для создания продукта
    """

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
            # добавление url продукта в Redis
            r.add_key_product_url(product)
            return redirect(reverse("cabinet:create"))
        form = ProductForm(request.POST)
        return render(
            request, "cabinet/create_product.html", {"space": "cabinet", "form": form}
        )


@method_decorator(login_required, name="dispatch")
class ListProductListView(ListView):
    """
    Представление для вывода, в кабинете, списка продуктов компании
    """

    model = Product
    template_name = "cabinet/list_product.html"
    paginate_by = 5
    context_object_name = "products"
    extra_context = {"space": "cabinet"}

    def get_queryset(self):
        company = self.request.user
        products = Product.objects.filter(company_id=company.pk)
        return r.get_products_with_views(products)


@method_decorator(login_required, name="dispatch")
class ListResponseListView(ListView):
    """
    Представление для вывода, в кабинете, списка откликов на продукты компании
    """

    model = Response
    template_name = "cabinet/responses_to_company.html"
    paginate_by = 5
    context_object_name = "responses"
    extra_context = {"space": "cabinet"}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        action = self.kwargs.get("completed", None)
        context["button"] = "active"
        if action == "completed":
            context["button"] = "completed"
        return context

    def get_queryset(self):
        company = self.request.user
        action = self.kwargs.get("completed", None)
        if action == "completed":
            return Response.objects.filter(
                product__company_id=company.pk, finished=True
            )
        return Response.objects.filter(product__company_id=company.pk, finished=False)


@method_decorator(login_required, name="dispatch")
class ResponseAction(View):
    """
    Представление для обновления статуса отклика или его удаления
    """

    def get(self, request, response_id, delete=None):
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


@method_decorator(login_required, name="dispatch")
class ProductDeleteView(View):
    """
    Представление для удаления продукта компании
    """

    def get(self, request, product_id):
        company_id = request.user.id
        product = get_object_or_404(Product, id=product_id)
        product_company_id = product.company.id
        if company_id == product_company_id:
            product.delete()
            r.delete_product_key("product_views", product_id)
            r.delete_product_key("product_url", product_id)
            return redirect(reverse("cabinet:list_product"))
        return redirect(reverse("cabinet:responses_list"))


class MainResponseListView(ListView):
    """
    Представление для вывода списка предложений от всех компаний
    """

    queryset = Product.objects.all()
    template_name = "cabinet/responses_to_product.html"
    paginate_by = 5
    context_object_name = "products"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["form_filter"] = FilterProductForm()
        context["products_count"] = len(self.get_queryset())
        context["page"] = "paginate"
        return context

    def get_queryset(self):
        return r.get_products_with_url(self.queryset)


class MainResponseCategoryListView(MainResponseListView):
    """
    Представление для вывода списка предложений от всех компаний по категориям
    """

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(slug=self.kwargs.get("category_slug", None))
        context["form_filter"] = FilterProductForm(initial={"category": category})
        context["category"] = category
        return context

    def get_queryset(self):
        products_queryset = Product.objects.filter(
            category__slug=self.kwargs.get("category_slug", None)
        )
        return r.get_products_with_url(products_queryset)


class PageResponseView(View):
    """
    Представление для вывода страницы продукта с формой отклика
    """

    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        response_form = ResponseForm()
        # увеличения счётчика просмотров на 1-н в Redis
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
            # отправка email используя Celery
            send_email.delay(new_form.id)
            # увеличения счётчика откликов на 1-н в Redis
            r.incr_key("response", product_id)
            messages.success(
                request, "Ваша заявка отправлена. С вами свяжется менеджер компании"
            )
            return redirect(reverse("cabinet:responses_list"))
        form = ResponseForm(request.POST)
        return render(
            request,
            "cabinet/response_page.html",
            {"response_form": form, "product": product},
        )


class FilterProductView(View):
    """
    Представление для вывода отфильтрованного списка предложений
    """

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
            form_filter = FilterProductForm(request.GET)
            products = r.get_products_with_url(products)
            return render(
                request,
                "cabinet/responses_to_product.html",
                {
                    "products": products,
                    "category": category,
                    "categories": categories,
                    "form_filter": form_filter,
                    "products_count": len(products),
                },
            )
        categories = Category.objects.all()
        form_filter = FilterProductForm(request.GET)
        return render(
            request,
            "cabinet/responses_to_product.html",
            {
                "categories": categories,
                "form_filter": form_filter,
                "products_count": 0,
            },
        )
