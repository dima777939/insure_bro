from django.test import TestCase, SimpleTestCase

from account.models import InsuranceCompany


class InsuranceCompanyTest(TestCase):
    """
    Тесты для модели InsuranceCompany
    """
    def setUp(self):
        self.test_company = InsuranceCompany.object.create_user(
            name="Компания",
            description="Лучшая страховая",
            email="company@company.com",
            password="qwerty",
        )

    def test_method_str(self):
        company = InsuranceCompany.object.get(email="company@company.com")
        self.assertEqual(f"{company.name}", "Компания")

