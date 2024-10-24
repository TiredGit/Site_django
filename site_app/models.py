from django.db import models

class MyUser(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=100)
    phone = models.CharField(verbose_name='Телефон', max_length=100, unique=True)
    picture = models.ImageField(verbose_name='Аватарка', upload_to='profile_picture', blank=True, null=True)
    password = models.CharField(verbose_name='Пароль', max_length=100)
    birthday = models.DateField(verbose_name='Дата Рождения')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'