from .models import Product
from .documents import ProductDocument


class Filter:
    @staticmethod
    def get_products_filter_main(cd):
        company = cd["company"]
        category = cd["category"]
        min_price = cd["min_price"]
        max_price = cd["max_price"]
        min_interest_rate = cd["min_interest_rate"]
        max_interest_rate = cd["max_interest_rate"]
        period = cd["period"]
        if not company and not category:
            products = Product.objects.filter(
                price__range=(min_price, max_price),
                interest_rate__range=(min_interest_rate, max_interest_rate),
                period=period,
            ).order_by("-date_create")
        elif company and not category:
            products = Product.objects.filter(
                company=company,
                interest_rate__range=(min_interest_rate, max_interest_rate),
                price__range=(min_price, max_price),
                period=period,
            ).order_by("-date_create")
        elif company and category:
            products = Product.objects.filter(
                company=company,
                category=category,
                price__range=(min_price, max_price),
                interest_rate__range=(min_interest_rate, max_interest_rate),
                period=period,
            ).order_by("-date_create")
        elif not company and category:
            products = Product.objects.filter(
                category=category,
                price__range=(min_price, max_price),
                interest_rate__range=(min_interest_rate, max_interest_rate),
                period=period,
            ).order_by("-date_create")
        return products

    @staticmethod
    def get_products_elasticsearch_main(cd):
        search = ProductDocument.search()
        company = cd["company"]
        category = cd["category"]
        name = cd["name"]
        min_price = cd["min_price"]
        max_price = cd["max_price"]
        min_interest_rate = cd["min_interest_rate"]
        max_interest_rate = cd["max_interest_rate"]

        products = (
            search.filter("range", price={"gte": min_price, "lte": max_price}).filter(
                "range",
                interest_rate={
                    "gte": min_interest_rate,
                    "lte": max_interest_rate,
                },
            )
        )
        if name:
            products = products.query(
                "multi_match",
                query=name,
                fields=["name", "category.name", "company.name"],
                fuzziness="auto",
            )
        if company:
            products = products.query(
                "multi_match", query=company.id, fields=["company.id", "company.name"]
            )
        if category:
            products = products.query(
                "multi_match",
                query=category.id,
                fields=["category.id", "category.name"],
            )
        products = products.sort("-date_create")

        return products
