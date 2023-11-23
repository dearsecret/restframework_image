# Generated by Django 4.2.4 on 2023-11-15 07:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0006_user_friend"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="avatar",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="bio",
        ),
        migrations.AddField(
            model_name="profile",
            name="drink",
            field=models.IntegerField(
                choices=[(0, "안"), (1, "아주 가끔 "), (2, "가끔 "), (3, "자주 ")], null=True
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="drive",
            field=models.IntegerField(
                choices=[(0, "면허 없음"), (1, "면허 있음"), (2, "차량 보유")], null=True
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="height",
            field=models.IntegerField(
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(145),
                    django.core.validators.MaxValueValidator(210),
                ],
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="job",
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="policy",
            field=models.IntegerField(
                choices=[(0, "무관심"), (-1, "진보"), (1, "보수")], null=True
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="religion",
            field=models.CharField(
                choices=[
                    ("none", "무관심"),
                    ("buddhism", "불교"),
                    ("catholicism", "천주교"),
                    ("christian", "기독교"),
                    ("etc", "기타"),
                ],
                max_length=12,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="school",
            field=models.IntegerField(
                choices=[(0, "고등학교 졸업"), (1, "전문대 졸업"), (2, "대학교 졸업"), (3, "대학원 졸업")],
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="smoke",
            field=models.IntegerField(
                choices=[(0, "-"), (1, "금연"), (2, "전자담배"), (3, "담배")], null=True
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="weight",
            field=models.IntegerField(choices=[(0, "")], null=True),
        ),
    ]