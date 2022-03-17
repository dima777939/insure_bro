from cabinet.models import Category, Product

from .test_data import DataTest


class CategoryModelTest(DataTest):
    def test_get_absolute_url(self):
        category = Category.objects.get(slug="nedvizhimost")
        self.assertEqual(
            category.get_absolute_url(),
            "/cabinet/nedvizhimost/",
            "model 'Category' failed test get_absolute_url",
        )

    def test_method_str(self):
        category = Category.objects.get(slug="nedvizhimost")
        category_name = f"{category.name}"
        self.assertEqual(
            category_name,
            str(category),
            "method '__str__' model 'Category' does not return model name",
        )


class ProductModelTest(DataTest):
    def test_get_absolute_url(self):
        product = Product.objects.get(name="Новая страховка")

        self.assertEqual(
            product.get_absolute_url(),
            f"/cabinet/{product.id}/",
            "model 'Product' failed test get_absolute_url",
        )

    def test_method_str(self):
        product = Product.objects.get(name="Новая страховка")
        product_name = f"{product.name}"
        self.assertEqual(
            product_name,
            str(product),
            "method '__str__' model 'Product' does not return model name",
        )
