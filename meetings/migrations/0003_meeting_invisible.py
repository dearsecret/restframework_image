# Generated by Django 4.2.4 on 2023-11-02 04:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("meetings", "0002_meeting_descriptions"),
    ]

    operations = [
        migrations.AddField(
            model_name="meeting",
            name="invisible",
            field=models.BooleanField(default=False),
        ),
    ]