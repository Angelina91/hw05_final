from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

User = get_user_model()


class StaticPagesURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="auth")

    def setUp(self):
        # Создаем неавторизованый клиент
        self.guest_client = Client()

    def test_url_exists_for_guest(self):
        """Проверка доступности для пользователя"""
        url_response_html_status = {
            "/about/author/": HTTPStatus.OK,
            "/about/tech/": HTTPStatus.OK,
            "/about/cat/": HTTPStatus.OK,
        }
        for url, html_status in url_response_html_status.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, html_status)
