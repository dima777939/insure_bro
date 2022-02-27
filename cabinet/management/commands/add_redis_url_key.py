from django.core.management.base import BaseCommand
from django.utils import timezone

from cabinet.redis_data import RedisData

r = RedisData()


class Command(BaseCommand):
    def handle(self, *args, **options):
        r.add_url_product_missing_key()
