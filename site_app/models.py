from django.db import models


class MyUser(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=100)
    phone = models.CharField(verbose_name='Телефон', max_length=100, unique=True)
    email = models.EmailField(verbose_name='Почта', unique=True, null=True, blank=True)
    picture = models.ImageField(verbose_name='Аватарка', upload_to='profile_picture', blank=True, null=True)
    password = models.CharField(verbose_name='Пароль', max_length=100)
    birthday = models.DateField(verbose_name='Дата Рождения')
    bonuses = models.PositiveIntegerField(verbose_name='Бонусы', default=0)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(verbose_name='Название категории', max_length=100, unique=True)
    description = models.TextField(verbose_name='Описание категории', blank=True, null=True)
    picture = models.ImageField(verbose_name='Изображение категории', upload_to='category_picture',
                                blank=True, null=True)
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(verbose_name='Название услуги', max_length=100, unique=True)
    price = models.PositiveIntegerField(verbose_name='Цена')
    description = models.TextField(verbose_name='Описание услуги', blank=True, null=True)
    category = models.ForeignKey(Category, verbose_name='Категория', related_name='services',
                                    on_delete=models.SET_NULL, null=True)
    picture = models.ImageField(verbose_name='Изображение услуги', upload_to='service_picture',
                                blank=True, null=True)

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['name']

    def __str__(self):
        return self.name


class Master(models.Model):
    name = models.CharField(verbose_name='Имя мастера', max_length=100)
    description = models.TextField(verbose_name='Описание мастера', blank=True, null=True)
    picture = models.ImageField(verbose_name='Аватарка мастера', upload_to='master_picture', blank=True, null=True)
    category = models.ManyToManyField(Category, verbose_name='Категория', related_name='masters')

    class Meta:
        verbose_name = 'Мастер'
        verbose_name_plural = 'Мастеры'
        ordering = ['id']

    def __str__(self):
        return self.name


class Review(models.Model):
    GRADE_CHOICES = [
        (1, 'Очень плохо'),
        (2, 'Плохо'),
        (3, 'Средне'),
        (4, 'Хорошо'),
        (5, 'Отлично'),
    ]
    user = models.OneToOneField(MyUser, verbose_name='Имя пользователя',
                                on_delete=models.SET_NULL, related_name='reviews', null=True)
    text = models.TextField(verbose_name='Текст отзыва', blank=True, null=True)
    grade = models.PositiveIntegerField(verbose_name='Оценка', choices=GRADE_CHOICES)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['user']

    def __str__(self):
        return f"Отзыв от {self.user.name} - Оценка: {self.grade}"


class Schedule(models.Model):
    master = models.ForeignKey(Master, verbose_name='Мастер', related_name='schedules', on_delete=models.CASCADE)
    date = models.DateField(verbose_name='Дата')
    time = models.TimeField(verbose_name='Время')

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'
        ordering = ['date', 'time']
        unique_together = ('master', 'date', 'time')

    def __str__(self):
        return f'{self.date} {self.time}'


class Record(models.Model):
    category = models.ForeignKey(Category, verbose_name='Категория',
                                 related_name='records', on_delete=models.CASCADE, null=True)
    service = models.ForeignKey(Service, verbose_name='Услуга',
                                related_name='records', on_delete=models.CASCADE)
    master = models.ForeignKey(Master, verbose_name='Мастер',
                               related_name='records', on_delete=models.CASCADE)
    datetime = models.ForeignKey(Schedule, verbose_name='Дата и время',
                                 related_name='records', on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(MyUser, verbose_name='Пользователь',
                             related_name='records', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        ordering = ['datetime']