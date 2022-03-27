from django.test import TestCase, SimpleTestCase

from account.views import *


class CompanyRegisterView(TestCase):

    def test_view_url_accessible_by_name(self):
        """
        Тест проверки url
        """
        resp = self.client.get(reverse("account:login"))
        self.assertEqual(resp.status_code, 200)

    def test_uses_correct_template(self):
        """
        Тест использования правильного шаблона
        """
        resp = self.client.get(reverse("account:register"))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "account/company/registration.html")

    def test_redirect_create_on_success_post(self):
        """
        Тест пост запроса, при валидной форме
        """
        data = {
            "name": "Компания",
            "description": "Страховая компания",
            "email": "company@company.com",
            "password": "qwerty",
            "password2": "qwerty"
        }
        resp = self.client.post(reverse("account:reg_done"), data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "account/company/reg_done.html")

    def test_redirect_on_invalid_form(self):
        """
        Тест пост запроса, при не валидной форме
        """
        data = {
            "name": "Компания",
            "description": "Страховая компания",
            "email": "company@company.com",
            "password": "qwerty",
            "password2": "qwerty1"
        }
        resp = self.client.post(reverse("account:reg_done"), data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "account/company/registration.html")