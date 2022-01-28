from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    name = models.CharField(max_length=20, verbose_name='Ниазвание')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    interest_rate = models.SmallIntegerField(max_length=2, verbose_name='Процентная ставка')
    period = models.DurationField(verbose_name='Период страхования')

