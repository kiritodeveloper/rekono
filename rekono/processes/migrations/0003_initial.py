# Generated by Django 3.2.10 on 2022-01-07 11:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('processes', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='process',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_processes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='process',
            name='liked_by',
            field=models.ManyToManyField(related_name='liked_process', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='step',
            constraint=models.UniqueConstraint(fields=('process', 'tool', 'configuration'), name='unique step'),
        ),
    ]
