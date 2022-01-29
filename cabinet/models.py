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

    PERIODS = (
        ('1 мес', '30'),
        ('3 мес', '90'),
        ('6 мес', '180'),
        ('12 мес', '365')
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    name = models.CharField(max_length=20, verbose_name='Название страховки')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='цена')
    interest_rate = models.SmallIntegerField(max_length=2, verbose_name='Процентная ставка')
    period = models.CharField(choices=PERIODS, verbose_name='Период страхования')

    class Meta:
        verbose_name = 'Страховое предложение'
        verbose_name_plural = 'Страховые предложения'

    def __str__(self):
        return self.name

