from .models import Product
from .documents import ProductDocument


class Filter:
    """
    Фильтрация продуктов по введенным параметрам
    """

    def __init__(self, cd):
        self.company = cd["company"]
        self.category = cd["category"]
        self.min_price = cd["min_price"]
        self.max_price = cd["max_price"]
        self.min_interest_rate = cd["min_interest_rate"]
        self.max_interest_rate = cd["max_interest_rate"]
        self.period = cd["period"]
        self.name = cd["name"]

    def get_products_filter_main(self):
        """
        Использует Django ORM для фильтрации
        """
        products = Product.objects.filter(
            price__range=(self.min_price, self.max_price),
            interest_rate__range=(self.min_interest_rate, self.max_interest_rate),
        ).order_by("-date_create")
        if self.company:
            products = products.filter(company=self.company)
        if self.category:
            products = products.filter(category=self.category)
        if self.period:
            products = products.filter(period=self.period)
        return products

    def get_products_elasticsearch_main(self):
        """
        Использует elasticsearch для фильтрации
        """
        search = ProductDocument.search().extra(size=100)
        products = search.filter(
            "range", price={"gte": self.min_price, "lte": self.max_price}
        ).filter(
            "range",
            interest_rate={
                "gte": self.min_interest_rate,
                "lte": self.max_interest_rate,
            },
        )
        if self.name:
            products = products.query(
                "multi_match",
                query=self.name,
                fields=["name", "category.name", "company.name"],
                fuzziness="auto",
            )
        if self.company:
            products = products.query(
                "multi_match",
                query=self.company.id,
                fields=["company.id", "company.name"],
            )
        if self.category:
            products = products.query(
                "multi_match",
                query=self.category.id,
                fields=["category.id", "category.name"],
            )
        products = products.sort("-date_create")

        return products
