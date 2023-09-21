# Generated by Django 4.2.4 on 2023-09-21 09:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("images", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="userimage",
            name="index",
            field=models.IntegerField(
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(5),
                ],
            ),
        ),
    ]