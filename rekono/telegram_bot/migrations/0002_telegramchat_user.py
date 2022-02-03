# Generated by Django 3.2.12 on 2022-02-03 20:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('telegram_bot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramchat',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='telegram_chat', to=settings.AUTH_USER_MODEL),
        ),
    ]
