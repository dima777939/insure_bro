from django import forms

from account.models import InsuranceCompany


class CompanyLoginForm(forms.Form):
    email = forms.EmailField(label='Электронная почта')
    password = forms.CharField(label='Введите пароль', widget=forms.PasswordInput)


class CompanyRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = InsuranceCompany
        fields = ('name', 'description', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']