# Generated by Django 3.2.12 on 2022-03-20 10:23

from django.db import migrations, models
import django.utils.timezone
import security.input_validation
import security.otp
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.TextField(blank=True, max_length=100, null=True, unique=True, validators=[security.input_validation.validate_name])),
                ('first_name', models.TextField(blank=True, max_length=100, null=True, validators=[security.input_validation.validate_name])),
                ('last_name', models.TextField(blank=True, max_length=100, null=True, validators=[security.input_validation.validate_name])),
                ('email', models.EmailField(max_length=150, unique=True)),
                ('otp', models.TextField(blank=True, max_length=200, null=True, unique=True)),
                ('otp_expiration', models.DateTimeField(blank=True, default=security.otp.get_expiration, null=True)),
                ('notification_scope', models.TextField(choices=[('Disabled', 'Disabled'), ('Only my executions', 'Own Executions'), ('All executions', 'All Executions')], default='Only my executions', max_length=18)),
                ('email_notification', models.BooleanField(default=True)),
                ('telegram_notification', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', users.models.RekonoUserManager()),
            ],
        ),
    ]
