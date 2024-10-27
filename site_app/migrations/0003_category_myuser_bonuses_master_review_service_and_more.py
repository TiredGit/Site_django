# Generated by Django 5.1.2 on 2024-10-25 17:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_app', '0002_rename_user_myuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название категории')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание категории')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='category_picture', verbose_name='Изображение категории')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='myuser',
            name='bonuses',
            field=models.PositiveIntegerField(default=0, verbose_name='Бонусы'),
        ),
        migrations.CreateModel(
            name='Master',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя мастера')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание мастера')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='master_picture', verbose_name='Аватарка мастера')),
                ('category', models.ManyToManyField(related_name='masters', to='site_app.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Мастер',
                'verbose_name_plural': 'Мастеры',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Текст отзыва')),
                ('grade', models.PositiveIntegerField(choices=[(1, 'Очень плохо'), (2, 'Плохо'), (3, 'Средне'), (4, 'Хорошо'), (5, 'Отлично')], verbose_name='Оценка')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='site_app.myuser', verbose_name='Имя пользователя')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
                'ordering': ['user'],
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название услуги')),
                ('price', models.PositiveIntegerField(verbose_name='Цена')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание услуги')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='services', to='site_app.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Услуга',
                'verbose_name_plural': 'Услуги',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата')),
                ('time', models.TimeField(verbose_name='Время')),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='site_app.master', verbose_name='Мастер')),
            ],
            options={
                'verbose_name': 'Расписание',
                'verbose_name_plural': 'Расписания',
                'ordering': ['date', 'time'],
                'unique_together': {('master', 'date', 'time')},
            },
        ),
    ]
