from django import forms

from .models import Product, Response, Category
from account.models import InsuranceCompany


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["category", "name", "price", "interest_rate", "period"]


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ["first_name", "last_name", "phone", "email"]

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if not phone.isdigit():
            raise forms.ValidationError("Номер должен состоять из цифр")
        if 8 > int(phone) > 16:
            raise forms.ValidationError("Номер телефона должен быть от 8 до 16 цифр")
        return phone


class FilterProductForm(forms.Form):
    PERIODS = (("30", "1 мес"), ("60", "3 мес"), ("180", "6 мес"), ("365", "12 мес"))

    company = forms.ModelChoiceField(
        queryset=InsuranceCompany.object.all(),
        required=False,
        label="Страховая компания",
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), required=False, label="Категория"
    )
    name = forms.CharField(
        min_length=3, max_length=20, required=False, label="Описание"
    )
    min_price = forms.IntegerField(
        initial=0, min_value=0, max_value=99999998, label="Минимальная цена"
    )
    max_price = forms.IntegerField(
        initial=9999999999,
        min_value=100,
        max_value=9999999999,
        label="Максимальная цена",
    )
    min_interest_rate = forms.IntegerField(
        initial=0, min_value=0, max_value=90, label="Минимальная % ставка"
    )
    max_interest_rate = forms.IntegerField(
        initial=100, min_value=5, max_value=100, label="Максимальная % ставка"
    )
    period = forms.ChoiceField(choices=PERIODS, required=False, label="Период")

    check_elastic = forms.BooleanField(
        initial=False, required=False, label="Поиск через elastic"
    )

    def clean_max_price(self):
        min = self.cleaned_data.get("min_price")
        max = self.cleaned_data.get("max_price")
        if max < min:
            raise forms.ValidationError(
                "Значение мин цены не должно быть больше макс цены"
            )
        return max

    def clean_max_interest_rate(self):
        max = self.cleaned_data.get("max_interest_rate")
        min = self.cleaned_data.get("min_interest_rate")
        if max < min:
            raise forms.ValidationError(
                "Значение мин процентной ставки не должно быть больше макс процентной ставки"
            )
        return max
