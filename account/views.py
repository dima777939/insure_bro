from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

from .forms import CompanyLoginForm, CompanyRegistrationForm


class CompanyRegisterView(View):

    def get(self, request):
        reg_form = CompanyRegistrationForm()
        return render(request, 'account/company/registration.html', {'reg_form': reg_form})

    def post(self, request):
        reg_form = CompanyRegistrationForm(request.POST)
        if reg_form.is_valid():
            new_company = reg_form.save(commit=False)
            new_company.set_password(reg_form.cleaned_data['password'])
            new_company.save()
            return render(request, 'account/company/reg_done.html', {'new_company': new_company})
        else:
            return HttpResponse('None')


class CompanyLoginView(View):

    def get(self, request):
        form = CompanyLoginForm()
        return render(request, 'account/company/login.html', {'form': form})

    def post(self, request):
        form = CompanyLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            company = authenticate(request, email=cd['email'], password=cd['password'])
        if company is not None:
            if company.is_active:
                login(request, company)
                return redirect(reverse('account:register'))
                # return redirect(reverse('mane_page:mane_page'))
            else:
                return HttpResponse('Аккаунт не активен')
        else:
            return HttpResponse('Неправильный логин или пароль')
