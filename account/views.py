from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.http import HttpResponse

from .forms import CompanyRegistrationForm


class CompanyRegisterView(View):
    def get(self, request):
        reg_form = CompanyRegistrationForm()
        return render(
            request, "account/company/registration.html", {"reg_form": reg_form}
        )

    def post(self, request):
        reg_form = CompanyRegistrationForm(request.POST)
        if reg_form.is_valid():
            new_company = reg_form.save(commit=False)
            new_company.set_password(reg_form.cleaned_data["password"])
            new_company.save()
            return render(
                request, "account/company/reg_done.html", {"new_company": new_company}
            )
        reg_form = CompanyRegistrationForm(request.POST)
        return render(
            request, "account/company/registration.html", {"reg_form": reg_form}
        )
