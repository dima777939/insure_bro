from django.test import TestCase, SimpleTestCase

from account.forms import *


class CompanyLoginFormTest(SimpleTestCase):

    def test_valid_login_form(self):
        form = CompanyLoginForm(
            data={
                "email": "company@company.com",
                "password": "qwerty"
            }
        )
        self.assertTrue(form.is_valid())

    def test_invalid_email_field(self):
        form = CompanyLoginForm(
            data={
                "email": "companycompany.com",
                "password": "qwerty"
            }
        )
        self.assertFalse(form.is_valid())


