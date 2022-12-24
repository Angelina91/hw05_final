from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    text = models.TextField(
        verbose_name="Текст",
        help_text="Введите текст поста",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Автор",
        help_text="Выбрать автора из выпадающего списка",
    )
    group = models.ForeignKey(
        "Group",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="posts",
        verbose_name="Группа",
        help_text="Выбрать группу из выпадающего списка",
    )
    image = models.ImageField(
        verbose_name="Картинка",
        upload_to="posts/",
        blank=True,
        help_text="Загрузить изображение",
    )

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        return self.text[:15]


class Group(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название группы")
    slug = models.SlugField(unique=True, verbose_name="URL-адрес")
    description = models.TextField(max_length=500, verbose_name="Описание")

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        "Post",
        related_name="comments",
        null=True,
        verbose_name="Комментарий",
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор комментария",
    )
    text = models.TextField(
        "Текст комментария",
        help_text="Текст нового комментария",
    )

    class Meta:
        ordering = ["-created"]
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text[:15]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="Подписчик",
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following", verbose_name="Автор"
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации",
    )

    class Meta:
        ordering = ["-pub_date"]
        verbose_name = "Подписаться на автора"
        verbose_name_plural = "Подписки"
        models.UniqueConstraint(fields=["user", "author"], name="following")

    def __str__(self):
        return f"Подписка {self.user} на {self.author}"
