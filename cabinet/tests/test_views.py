from typing import List

from cabinet.views import *
from cabinet.models import Category, Product
from cabinet.tests.test_data import DataTestList, DataTest


class CreateProductViewTest(DataTest):
    """
    Тесты для представления CreateProductView
    """

    def test_redirect_if_not_logged_in(self):
        """
        Тест редиректа если пользователь не авторизован
        """
        resp = self.client.get(reverse("cabinet:create"))
        self.assertRedirects(
            resp,
            "/account/login/?next=/cabinet/create/",
            msg_prefix="When an unauthorized user gets access, he does not redirect to the authorization page",
        )

    def test_logged_in_uses_correct_template(self):
        """
        Тест ответа на запрос и использования правильного шаблона для авторизации пользователя
        """
        login = self.client.login(email="company@company.com", password="qwerty")
        resp = self.client.get(reverse("cabinet:create"))
        self.assertEqual(str(resp.context["user"]), "Компания")
        self.assertEqual(resp.status_code, 200, "No access to the page")
        self.assertTemplateUsed(
            resp, "cabinet/create_product.html", "The incorrect template is used"
        )

    def test_redirect_cabinet_create_on_success_post(self):
        """
        Тест пост запроса, при валидной форме для авторизованного пользователя
        """
        login = self.client.login(email="company@company.com", password="qwerty")
        data = {
            "category": self.test_category.pk,
            "name": "Новая страховка",
            "price": "15214",
            "interest_rate": "25",
            "period": "60",
        }
        resp = self.client.post(reverse("cabinet:create"), data=data)
        self.assertRedirects(
            resp,
            reverse("cabinet:create"),
            msg_prefix="With a successful post request redirect to another url",
        )

    def test_form_invalid_price_field(self):
        """
        Тест текста ошибки, при невалидном поле цена для авторизованного пользователя
        """
        login = self.client.login(email="company@company.com", password="qwerty")

        data = {
            "category": self.test_category,
            "name": "Новая страховка",
            "price": "123456789",
            "interest_rate": "25",
            "period": "60",
        }
        resp = self.client.post(reverse("cabinet:create"), data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertFormError(
            resp,
            "form",
            "price",
            "Убедитесь, что вы ввели не более 8 цифр перед запятой.",
            "Incorrect error text in the price field",
        )

    def test_form_invalid_interest_rate_field(self):
        """
        Тест текста ошибки формы, при невалидном поле процентная ставка
        и используемого шаблона для авторизованного пользователя
        """
        login = self.client.login(email="company@company.com", password="qwerty")
        data = {
            "category": self.test_category,
            "name": "Новая страховка",
            "price": "12345678",
            "interest_rate": "123",
            "period": "120",
        }
        resp = self.client.post(reverse("cabinet:create"), data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertFormError(
            resp,
            "form",
            "interest_rate",
            "Процентная ставка может быть в пределах от 0 до 100",
            "Incorrect error text in the interest_rate field",
        )
        self.assertTemplateUsed(
            resp, "cabinet/create_product.html", "The incorrect template is used"
        )


class ListProductListViewTest(DataTestList):
    """
    Тесты для представления CreateProductView
    """

    def test_view_url_accessible_by_name(self):
        """
        Тест доступа авторизованного пользователя
        """
        login = self.client.login(email="company@company.com", password="qwerty")
        resp = self.client.get(reverse("cabinet:list_product"))
        self.assertEqual(str(resp.context["user"]), "Компания")
        self.assertEqual(resp.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        """
        Тест редиректа если пользователь не авторизован
        """
        resp = self.client.get(reverse("cabinet:list_product"))
        self.assertRedirects(
            resp,
            "/account/login/?next=/cabinet/products/",
            msg_prefix="When an unauthorized user gets access, he does not redirect to the authorization page",
        )

    def test_logged_in_uses_correct_template(self):
        """
        Тест ответа на запрос и использования правильного шаблона для авторизации пользователя
        """
        login = self.client.login(email="company@company.com", password="qwerty")
        resp = self.client.get(reverse("cabinet:list_product"))
        self.assertEqual(str(resp.context["user"]), "Компания")
        self.assertEqual(resp.status_code, 200, "No access to the page")
        self.assertTemplateUsed(
            resp, "cabinet/list_product.html", "The incorrect template is used"
        )

    def test_only_test_company_product_in_list(self):
        """
        Тест проверки получаемого списка продуктов, что они принадлежат компании test_company
        """
        login = self.client.login(email="company@company.com", password="qwerty")
        resp = self.client.get(reverse("cabinet:list_product"))
        self.assertEqual(str(resp.context["user"]), "Компания")
        self.assertEqual(resp.status_code, 200, "No access to the page")
        self.assertTrue(
            "products" in resp.context, "The context does not contain product"
        )

        for product in resp.context["products"]:
            product = product.get("product")
            self.assertEqual(
                resp.context["user"],
                product.company,
                "The context contains products that did not belong to the test_company",
            )

    def test_pagination_first_page(self):
        """
        Тест проверки количества элементов на первой странице
        """
        login = self.client.login(email="company@company.com", password="qwerty")
        resp = self.client.get(reverse("cabinet:list_product"))
        self.assertEqual(str(resp.context["user"]), "Компания")
        self.assertEqual(resp.status_code, 200, "No access to the page")
        self.assertTrue("is_paginated" in resp.context)
        self.assertTrue(resp.context["is_paginated"] == True)
        self.assertTrue(len(resp.context["products"]) == 5)

    def test_pagination_second_page(self):
        """
        Тест проверки количества элементов на второй странице
        """
        login = self.client.login(email="company@company.com", password="qwerty")
        resp = self.client.get(reverse("cabinet:list_product") + "?page=2")
        self.assertEqual(str(resp.context["user"]), "Компания")
        self.assertEqual(resp.status_code, 200, "No access to the page")
        self.assertTrue("is_paginated" in resp.context)
        self.assertTrue(resp.context["is_paginated"] == True)
        self.assertTrue(len(resp.context["products"]) == 4)


class ListResponseListViewTest(DataTestList):
    """
    Тесты для представления ListResponseListView
    """

    def test_view_url_accessible_by_name(self):
        """
        Тест доступа авторизованного пользователя
        """
        login = self.client.login(email="company@company.com", password="qwerty")
        resp = self.client.get(reverse("cabinet:responses_active"))
        self.assertEqual(str(resp.context["user"]), "Компания")
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get(
            reverse("cabinet:responses_completed", args=["completed"])
        )
        self.assertEqual(str(resp.context["user"]), "Компания")
        self.assertEqual(resp.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        """
        Тест редиректа если пользователь не авторизован
        """
        resp = self.client.get(reverse("cabinet:responses_active"))
        self.assertRedirects(
            resp,
            "/account/login/?next=/cabinet/responses/",
            msg_prefix="When an unauthorized user gets access, he does not redirect to the authorization page",
        )
        resp = self.client.get(
            reverse("cabinet:responses_completed", args=["completed"])
        )
        self.assertRedirects(
            resp,
            "/account/login/?next=/cabinet/responses/completed/",
            msg_prefix="When an unauthorized user gets access, he does not redirect to the authorization page",
        )

    def test_logged_in_uses_correct_template(self):
        """
        Тест ответа на запрос и использования правильного шаблона для авторизации пользователя
        """
        login = self.client.login(email="company@company.com", password="qwerty")
        resp = self.client.get(reverse("cabinet:responses_active"))
        self.assertEqual(str(resp.context["user"]), "Компания")
        self.assertEqual(resp.status_code, 200, "No access to the page")
        self.assertTemplateUsed(
            resp, "cabinet/responses_to_company.html", "The incorrect template is used"
        )
        resp = self.client.get(
            reverse("cabinet:responses_completed", args=["completed"])
        )
        self.assertEqual(str(resp.context["user"]), "Компания")
        self.assertEqual(resp.status_code, 200, "No access to the page")
        self.assertTemplateUsed(
            resp, "cabinet/responses_to_company.html", "The incorrect template is used"
        )

    def test_only_test_company_responses_active_in_list(self):
        """
        Тест проверки получаемого списка активных откликов, что они принадлежат компании test_company
        """
        login = self.client.login(email="company@company.com", password="qwerty")
        resp = self.client.get(reverse("cabinet:responses_active"))
        self.assertEqual(str(resp.context["user"]), "Компания")
        self.assertEqual(resp.status_code, 200, "No access to the page")
        self.assertTrue(
            "responses" in resp.context, "The context does not contain product"
        )

        for response in resp.context["responses"]:
            self.assertEqual(
                resp.context["user"],
                response.product.company,
                "The context contains products that did not belong to the test_company",
            )

    def test_only_test_company_responses_completed_in_list(self):
        """
        Тест проверки получаемого списка обработанных откликов, что они принадлежат компании test_company
        """
        response_active = Response.objects.all()
        for response in response_active:
            response.finished = True
            response.save()
        login = self.client.login(email="company@company.com", password="qwerty")
        resp = self.client.get(
            reverse("cabinet:responses_completed", args=["completed"])
        )
        self.assertEqual(str(resp.context["user"]), "Компания")
        self.assertEqual(resp.status_code, 200, "No access to the page")
        self.assertTrue(
            "responses" in resp.context, "The context does not contain product"
        )
        for response in resp.context["responses"]:
            self.assertEqual(
                resp.context["user"],
                response.product.company,
                "The context contains products that did not belong to the test_company",
            )

    def test_pagination_first_page(self):
        """
        Тест проверки количества активных откликов на первой странице
        """
        login = self.client.login(email="company@company.com", password="qwerty")
        resp = self.client.get(reverse("cabinet:responses_active"))
        self.assertEqual(str(resp.context["user"]), "Компания")
        self.assertEqual(resp.status_code, 200, "No access to the page")
        self.assertTrue("is_paginated" in resp.context)
        self.assertTrue(resp.context["is_paginated"] == True)
        self.assertTrue(len(resp.context["responses"]) == 5)

    def test_pagination_second_page(self):
        """
        Тест проверки количества активных откликов на второй странице
        """
        login = self.client.login(email="company@company.com", password="qwerty")
        resp = self.client.get(reverse("cabinet:responses_active") + "?page=2")
        self.assertEqual(str(resp.context["user"]), "Компания")
        self.assertEqual(resp.status_code, 200, "No access to the page")
        self.assertTrue("is_paginated" in resp.context)
        self.assertTrue(resp.context["is_paginated"] == True)
        self.assertEqual(len(resp.context["responses"]), 4)

    def test_pagination_first_page_completed_responses(self):
        """
        Тест проверки количества активных откликов на первой странице
        """
        login = self.client.login(email="company@company.com", password="qwerty")
        resp = self.client.get(reverse("cabinet:responses_active"))
        self.assertEqual(str(resp.context["user"]), "Компания")
        self.assertEqual(resp.status_code, 200, "No access to the page")
        self.assertTrue("is_paginated" in resp.context)
        self.assertTrue(resp.context["is_paginated"] == True)
        self.assertEqual(len(resp.context["responses"]), 5)

    def test_pagination_second_page_completed_responses(self):
        """
        Тест проверки количества активных откликов на второй странице
        """
        response_active = Response.objects.filter(
            product__company__email="company@company.com"
        )
        for response in response_active:
            response.finished = True
            response.save()
        login = self.client.login(email="company@company.com", password="qwerty")
        resp = self.client.get(
            reverse("cabinet:responses_completed", args=["completed"]) + "?page=2"
        )
        self.assertEqual(str(resp.context["user"]), "Компания")
        self.assertEqual(resp.status_code, 200, "No access to the page")
        self.assertTrue("is_paginated" in resp.context)
        self.assertTrue(resp.context["is_paginated"] == True)
        self.assertEqual(len(resp.context["responses"]), 4)


class ResponseActionTest(DataTestList):
    """
    Тесты для представления ResponseAction
    """

    def test_redirect_if_not_logged_in(self):
        """
        Тест редиректа если пользователь не авторизован
        """
        resp = self.client.get(reverse("cabinet:response_finished", args=["1"]))
        self.assertRedirects(
            resp,
            "/account/login/?next=/cabinet/responses/action/1/",
            msg_prefix="When an unauthorized user gets access, he does not redirect to the authorization page",
        )
        resp = self.client.get(reverse("cabinet:response_delete", args=["1", "delete"]))
        self.assertRedirects(
            resp,
            "/account/login/?next=/cabinet/responses/action/1/delete/",
            msg_prefix="When an unauthorized user gets access, he does not redirect to the authorization page",
        )

    def test_view_url_accessible(self):
        """
        Тест доступа авторизованного пользователя к отклику который принадлежит ему
        """
        login = self.client.login(email="company@company.com", password="qwerty")
        self.assertTrue(login)
        # изменение статуса отклика на "обработан"
        resp = self.client.get(reverse("cabinet:responses_active"))
        company = resp.context["user"]
        r_not_fin = Response.objects.filter(
            product__company__email=company.email, finished=False
        )[:1]
        for response in r_not_fin:
            response_id = response.id
        resp = self.client.get(reverse("cabinet:response_finished", args=[response_id]))
        self.assertRedirects(resp, reverse("cabinet:responses_active"))
        # удаление отклика со статусом "обработан"
        resp = self.client.get(
            reverse("cabinet:response_delete", args=[response_id, "delete"])
        )
        responses = Response.objects.filter(id=response_id)
        for response in responses:
            self.assertIsNone(response)
        self.assertRedirects(
            resp, reverse("cabinet:responses_completed", args=["completed"])
        )
        # удаление отклика со статусом "не обработан"
        r_not_fin = Response.objects.filter(
            product__company__email=company.email, finished=False
        )[:1]
        for response in r_not_fin:
            response_id = response.id
        resp = self.client.get(
            reverse("cabinet:response_delete", args=[response_id, "delete"])
        )
        responses = Response.objects.filter(id=response_id)
        for response in responses:
            self.assertIsNotNone(response)
        self.assertRedirects(resp, reverse("cabinet:responses_list"))
        resp = self.client.get(reverse("cabinet:responses_list"))
        for message in resp.context["messages"]:
            self.assertEqual(message, "Нельзя удалить необработанный отклик")

    def test_view_url_accessible_response_not_belong(self):
        """
        Тест доступа авторизованного пользователя к отклику который не принадлежит ему
        """
        login = self.client.login(email="company1@company.com", password="qwerty")
        self.assertTrue(login)
        # попытка изменение статуса отклика на "обработан"
        resp = self.client.get(reverse("cabinet:response_finished", args=["1"]))
        self.assertEqual(resp.status_code, 404)
        responses = Response.objects.filter(id="1")
        for response in responses:
            self.assertFalse(response.finished)
        # попытка удаления отклика со статусом "обработан"
        Response.objects.filter(id="1").update(finished=True)
        resp = self.client.get(reverse("cabinet:response_delete", args=["1", "delete"]))
        responses = Response.objects.filter(id="1")
        for response in responses:
            self.assertIsNotNone(response)
        self.assertEqual(resp.status_code, 404)
        # self.assertRedirects(resp, reverse("cabinet:responses_list"))
        # попытка удаления отклика со статусом "не обработан"
        resp = self.client.get(reverse("cabinet:response_delete", args=["2", "delete"]))
        responses = Response.objects.filter(id="2")
        for response in responses:
            self.assertIsNotNone(response)
        self.assertEqual(resp.status_code, 404)
        # self.assertRedirects(resp, reverse("cabinet:responses_list"))


class ProductDeleteViewTest(DataTestList):
    """
    Тесты для представления ProductDeleteView
    """

    def test_redirect_if_not_logged_in(self):
        """
        Тест редиректа если пользователь не авторизован
        """
        resp = self.client.get(reverse("cabinet:delete_product", args=["1"]))
        self.assertRedirects(
            resp,
            "/account/login/?next=/cabinet/product/delete/1/",
            msg_prefix="When an unauthorized user gets access, he does not redirect to the authorization page",
        )

    def test_view_url_accessible(self):
        """
        Тест удаления продукта который принадлежит авторизованному пользователю
        """
        login = self.client.login(email="company@company.com", password="qwerty")
        self.assertTrue(login)
        resp = self.client.get(reverse("cabinet:list_product"))
        company = resp.context["user"]
        p_not_fin = Product.objects.filter(company__email=company.email)[:1]
        for product in p_not_fin:
            product_id = product.id
        resp = self.client.get(reverse("cabinet:delete_product", args=[product_id]))
        products = Product.objects.filter(id=product_id)
        for product in products:
            self.assertIsNone(product)
        self.assertRedirects(resp, reverse("cabinet:list_product"))

    def test_view_url_accessible_product_not_belong(self):
        """
        Тест удаления продукта который не принадлежит авторизованному пользователю
        """
        login = self.client.login(email="company1@company.com", password="qwerty")
        self.assertTrue(login)
        resp = self.client.get(reverse("cabinet:list_product"))
        resp = self.client.get(reverse("cabinet:delete_product", args=["1"]))
        products = Product.objects.filter(id="1")
        for product in products:
            self.assertIsNotNone(product)
        self.assertEqual(resp.status_code, 404)


class MainResponseListViewTest(DataTestList):
    """
    Тесты для представления CreateProductView
    """

    def test_view_url_accessible_by_name(self):
        """
        Тест проверки url
        """
        resp = self.client.get(reverse("cabinet:responses_list"))
        self.assertEqual(resp.status_code, 200)

    def test_context(self):
        """
        Тест контекста передаваемого на страницу
        """
        resp = self.client.get(reverse("cabinet:responses_list"))
        self.assertEqual(resp.status_code, 200)
        categories = resp.context["categories"]
        for category in categories:
            self.assertEqual(category.name, "Недвижимость")
        self.assertTrue(resp.context["is_paginated"])

    def test_uses_correct_template(self):
        """
        Тест использования правильного шаблона
        """
        resp = self.client.get(reverse("cabinet:responses_list"))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "cabinet/responses_to_product.html")

    def test_view_url_accessible_by_name_in_category(self):
        """
        Тест проверки url при отображении по категориям
        """
        resp = self.client.get(
            reverse("cabinet:responses_list_category", args=["nedvizhimost"])
        )
        self.assertEqual(resp.status_code, 200)

    def test_uses_correct_template_in_category(self):
        """
        Тест использования правильного шаблона при отображении по категориям
        """
        resp = self.client.get(
            reverse("cabinet:responses_list_category", args=["nedvizhimost"])
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "cabinet/responses_to_product.html")

    def test_context_in_category(self):
        """
        Тест контекста передаваемого на страницу при отображении по категориям
        """
        resp = self.client.get(
            reverse("cabinet:responses_list_category", args=["nedvizhimost"])
        )
        self.assertEqual(resp.status_code, 200)
        category = get_object_or_404(Category, slug="nedvizhimost")
        self.assertEqual(resp.context["form_filter"].initial, {"category": category})
        self.assertEqual(resp.context["category"], category)

    def test_pagination_first_page(self):
        """
        Тест проверки количества элементов на первой странице
        """
        resp = self.client.get(reverse("cabinet:responses_list"))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue("is_paginated" in resp.context)
        self.assertTrue(resp.context["is_paginated"] == True)
        self.assertTrue(len(resp.context["products"]) == 5)

    def test_pagination_first_page_in_category(self):
        """
        Тест проверки количества элементов на первой странице при отображении по категориям
        """
        resp = self.client.get(
            reverse("cabinet:responses_list_category", args=["nedvizhimost"])
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue("is_paginated" in resp.context)
        self.assertTrue(resp.context["is_paginated"] == True)
        self.assertTrue(len(resp.context["products"]) == 5)

    def test_pagination_last_page(self):
        """
        Тест проверки количества элементов на крайней странице
        """
        resp = self.client.get(reverse("cabinet:responses_list") + "?page=4")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue("is_paginated" in resp.context)
        self.assertTrue(resp.context["is_paginated"] == True)
        self.assertTrue(len(resp.context["products"]) == 3)

    def test_pagination_last_page_in_category(self):
        """
        Тест проверки количества элементов на крайней странице при отображении по категориям
        """
        resp = self.client.get(
            reverse("cabinet:responses_list_category", args=["nedvizhimost"])
            + "?page=4"
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue("is_paginated" in resp.context)
        self.assertTrue(resp.context["is_paginated"] == True)
        self.assertTrue(len(resp.context["products"]) == 3)


class PageResponseViewTest(DataTestList):
    """
    Тесты для представления PageResponseView
    """
    def get_id_product(self):
        product = [prod.id for prod in self.products][:1]
        return product

    def test_view_url_accessible_by_name(self):

        """
        Тест проверки url
        """
        resp = self.client.get(reverse("cabinet:page_response_form", args=self.get_id_product()))
        self.assertEqual(resp.status_code, 200)

    def test_uses_correct_template(self):
        """
        Тест использования правильного шаблона
        """
        resp = self.client.get(reverse("cabinet:page_response_form", args=self.get_id_product()))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "cabinet/response_page.html")

    def test_context(self):
        """
        Тест контекста передаваемого на страницу
        """
        resp = self.client.get(reverse("cabinet:page_response_form", args=self.get_id_product()))
        self.assertEqual(resp.status_code, 200)
        product = get_object_or_404(
            Product, id=resp.resolver_match.kwargs.get("product_id")
        )
        self.assertEqual(resp.context["product"], product)
        self.assertIsInstance(resp.context["response_form"], ResponseForm)

    def test_redirect_create_on_success_post(self):
        """
        Тест пост запроса, при валидной форме
        """
        data = {
            "first_name": "name",
            "last_name": "lastname",
            "phone": "123456789",
            "email": "test@test.com",
        }
        resp = self.client.post(
            reverse("cabinet:page_response_form", args=self.get_id_product()), data=data
        )
        self.assertRedirects(resp, reverse("cabinet:responses_list"))

    def test_form_invalid_phone_field_num_seven(self):
        """
        Тест текста ошибки, при невалидном поле телефон (7 цифр)
        """
        data = {
            "first_name": "name",
            "last_name": "lastname",
            "phone": "1234567",
            "email": "test@test.com",
        }
        resp = self.client.post(
            reverse("cabinet:page_response_form", args=self.get_id_product()), data=data
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "cabinet/response_page.html")
        self.assertFormError(
            resp,
            "response_form",
            "phone",
            "Номер телефона должен быть от 8 до 16 цифр",
        )

    def test_form_invalid_phone_field_num_seventeen(self):
        """
        Тест текста ошибки, при невалидном поле телефон (17 цифр)
        """
        data = {
            "first_name": "name",
            "last_name": "lastname",
            "phone": "12345678998765432",
            "email": "test@test.com",
        }
        resp = self.client.post(
            reverse("cabinet:page_response_form", args=self.get_id_product()), data=data
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "cabinet/response_page.html")
        self.assertFormError(
            resp,
            "response_form",
            "phone",
            "Убедитесь, что это значение содержит не более 16 символов (сейчас 17).",
        )

    def test_form_invalid_phone_field_alpha(self):
        """
        Тест текста ошибки, при невалидном поле телефон (содержит буквы)
        """
        data = {
            "first_name": "name",
            "last_name": "lastname",
            "phone": "123456789g",
            "email": "test@test.com",
        }
        resp = self.client.post(
            reverse("cabinet:page_response_form", args=self.get_id_product()), data=data
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "cabinet/response_page.html")
        self.assertFormError(
            resp,
            "response_form",
            "phone",
            "Номер должен состоять из цифр",
        )

    def test_message_create_on_success_post(self):
        """
        Тест текста сообщения при удачной отправки формы
        """
        data = {
            "first_name": "name",
            "last_name": "lastname",
            "phone": "123456789",
            "email": "test@test.com",
        }
        resp = self.client.post(
            reverse("cabinet:page_response_form", args=self.get_id_product()), data=data
        )
        self.assertRedirects(resp, reverse("cabinet:responses_list"))
        resp = self.client.get(reverse("cabinet:responses_list"))
        for message in resp.context["messages"]:
            self.assertEqual(
                message, "Ваша заявка отправлена. С вами свяжется менеджер компании"
            )


class FilterProductViewTest(DataTestList):
    """
    Тесты для представления FilterProductView
    """

    def test_view_url_accessible_by_name(self):
        """
        Тест проверки url
        """
        resp = self.client.get(reverse("cabinet:filter_product"))
        self.assertEqual(resp.status_code, 200)

    def test_uses_correct_template_form_valid(self):
        """
        Тест использования правильного шаблона при валидной форме
        """
        params = "?company=&category=&name=&min_price=0&max_price=9999999999&" \
                 "min_interest_rate=0&max_interest_rate=100&period="
        resp = self.client.get(reverse("cabinet:filter_product") + params)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "cabinet/responses_to_product.html")
        self.assertEqual(resp.context["products_count"], 18)

    def test_uses_correct_template_form_invalid(self):
        """
        Тест использования правильного шаблона при не валидной форме
        """
        params = "?company=&category=&name=&min_price=0&max_price=9999999999&" \
                 "min_interest_rate=150&max_interest_rate=100&period="
        resp = self.client.get(reverse("cabinet:filter_product") + params)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "cabinet/responses_to_product.html")
        self.assertEqual(resp.context["products_count"], 0)

    def test_uses_correct_template_form_valid_check_elastic(self):
        """
        Тест использования правильного шаблона при валидной форме при поиске через elastic
        """
        params = "?company=&category=&name=&min_price=0&max_price=9999999999&" \
                 "min_interest_rate=0&max_interest_rate=100&period=&check_elastic=on"
        resp = self.client.get(reverse("cabinet:filter_product") + params)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "cabinet/responses_to_product.html")

    def test_uses_correct_template_form_invalid_check_elastic(self):
        """
        Тест использования правильного шаблона при не валидной форме при поиске через elastic
        """
        params = "?company=&category=&name=&min_price=0&max_price=9999999999&" \
                 "min_interest_rate=1500&max_interest_rate=100&period=&check_elastic=on"
        resp = self.client.get(reverse("cabinet:filter_product") + params)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "cabinet/responses_to_product.html")

    def test_context(self):
        """
        Тест контекста передаваемого на страницу
        """
        category = self.test_category.id
        params = f"?company=&category={category}&name=&min_price=0&max_price=9999999999&" \
                 "min_interest_rate=0&max_interest_rate=100&period="
        resp = self.client.get(reverse("cabinet:filter_product") + params)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["category"], self.test_category)
        self.assertIsInstance(resp.context["products"], List)
        self.assertIsInstance(resp.context["form_filter"], FilterProductForm)
        self.assertEqual(resp.context["products_count"], len(resp.context["products"]))
        self.assertQuerysetEqual(resp.context["categories"], Category.objects.all())

    def test_form_invalid_max_price(self):
        """
        Тест текста ошибки, при невалидном поле цена
        """
        params = "?company=&category=&name=&min_price=999&max_price=99&" \
                 "min_interest_rate=0&max_interest_rate=100&period="
        resp = self.client.get(reverse("cabinet:filter_product") + params)
        self.assertTemplateUsed(resp, "cabinet/responses_to_product.html")
        self.assertFormError(
            resp,
            "form_filter",
            "max_price",
            "Значение мин цены не должно быть больше макс цены",
        )

    def test_form_invalid_max_interest_rate(self):
        """
        Тест текста ошибки, при невалидном поле процентная ставка
        """
        params = "?company=&category=&name=&min_price=999&max_price=999999&" \
                 "min_interest_rate=110&max_interest_rate=100&period="
        resp = self.client.get(reverse("cabinet:filter_product") + params)
        self.assertTemplateUsed(resp, "cabinet/responses_to_product.html")
        self.assertFormError(
            resp,
            "form_filter",
            "max_interest_rate",
            "Значение мин процентной ставки не должно быть больше макс процентной ставки",
        )





