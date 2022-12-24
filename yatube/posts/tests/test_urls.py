from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from ..models import Group, Post

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="auth")
        cls.group = Group.objects.create(
            title="Тестовая группа",
            slug="test_slug",
            description="Тестовое описание",
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text="Тестовый пост",
            group=cls.group,
        )

    def setUp(self):
        """Создаем тестовых пользователей."""
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(PostURLTests.user)

    def test_url_exists_for_guest(self):
        """Проверка доступности для неавторизованного пользователя"""
        url_response_html_status = {
            "/": HTTPStatus.OK,
            "/create/": HTTPStatus.FOUND,
            f"/posts/{self.post.pk}/": HTTPStatus.FOUND,
            f"/group/{self.group.slug}/": HTTPStatus.OK,
            f"/posts/{self.post.id}/": HTTPStatus.OK,
            f"/profile/{self.user.username}/": HTTPStatus.OK,
        }
        for url, html_status in url_response_html_status.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, html_status)

    def test_correct_templates(self):
        """URL-адрес вызывает корректный шаюблон HTML"""
        url_path_templates = {
            "/": "posts/index.html",
            "/create/": "posts/create_post.html",
            f"/group/{self.group.slug}/": "posts/group_list.html",
            f"/posts/{self.post.id}/": "posts/post_detail.html",
            f"/posts/{self.post.pk}/edit/": "posts/create_post.html",
            f"/profile/{self.user}/": "posts/profile.html",
        }
        for url, template in url_path_templates.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_not_found_page(self):
        """Проверка несуществующей страницы."""
        response = self.guest_client.get("/not_found_page/")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
