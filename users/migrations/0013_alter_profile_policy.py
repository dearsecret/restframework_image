# Generated by Django 4.2.4 on 2023-11-20 19:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0012_alter_profile_dating_alter_profile_deny_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="policy",
            field=models.IntegerField(
                choices=[(0, "무관심"), (1, "진보"), (2, "보수")], null=True
            ),
        ),
    ]
