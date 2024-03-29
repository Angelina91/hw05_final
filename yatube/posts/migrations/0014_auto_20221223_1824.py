# Generated by Django 2.2.16 on 2022-12-23 18:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0013_follow"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="follow",
            options={
                "ordering": ["-pub_date"],
                "verbose_name": "Подписаться на автора",
                "verbose_name_plural": "Подписки",
            },
        ),
        migrations.AlterField(
            model_name="follow",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="following",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Автор",
            ),
        ),
    ]
