# Generated by Django 3.2.7 on 2021-10-03 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('executions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enumeration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('port', models.IntegerField()),
                ('port_status', models.IntegerField(choices=[(1, 'Open'), (2, 'Open Filtered'), (3, 'Filtered'), (4, 'Closed')])),
                ('protocol', models.IntegerField(choices=[(1, 'Udp'), (2, 'Tcp')])),
                ('service', models.TextField(max_length=50)),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('execution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='enumerations', to='executions.execution')),
            ],
        ),
        migrations.CreateModel(
            name='Technology',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=100)),
                ('version', models.TextField(blank=True, max_length=100, null=True)),
                ('reference', models.TextField(blank=True, max_length=250, null=True)),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('enumeration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='technologies', to='findings.enumeration')),
                ('execution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='technologies', to='executions.execution')),
            ],
        ),
        migrations.CreateModel(
            name='Vulnerability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
                ('severity', models.IntegerField(choices=[(1, 'Info'), (2, 'Low'), (3, 'Medium'), (4, 'High'), (5, 'Critical')], default=3)),
                ('cve', models.TextField(blank=True, max_length=20, null=True)),
                ('osvdb', models.TextField(blank=True, max_length=20, null=True)),
                ('reference', models.TextField(blank=True, max_length=250, null=True)),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('execution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vulnerabilities', to='executions.execution')),
                ('technology', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vulnerabilities', to='findings.technology')),
            ],
        ),
        migrations.CreateModel(
            name='OSINT',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField(max_length=250)),
                ('data_type', models.IntegerField(choices=[(1, 'Ip'), (2, 'Domain'), (3, 'Url'), (4, 'Mail'), (5, 'Link'), (6, 'Asn'), (7, 'User'), (8, 'Password')])),
                ('source', models.TextField(blank=True, max_length=50, null=True)),
                ('reference', models.TextField(blank=True, max_length=250, null=True)),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('execution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='osints', to='executions.execution')),
            ],
        ),
        migrations.CreateModel(
            name='HttpEndpoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('endpoint', models.TextField(max_length=500)),
                ('status', models.IntegerField(blank=True, null=True)),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('enumeration', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='http_endpoints', to='findings.enumeration')),
                ('execution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='http_endpoints', to='executions.execution')),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField(max_length=20)),
                ('os', models.TextField(blank=True, max_length=250, null=True)),
                ('os_type', models.IntegerField(blank=True, choices=[(1, 'Linux'), (2, 'Windows'), (3, 'Macos'), (4, 'Ios'), (5, 'Android'), (6, 'Solaris'), (7, 'Freebsd'), (8, 'Other')], null=True)),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('execution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hosts', to='executions.execution')),
            ],
        ),
        migrations.CreateModel(
            name='Exploit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('reference', models.TextField(max_length=250)),
                ('checked', models.BooleanField(default=False)),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('execution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exploits', to='executions.execution')),
                ('technology', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exploits', to='findings.technology')),
                ('vulnerability', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exploits', to='findings.vulnerability')),
            ],
        ),
        migrations.AddField(
            model_name='enumeration',
            name='host',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enumerations', to='findings.host'),
        ),
    ]
