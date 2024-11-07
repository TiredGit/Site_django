# Generated by Django 5.1.2 on 2024-11-05 03:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_app', '0003_alter_category_options_alter_master_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='records', to='site_app.category', verbose_name='Категория'),
        ),
    ]