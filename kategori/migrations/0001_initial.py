# Generated by Django 5.0.6 on 2024-06-10 20:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Kategori',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_kategori', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2024, 6, 10, 20, 56, 10, 245480, tzinfo=datetime.timezone.utc))),
                ('language', models.CharField(max_length=255)),
                ('member_count', models.IntegerField()),
                ('subcategories', models.BooleanField(default=None, null=True)),
            ],
        ),
    ]
