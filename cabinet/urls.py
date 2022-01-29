from django.urls import path
from . import views

app_name = 'cabinet'

urlpatterns = [
    path('create/', views.CreateProductView.as_view(), name='create'),
]