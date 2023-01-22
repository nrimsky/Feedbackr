# Generated by Django 4.1.5 on 2023-01-22 11:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="QuestionSet",
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
                ("description", models.CharField(max_length=1000)),
                (
                    "creator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="YesNoQuestion",
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
                ("prompt", models.CharField(max_length=2000)),
                ("completion", models.CharField(max_length=2000)),
                ("yes_votes", models.IntegerField(default=0)),
                ("no_votes", models.IntegerField(default=0)),
                (
                    "question_set",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="getfeedback.questionset",
                    ),
                ),
            ],
        ),
    ]
