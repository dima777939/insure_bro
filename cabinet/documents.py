from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import Product, Category
from account.models import InsuranceCompany


@registry.register_document
class ProductDocument(Document):
    company = fields.ObjectField(
        properties={"id": fields.IntegerField(), "name": fields.TextField()}
    )
    category = fields.ObjectField(
        properties={"id": fields.IntegerField(), "name": fields.TextField()}
    )

    class Index:
        name = "product"
        settings = {"number_of_shards": 1, "number_of_replicas": 1}

    class Django:
        model = Product
        fields = [
            "name",
            "price",
            "interest_rate",
            "period",
        ]
        related_models = [Category, InsuranceCompany]

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, InsuranceCompany):
            return related_instance.product_set.all()
        elif isinstance(related_instance, Category):
            return related_instance.product_set.all()
