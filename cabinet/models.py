from django.db import models
from django.core.validators import RegexValidator
from django.urls import reverse

from account.models import InsuranceCompany


class Category(models.Model):
    """
    Модель таблицы в базе данных с категориями продуктов
    """

    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def get_absolute_url(self):
        return reverse("cabinet:responses_list_category", args=[self.slug])


class Product(models.Model):
    """
    Модель таблицы в базе данных для продуктов компании
    """

    PERIODS = (("30", "1 мес"), ("60", "3 мес"), ("180", "6 мес"), ("365", "12 мес"))
    company = models.ForeignKey(
        InsuranceCompany, on_delete=models.CASCADE, verbose_name="Страховая компания"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="Категория"
    )
    name = models.CharField(max_length=100, verbose_name="Название страховки")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="цена")
    interest_rate = models.SmallIntegerField(verbose_name="Процентная ставка")
    period = models.CharField(
        choices=PERIODS, max_length=6, verbose_name="Период страхования"
    )
    date_create = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "Страховое предложение"
        verbose_name_plural = "Страховые предложения"
        ordering = ["-date_create"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("cabinet:page_response_form", args=[self.id])


class Response(models.Model):
    """
    Модель таблицы в базе данных для откликов на продукты компании
    """

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Вид страховки"
    )
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    phone_regex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phone = models.CharField(
        validators=[phone_regex],
        max_length=16,
        blank=True,
        verbose_name="Номер телефона",
    )
    email = models.EmailField(max_length=50, verbose_name="Электронная почта")
    finished = models.BooleanField(default=False, verbose_name="Отклик обработан")

    class Meta:
        verbose_name = "Отклик"
        verbose_name_plural = "Отклики"
        ordering = ["first_name"]
