from django.urls import path
from . import views

app_name = "cabinet"

urlpatterns = [
    path("create/", views.CreateProductView.as_view(), name="create"),
    path("products/", views.ListProductView.as_view(), name="list_product"),
]
