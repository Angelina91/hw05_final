# Generated by Django 2.2.9 on 2022-09-10 05:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0004_auto_20220910_0501"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="post",
            options={"ordering": ("pub_date",)},
        ),
    ]
