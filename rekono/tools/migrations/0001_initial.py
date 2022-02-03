# Generated by Django 3.2.12 on 2022-02-03 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Argument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=20)),
                ('argument', models.TextField(blank=True, default='', max_length=50)),
                ('required', models.BooleanField(default=False)),
                ('multiple', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=30)),
                ('arguments', models.TextField(blank=True, default='', max_length=250)),
                ('default', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Input',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filter', models.TextField(blank=True, max_length=250, null=True)),
                ('order', models.IntegerField(default=1)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Intensity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('argument', models.TextField(blank=True, default='', max_length=50)),
                ('value', models.IntegerField(choices=[(1, 'Sneaky'), (2, 'Low'), (3, 'Normal'), (4, 'Hard'), (5, 'Insane')], default=3)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Output',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=30, unique=True)),
                ('command', models.TextField(blank=True, max_length=30, null=True)),
                ('output_format', models.TextField(blank=True, max_length=5, null=True)),
                ('defectdojo_scan_type', models.TextField(blank=True, max_length=50, null=True)),
                ('stage', models.IntegerField(choices=[(1, 'Osint'), (2, 'Enumeration'), (3, 'Vulnerabilities'), (4, 'Services'), (5, 'Exploitation')])),
                ('reference', models.TextField(blank=True, max_length=250, null=True)),
                ('icon', models.TextField(blank=True, max_length=250, null=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
