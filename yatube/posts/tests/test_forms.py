from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post, User


class PostFormTests(TestCase):
    """Создаем тестовую Базу Данных."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="auth")
        cls.group = Group.objects.create(
            title="Тестовая группа",
            slug="test_slug",
            description="Тестовое описание",
        )

    def setUp(self):
        """Создаем авторизованного клиента"""
        self.authorized_client = Client()
        self.authorized_client.force_login(PostFormTests.user)

    def test_new_post_create(self):
        """Проверка занесения данных в БД при создании поста"""
        all_posts_count = Post.objects.count()
        posts_count_in_group = Post.objects.filter(
            group=self.group
        ).count()
        imagine_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        upload = SimpleUploadedFile(
            name="imagine.gif",
            content=imagine_gif,
            content_type="image/gif"
        )
        form_data = {
            "text": "Текст - тест",
            "author": self.user,
            "group": self.group.id,
            "image": upload
        }
        response = self.authorized_client.post(
            reverse("posts:create_post"),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            "posts:profile",
            kwargs={"username": self.user.username})
        )
        self.assertEqual(Post.objects.count(), all_posts_count + 1)
        self.assertEqual(
            Post.objects.filter(group=self.group).count(),
            posts_count_in_group + 1, self.group
        )
        self.assertTrue(
            Post.objects.filter(
                text="Текст - тест",
                author=self.user,
                group=self.group
            ).exists()
        )

    def test_edit_post(self):
        """Проверка сохранения изменного поста в БД с post_edit"""
        group_2 = Group.objects.create(
            title="Тестовая группа_2",
            slug="test_slug_2",
            description="Тестовое описание_2"
        )
        post = Post.objects.create(
            author=self.user,
            text="Тестовый пост",
            group=self.group,
        )
        url = reverse("posts:post_edit", kwargs={"post_id": post.id})
        self.response = self.authorized_client.post(url, {
            "text": "Обновленный пост",
            "group": group_2.id,
        },
        )
        post.refresh_from_db()
        self.assertEqual(post.text, "Обновленный пост")
        self.assertEqual(post.group.id, group_2.id)
