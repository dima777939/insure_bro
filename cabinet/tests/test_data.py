from django.test import TestCase

from cabinet.forms import *
from account.models import InsuranceCompany
from cabinet.models import Category, Product


class DataTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_category = Category.objects.create(
            name="Недвижимость", slug="nedvizhimost"
        )
        test_company = InsuranceCompany.object.create_user(
            name="Компания", description="Лучшая страховая", email="company@company.com"
        )
        test_product = Product.objects.create(
            name="Новая страховка",
            category=test_category,
            company=test_company,
            price="152.11",
            interest_rate=55,
            period="60",
            date_create="2022-02-10",
        )
        cls.test_category = test_category
        cls.test_company = test_company
