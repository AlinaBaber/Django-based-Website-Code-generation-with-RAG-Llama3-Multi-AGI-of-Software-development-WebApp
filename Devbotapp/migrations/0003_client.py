# Generated by Django 5.0.6 on 2024-07-10 13:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Devbotapp', '0002_add_questions'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, null=True)),
                ('company_name', models.CharField(max_length=255, null=True)),
                ('designation', models.CharField(max_length=255, null=True)),
                ('contact_info', models.TextField(null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('phone_number', models.CharField(max_length=15, null=True)),
                ('address', models.TextField(null=True)),
                ('industry', models.CharField(blank=True, max_length=255, null=True)),
                ('website', models.URLField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('client_type', models.CharField(choices=[('Simple', 'Simple'), ('Professional', 'Professional'), ('Business', 'Business')], default='Simple', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
