from django import forms
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from posts.forms import PostForm

from ..models import Follow, Group, Post, User

ALL_TESTS_COUNT = settings.COUNT_POSTS_ON_PAGE * 2 - 1
TEST_COUNT_SECOND_PAGE = ALL_TESTS_COUNT - settings.COUNT_POSTS_ON_PAGE


class PostViewsTests(TestCase):
    """Создаем тестовую Базу Данных."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="auth")
        cls.user_1 = User.objects.create_user(username="auth_1")
        cls.group = Group.objects.create(
            title="Тестовая группа",
            slug="test_slug",
            description="Тестовое описание",
        )
        cls.small_gif = (
            b"\x47\x49\x46\x38\x39\x61\x02\x00"
            b"\x01\x00\x80\x00\x00\x00\x00\x00"
            b"\xFF\xFF\xFF\x21\xF9\x04\x00\x00"
            b"\x00\x00\x00\x2C\x00\x00\x00\x00"
            b"\x02\x00\x01\x00\x00\x02\x02\x0C"
            b"\x0A\x00\x3B"
        )
        cls.upload = SimpleUploadedFile(
            name="small.gif",
            content=cls.small_gif,
            content_type="image/gif",
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text="Тестовый пост",
            group=cls.group,
            image=cls.upload,
        )

    def setUp(self):
        """Создаем гостя и авторизованного клиента"""
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(PostViewsTests.user)
        self.new_author = User.objects.create_user(username="new_author")

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            "/": "posts/index.html",
            "/create/": "posts/create_post.html",
            f"/group/{self.group.slug}/": "posts/group_list.html",
            f"/posts/{self.post.id}/": "posts/post_detail.html",
            f"/posts/{self.post.pk}/edit/": "posts/create_post.html",
            f"/profile/{self.user}/": "posts/profile.html",
        }
        for path, name in templates_pages_names.items():
            with self.subTest(name=name):
                response = self.authorized_client.get(path)
                error_name = f"Ошибка: по {path} ожидался шаблон {name}"
                self.assertTemplateUsed(response, name, error_name)

    def test_page_index_uses_correct_context(self):
        """Корректность словаря в шаблоне index"""
        response = self.authorized_client.get(reverse("posts:index"))
        test_object_post = response.context["page_obj"][0]
        self.assertEqual(test_object_post.author.username, "auth")
        self.assertEqual(test_object_post.text, "Тестовый пост")
        self.assertEqual(test_object_post.group, self.group)
        self.assertEqual(test_object_post.image, self.post.image)

    def test_page_group_list_uses_correct_context(self):
        """Корректность словаря в шаблоне group_list"""
        response = self.authorized_client.get(
            reverse("posts:group_list", kwargs={"slug": self.group.slug})
        )
        test_object_post = response.context["page_obj"][0]
        self.assertEqual(test_object_post.author.username, "auth")
        self.assertEqual(test_object_post.text, "Тестовый пост")
        self.assertEqual(test_object_post.group, self.group)
        self.assertEqual(test_object_post.image, self.post.image)

    def test_page_profile_uses_correct_context(self):
        """Корректность словаря в шаблоне profile"""
        response = self.authorized_client.get(
            reverse("posts:profile", kwargs={"username": "auth"})
        )
        test_object_post = response.context["page_obj"][0]
        self.assertEqual(test_object_post.author.username, "auth")
        self.assertEqual(test_object_post.text, "Тестовый пост")
        self.assertEqual(test_object_post.group, self.group)
        self.assertEqual(test_object_post.image, self.post.image)

    def test_page_post_detail_uses_correct_context(self):
        """Корректность словаря в шаблоне post_detail"""
        response = self.authorized_client.get(
            reverse("posts:post_detail", kwargs={"post_id": self.post.id}),
        )
        post_1 = {
            response.context["post"].text: "Тестовый пост",
            response.context["post"].author: self.user,
            response.context["post"].group: self.group,
            response.context["post"].image: self.post.image,
        }
        for value, expected in post_1.items():
            self.assertEqual(post_1[value], expected)

    def test_form_is_instanse_context_on_page_create_post(self):
        """Проверка контекста по форме на странице сreate_post"""
        response = self.authorized_client.get(reverse("posts:create_post"))
        form = response.context["form"]
        self.assertIsInstance(form, PostForm)

    def test_page_create_post_uses_correct_context(self):
        """Корректность словаря в шаблоне create_post"""
        response = self.authorized_client.get(reverse("posts:create_post"))
        form_fields = {
            "text": forms.fields.CharField,
            "group": forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get("form").fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_form_is_instanse_context_on_page_post_edit(self):
        """Проверка контекста по форме на странице post_edit"""
        response = self.authorized_client.get(
            reverse("posts:post_edit", kwargs={"post_id": self.post.id})
        )
        form = response.context["form"]
        self.assertIsInstance(form, PostForm)

    def test_page_create_post_uses_correct_context_edit(self):
        """Корректность словаря в шаблоне create_post при редактировании"""
        response = self.authorized_client.get(
            reverse("posts:post_edit", kwargs={"post_id": self.post.id})
        )
        form_fields = {
            "text": forms.fields.CharField,
            "group": forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get("form").fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_exists_on_index_group_list_profile(self):
        """При создании и заполнении группы текст добавлен корректно"""
        response_index = self.authorized_client.get(reverse("posts:index"))
        response_group = self.authorized_client.get(
            reverse("posts:group_list", kwargs={"slug": self.group.slug})
        )
        response_profile = self.authorized_client.get(
            reverse("posts:profile", kwargs={"username": "auth"})
        )
        index = response_index.context["page_obj"]
        group = response_group.context["page_obj"]
        profile = response_profile.context["page_obj"]
        self.assertIn(self.post, index, "Пост на главную страницу не добавлен")
        self.assertIn(self.post, group, "На странице group_list поста нет")
        self.assertIn(
            self.post,
            profile,
            "На страницу пользователя пост не добавлен",
        )

    def test_post_not_in_another_groups(self):
        """Пост не добавляется в другую группу, к другому пользователю"""
        group_2 = Group.objects.create(
            title="Тестовая групаа_2",
            slug="test_group_2",
        )
        posts_count = Post.objects.filter(group=self.group).count()
        post = Post.objects.create(
            text="Тестовый пост_2",
            author=self.user_1,
            group=group_2,
        )
        response_profile = self.authorized_client.get(
            reverse("posts:profile", kwargs={"username": "auth"})
        )
        group = Post.objects.filter(group=self.group).count()
        profile = response_profile.context["page_obj"]
        self.assertEqual(group, posts_count, "Пост добавлен не в ту группу")
        self.assertNotIn(post, profile, "Пост в группе другого пользователя")

    def test_comments_only_for_authorized_guests(self):
        """Создавать комментарий неавторизованный пользователь не может"""
        form_data = {"text": "text"}
        response = self.guest_client.post(
            reverse("posts:add_comment", kwargs={"post_id": self.post.pk}),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response, f"/auth/login/?next=/posts/{self.post.pk}/comment/"
        )

    def test_show_new_comments_on_post_detail(self):
        """Комментарии появляются на странице детализации поста"""
        form_data = {
            "author": self.user,
            "text": "Тестируемый коммент",
            "post": self.post,
        }
        self.authorized_client.post(
            reverse("posts:add_comment", kwargs={"post_id": self.post.pk}),
            data=form_data,
        )
        response = self.guest_client.get(
            reverse("posts:post_detail", kwargs={"post_id": self.post.pk})
        )
        comment = response.context["comments"][0]
        self.assertEqual(comment.text, "Тестируемый коммент")

    def test_index_page_cache(self):
        """Тест кеширования главной страницы"""
        response = self.authorized_client.get(reverse("posts:index"))
        posts_1 = response.content
        Post.objects.create(author=self.user, text="Тест кеширования")
        self.assertTrue(Post.objects.filter(text="Тест кеширования").exists())
        response = self.authorized_client.get(reverse("posts:index"))
        posts_2 = response.content
        self.assertEqual(posts_2, posts_1)

    def test_correct_following_authors(self):
        """Добавление и удаление подписки"""
        Post.objects.create(
            author=self.new_author,
            text="Новый пост",
        )
        Follow.objects.create(user=self.user, author=self.new_author)
        response = self.authorized_client.get(reverse("posts:follow_index"))
        page_object = response.context["page_obj"]
        first_post = page_object[0]
        self.assertEqual(first_post.text, "Новый пост")
        Follow.objects.get(user=self.user, author=self.new_author).delete()
        response = self.authorized_client.get(reverse("posts:follow_index"))
        page_object = response.context["page_obj"]
        self.assertFalse(page_object)

    def test_correct_content_following_users(self):
        """Появление записи только в подписке пользователя"""
        new_author_2 = User.objects.create_user(username="new_author_2")
        new_user = User.objects.create_user(username="new_user")
        new_user_client = Client()
        new_user_client.force_login(new_user)
        Post.objects.create(
            author=self.new_author,
            text="Новый пост",
        )
        Post.objects.create(author=new_author_2, text="Новый Пост2")
        obj = [
            Follow(user=self.user, author=self.new_author),
            Follow(user=self.user, author=new_author_2),
            Follow(user=new_user, author=self.new_author),
        ]
        Follow.objects.bulk_create(obj)
        response_first = self.authorized_client.get(
            reverse("posts:follow_index")
        )
        count_for_first_user = len(response_first.context["page_obj"])
        response_second = new_user_client.get(
            reverse("posts:follow_index")
        )
        count_for_second_user = len(response_second.context["page_obj"])
        self.assertNotEqual(count_for_first_user, count_for_second_user)


class PaginatorViewsTest(TestCase):
    """Создание класса Paginator - проверка корректности отображения постов"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.author = User.objects.create_user(username="auth")
        cls.authorized_client = Client()
        cls.authorized_client.force_login(PaginatorViewsTest.author)
        cls.group = Group.objects.create(
            title="test_title",
            slug="test_slug",
            description="test_description",
        )

    def test_paginator_count_posts(self):
        """Проверка Paginator на 1 и 2 страницах"""
        test_post = [
            Post(
                author=self.author,
                text=f"Тестовый текст номер {post}",
                group=self.group,
            )
            for post in range(ALL_TESTS_COUNT)
        ]
        Post.objects.bulk_create(test_post)
        reverse_values = (
            ("posts:index", None),
            ("posts:group_list", (self.group.slug,)),
            ("posts:profile", (self.author.username,)),
        )
        object_list = (
            ("?page=1", settings.COUNT_POSTS_ON_PAGE),
            ("?page=2", TEST_COUNT_SECOND_PAGE),
        )
        for reverse_value, args in reverse_values:
            with self.subTest():
                for page, number in object_list:
                    with self.subTest():
                        reverse_name = reverse(reverse_value, args=args)
                        response = self.authorized_client.get(
                            reverse_name + page
                        )
                        self.assertEqual(len(
                            response.context["page_obj"]),
                            number,
                        )
