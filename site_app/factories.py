import factory
from factory.django import ImageField

from site_app import models

class MyUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.MyUser

    name = factory.Faker('name')
    phone = factory.Faker('phone_number')
    email = factory.Faker('email')
    picture = factory.django.ImageField(filename='avatar.jpg')
    password = factory.Faker('password')
    birthday = factory.Faker('date_of_birth', minimum_age=18, maximum_age=90)
    bonuses = factory.Faker('random_int', min=0, max=500)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Category

    name = factory.Faker('word')
    description = factory.Faker('text')
    picture = factory.django.ImageField(filename='category.jpg')


class ServiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Service

    name = factory.Faker('word')
    price = factory.Faker('random_int', min=100, max=10000)
    description = factory.Faker('text')
    category = factory.SubFactory(CategoryFactory)
    picture = factory.django.ImageField(filename='service.jpg')


class MasterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Master

    name = factory.Faker('name')
    description = factory.Faker('text')
    picture = factory.django.ImageField(filename='master_avatar.jpg')

    @factory.post_generation
    def category(self, create, extracted, **kwargs):
        if not create:
            # Если объект не сохраняется в БД, пропускаем настройку полей many-to-many
            return
        if extracted:
            # Если передан список категорий, добавляем их
            for category in extracted:
                self.category.add(category)
        else:
            # Иначе создаем одну категорию по умолчанию
            self.category.add(CategoryFactory())

class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Review

    user = factory.SubFactory(MyUserFactory)
    text = factory.Faker('text')
    grade = factory.Faker('random_element', elements=[1, 2, 3, 4, 5])

class ScheduleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Schedule

    master = factory.SubFactory(MasterFactory)
    date = factory.Faker('date_this_month')  # Генерируем дату в пределах текущего месяца
    time = factory.Faker('time_object')      # Генерируем случайное время

class RecordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Record