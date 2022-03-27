from django.test import TestCase

from account.models import InsuranceCompany
from cabinet.models import Category, Product, Response


class DataTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_category = Category.objects.create(
            name="Недвижимость", slug="nedvizhimost"
        )
        cls.test_company = InsuranceCompany.object.create_user(
            name="Компания",
            description="Лучшая страховая",
            email="company@company.com",
            password="qwerty",
        )
        test_product = Product.objects.create(
            name="Новая страховка",
            category=cls.test_category,
            company=cls.test_company,
            price="152.11",
            interest_rate=55,
            period="60",
            date_create="2022-02-10",
        )


class DataTestList(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_category = Category.objects.create(
            name="Недвижимость", slug="nedvizhimost"
        )
        cls.test_company = InsuranceCompany.object.create_user(
            id=1,
            name="Компания",
            description="Лучшая страховая",
            email="company@company.com",
            password="qwerty",
        )
        cls.test_company1 = InsuranceCompany.object.create_user(
            id=2,
            name="Компания1",
            description="Лучшая страховая1",
            email="company1@company.com",
            password="qwerty",
        )
        for num in range(1, 10):
            Product.objects.create(
                name=f"Новая страховка{num}",
                category=cls.test_category,
                company=cls.test_company,
                price=f"1234{num}",
                interest_rate=num,
                period="60",
                date_create="2022-02-10",
            )
        for num in range(1, 10):
            Product.objects.create(
                name=f"Новая страховка{num}",
                category=cls.test_category,
                company=cls.test_company1,
                price=f"1234{num}",
                interest_rate=num,
                period="60",
                date_create="2022-02-10",
            )
        cls.products = Product.objects.filter(company__email="company@company.com")[:9]
        cls.products1 = Product.objects.filter(company__email="company1@company.com")[
            :9
        ]
        for product in cls.products:
            Response.objects.create(
                product=product,
                first_name=f"name{product.id}",
                last_name=f"lastname{product.id}",
                phone=12345678,
                email=f"test{product.id}@test.com",
                finished=False,
            )
        for product1 in cls.products1:
            Response.objects.create(
                product=product1,
                first_name=f"name{product1.id}",
                last_name=f"lastname{product1.id}",
                phone=12345678,
                email=f"test{product1.id}@test.com",
                finished=False,
            )
