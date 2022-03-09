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
    path(
        "product/delete/<int:product_id>/",
        views.ProductDeleteView.as_view(),
        name="delete_product",
    ),
    path("responses/", views.ListResponseView.as_view(), name="responses_active"),
    path("filter/", views.FilterProductView.as_view(), name="filter_product"),
    path(
        "responses/<str:completed>/",
        views.ListResponseView.as_view(),
        name="responses_completed",
    ),
    path(
        "responses/action/<int:response_id>/",
        views.ResponseAction.as_view(),
        name="response_finished",
    ),
    path(
        "responses/action/<int:response_id>/<str:delete>/",
        views.ResponseAction.as_view(),
        name="response_delete",
    ),
    path(
        "<slug:category_slug>/",
        views.MainResponseView.as_view(),
        name="responses_list_category",
    ),
]
