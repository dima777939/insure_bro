from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "account"

urlpatterns = [
    path("login/", views.CompanyLoginView.as_view(), name="login"),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="account/company/logout.html"),
        name="logout",
    ),
    path("register/", views.CompanyRegisterView.as_view(), name="register"),
    path("register/success/", views.CompanyRegisterView.as_view(), name="reg_done"),
]
