# Generated by Django 4.2.4 on 2023-11-05 07:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_alter_user_age"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="point",
            field=models.PositiveIntegerField(default=20),
        ),
    ]