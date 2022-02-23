from django.urls import path
from . import views

app_name = "cabinet"

urlpatterns = [
    path("", views.MainResponseView.as_view(), name="responses_list"),
    path(
        "<int:product_id>/", views.PageResponseView.as_view(), name="page_response_form"
    ),
    path("create/", views.CreateProductView.as_view(), name="create"),
    path("products/", views.ListProductView.as_view(), name="list_product"),
    path("responses/", views.ListResponseView.as_view(), name="responses_active"),
    path("filter/", views.FilterProductView.as_view(), name="filter_product"),
    path(
        "responses/<str:completed>/",
        views.ListResponseView.as_view(),
        name="responses_completed",
    ),
    path(
        "<slug:category_slug>/",
        views.MainResponseView.as_view(),
        name="responses_list_category",
    ),
]
