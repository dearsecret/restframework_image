# Generated by Django 4.2.4 on 2023-11-15 16:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0007_remove_profile_avatar_remove_profile_bio_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="profiles",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]