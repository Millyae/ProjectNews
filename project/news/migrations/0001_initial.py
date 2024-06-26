# Generated by Django 5.0.6 on 2024-05-11 18:53

import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=255, unique=True)),
                ('content', models.TextField(default='')),
                ('author', models.CharField(default='', max_length=40)),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('subscribers', models.ManyToManyField(blank=True, related_name='subscribed_to', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
