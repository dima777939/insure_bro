from django.test import SimpleTestCase

from cabinet.forms import *
from .test_data import DataTest


class ProductFormTest(DataTest):
    def test_valid_product_form(self):
        form = ProductForm(
            data={
                "category": self.test_category,
                "name": "Новая страховка",
                "price": 152.11,
                "interest_rate": 55,
                "period": "60",
            }
        )
        self.assertTrue(form.is_valid(), "ProductForm has not passed validation")

    def test_product_form_interest_rate_equal_to_101(self):
        form = ProductForm(
            data={
                "category": self.test_category,
                "name": "Новая страховка",
                "price": 152.11,
                "interest_rate": 101,
                "period": "60",
            }
        )
        self.assertFalse(form.is_valid(), "Cleaned form skips a value > 100")

    def test_product_form_interest_rate_less_than_zero(self):
        form = ProductForm(
            data={
                "category": self.test_category,
                "name": "Новая страховка",
                "price": 152.11,
                "interest_rate": -1,
                "period": "60",
            }
        )
        self.assertFalse(form.is_valid(), "Cleaned form skips a value < 0")


class ResponseFormTest(SimpleTestCase):
    def test_valid_response_form(self):
        form = ResponseForm(
            data={
                "first_name": "test",
                "last_name": "testov",
                "phone": 123456789,
                "email": "test@test.com",
            }
        )
        self.assertTrue(form.is_valid(), "ResponseForm has not passed validation")

    def test_response_form_field_less_that_8(self):
        form = ResponseForm(
            data={
                "first_name": "test",
                "last_name": "testov",
                "phone": 1234567,
                "email": "test@test.com",
            }
        )
        self.assertFalse(form.is_valid(), "Cleaned form skips a value < 8")


class FilterProductFormTest(DataTest):
    def test_valid_filter_product_form(self):
        form = FilterProductForm(
            data={
                "company": self.test_company,
                "category": self.test_category,
                "name": "",
                "min_price": 0,
                "max_price": 80,
                "min_interest_rate": 0,
                "max_interest_rate": 50,
                "period": "60",
                "check_elastic": True,
            }
        )
        self.assertTrue(form.is_valid(), "FilterProductForm has not passed validation")

    def test_product_form_min_price_more_that_max_price(self):
        form = FilterProductForm(
            data={
                "company": self.test_company,
                "category": self.test_category,
                "name": "",
                "min_price": 100,
                "max_price": 80,
                "min_interest_rate": 0,
                "max_interest_rate": 50,
                "period": "60",
                "check_elastic": True,
            }
        )
        self.assertFalse(
            form.is_valid(), "Cleaned form skips a value min_price > max_price"
        )

    def test_product_form_min_interest_rate_more_that_max_interest_rate(self):
        form = FilterProductForm(
            data={
                "company": self.test_company,
                "category": self.test_category,
                "name": "",
                "min_price": 0,
                "max_price": 80,
                "min_interest_rate": 80,
                "max_interest_rate": 50,
                "period": "60",
                "check_elastic": True,
            }
        )
        self.assertFalse(
            form.is_valid(),
            "Cleaned form skips a value min_interest_rate > max_interest_rate",
        )
