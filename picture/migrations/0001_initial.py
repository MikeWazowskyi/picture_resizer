# Generated by Django 4.2.2 on 2023-06-23 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Picture",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("file", models.ImageField(default=None, upload_to="images/default/")),
                (
                    "resized_image",
                    models.ImageField(
                        blank=True, null=True, upload_to="images/resized/"
                    ),
                ),
                ("width", models.PositiveIntegerField()),
                ("height", models.PositiveIntegerField(blank=True, null=True)),
            ],
        ),
    ]