import redis

from django.conf import settings
from .models import Product


class RedisData:
    def __init__(self):
        self._r = redis.StrictRedis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True,
        )

    def get_products_with_views(self, products_queryset):
        products = []
        product = {}
        for product_queryset in products_queryset:
            product_views = self._r.get(f"product_views:{product_queryset.id}")
            product_response = self._r.get(f"response:{product_queryset.id}")
            product["product"] = product_queryset
            product["views"] = product_views if product_views else 0
            product["response"] = product_response if product_response else 0
            products.append(product.copy())
        return products

    def get_products_with_url(self, products_queryset):
        products = []
        product = {}
        for product_queryset in products_queryset:
            product_url = self._r.get(f"product_url:{product_queryset.id}")
            product["product"] = product_queryset
            product["url"] = product_url
            products.append(product.copy())
        return products

    def add_key_product_url(self, product):
        self._r.set(f"product_url:{product.id}", f"{product.get_absolute_url()}")

    def incr_key(self, name, product_id):
        self._r.incr(f"{name}:{product_id}")

    def add_url_product_missing_key(self):
        products = Product.objects.all()
        for product in products:
            self.add_key_product_url(product)

    def delete_product_key(self, name,  product_id):
        self._r.delete(f"{name}:{product_id}")
