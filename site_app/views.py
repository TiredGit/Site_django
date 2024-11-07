from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DetailView, ListView, TemplateView, CreateView, DeleteView

from django_filters.views import FilterView
from site_app.filters import MasterFilter, ServiceFilter, MasterSearchFilter

from site_app import models

import re

from django.core.mail import send_mail
from django.conf import settings

from rest_framework import viewsets
from site_app import serializers

class MyUserAPI(viewsets.ModelViewSet):
    queryset = models.MyUser.objects.all()
    serializer_class = serializers.MyUserSerializer


class CategoryAPI(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class ServiceAPI(viewsets.ModelViewSet):
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceSerializer


class MasterAPI(viewsets.ModelViewSet):
    queryset = models.Master.objects.all()
    serializer_class = serializers.MasterSerializer


class ReviewAPI(viewsets.ModelViewSet):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer


class ScheduleAPI(viewsets.ModelViewSet):
    queryset = models.Schedule.objects.all()
    serializer_class = serializers.ScheduleSerializer


class RecordAPI(viewsets.ModelViewSet):
    queryset = models.Record.objects.all()
    serializer_class = serializers.RecordSerializer




class MainView(FilterView):
    model = models.Master
    template_name = 'main.html'
    context_object_name = 'masters'
    filterset_class = MasterFilter

    def get_filterset(self, filterset_class):
        category_id = self.request.GET.get('category')
        self.queryset = models.Master.objects.all()
        if category_id:
            self.queryset = self.queryset.filter(category__id=category_id)
        return filterset_class(self.request.GET, queryset=self.queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = models.Category.objects.all()
        context['reviews'] = models.Review.objects.all()

        user = None
        if 'user_id' in self.request.session:
            user = models.MyUser.objects.get(id=self.request.session['user_id'])
        context['user'] = user

        return context


class CategoryDetailView(DetailView):
    model = models.Category
    template_name = 'category_detail.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = models.Service.objects.filter(category=self.object)

        user = None
        if 'user_id' in self.request.session:
            user = models.MyUser.objects.get(id=self.request.session['user_id'])
        context['user'] = user

        return context


def login(request):
    user = None

    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        if not (phone.startswith('+7') and len(phone) == 12 and phone[1:].isdigit()):
            messages.error(request, "Неверный формат номера")
            return redirect('login')

        try:
            user = models.MyUser.objects.get(phone=phone)
        except models.MyUser.DoesNotExist:
            messages.error(request, "Пользователь с таким номером телефона не найден.")
            return redirect('login')

        if check_password(password, user.password):
            request.session['user_id'] = user.id
            request.session['user_name'] = user.name
            request.session['user_bonuses'] = user.bonuses
            return redirect('main')
        else:
            messages.error(request, "Неверный пароль.")
            return redirect('login')

    return render(request, 'login.html', {'user': user})


def register(request):
    user = None

    if request.method == 'POST':
        name = request.POST.get('first_name')
        phone = request.POST.get('phone')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        birthday = request.POST.get('birthday')
        email = request.POST.get('email')

        if not (phone.startswith('+7') and len(phone) == 12 and phone[1:].isdigit()):
            messages.error(request, "Неверный формат номера")
            return redirect('register')

        if password1 != password2:
            messages.error(request, "Пароли не совпадают.")
            return redirect('register')

        if models.MyUser.objects.filter(phone=phone).exists():
            messages.error(request, "Пользователь с таким номером телефона уже существует.")
            return redirect('register')

        if email:
            email_regex = r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,6}$'
            if not re.match(email_regex, email):
                messages.error(request, "Неверный формат email.")
                return redirect('register')

            if models.MyUser.objects.filter(email=email).exists():
                messages.error(request, "Пользователь с такой почтой уже существует.")
                return redirect('register')
        else:
            email = None

        hashed_password=make_password(password1)

        user = models.MyUser.objects.create(name=name, phone=phone, password=hashed_password, birthday=birthday, email=email)

        request.session['user_id'] = user.id
        request.session['user_name'] = user.name
        request.session['user_bonuses'] = user.bonuses

        if email:
            send_mail(
                'Успешная регистрация!',
                f'Спасибо за регистрацию на нашем сайте, {user.name}!',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

        return redirect('main')

    return render(request, 'register.html', {'user': user})


def logout(request):
    request.session.flush()
    return redirect('login')


class BookingServiceView(FilterView):
    model = models.Service
    template_name = 'booking_service.html'
    context_object_name = 'services'
    filterset_class = ServiceFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = None
        context['show_modal'] = True
        if 'user_id' in self.request.session:
            user = models.MyUser.objects.get(id=self.request.session['user_id'])
            context['show_modal'] = False
        context['user'] = user

        context['categories'] = models.Category.objects.all()

        selected_service_id = self.request.session.get('selected_service_id')
        if selected_service_id:
            selected_service = models.Service.objects.get(id=selected_service_id)
            context['selected_service'] = selected_service
        else:
            context['selected_service'] = None
        return context

def save_selected_service(request, service_id):
    request.session['selected_service_id'] = service_id
    request.session['selected_master_id'] = None
    request.session['selected_schedule_id'] = None
    return redirect('booking_service')


class BookingMasterView(FilterView):
    model = models.Master
    template_name = 'booking_master.html'
    context_object_name = 'masters'
    filterset_class = MasterSearchFilter

    def get_queryset(self):
        queryset = super().get_queryset()

        selected_service_id = self.request.session.get('selected_service_id')
        selected_service = models.Service.objects.get(id=selected_service_id)
        category_id = selected_service.category.id
        queryset = queryset.filter(category__id=category_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = None
        context['show_modal'] = True
        if 'user_id' in self.request.session:
            user = models.MyUser.objects.get(id=self.request.session['user_id'])
            context['show_modal'] = False
        context['user'] = user

        selected_master_id = self.request.session.get('selected_master_id')
        if selected_master_id:
            selected_master = models.Master.objects.get(id=selected_master_id)
            context['selected_master'] = selected_master
        else:
            context['selected_master'] = None

        return context

def save_selected_master(request, master_id):
    request.session['selected_master_id'] = master_id
    request.session['selected_schedule_id'] = None
    return redirect('booking_master')


class BookingDateView(ListView):
    model = models.Schedule
    template_name = 'booking_date.html'
    context_object_name = 'schedules'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = None
        context['show_modal'] = True
        if 'user_id' in self.request.session:
            user = models.MyUser.objects.get(id=self.request.session['user_id'])
            context['show_modal'] = False
        context['user'] = user

        selected_master_id = self.request.session.get('selected_master_id')
        if selected_master_id:
            schedules = models.Schedule.objects.filter(master=selected_master_id)
        else:
            schedules = None

        used_schedule_ids = models.Record.objects.values_list('datetime', flat=True)
        schedules = schedules.exclude(id__in=used_schedule_ids)
        context['schedules'] = schedules

        selected_schedule_id = self.request.session.get('selected_schedule_id')
        if selected_schedule_id:
            selected_schedule = models.Schedule.objects.get(id=selected_schedule_id)
            context['selected_schedule'] = selected_schedule
        else:
            context['selected_schedule'] = None


        return context

def save_selected_schedule(request, schedule_id):
    request.session['selected_schedule_id'] = schedule_id
    return redirect('booking_date')


def create_record(request):
    try:
        selected_schedule_id = request.session.get('selected_schedule_id')
        selected_master_id = request.session.get('selected_master_id')
        selected_service_id = request.session.get('selected_service_id')
        user_id = request.session.get('user_id')

        if not all([selected_schedule_id, selected_master_id, selected_service_id, user_id]):
            raise ValueError("Missing session data")

        schedule = models.Schedule.objects.get(id=selected_schedule_id)
        master = models.Master.objects.get(id=selected_master_id)
        service = models.Service.objects.get(id=selected_service_id)
        user = models.MyUser.objects.get(id=user_id)
        category = service.category

        record = models.Record.objects.create(
            category=category,
            service=service,
            master=master,
            datetime=schedule,
            user=user
        )

        if user.email:
            send_mail(
                "Подтверждение записи",
                f"Здравствуйте, {user.name}!\n\nВы успешно записаны на {record.service}"
                        f" с мастером {record.master} на дату {record.datetime.date} в {record.datetime.time}.",
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

        request.session['selected_service_id'] = None
        request.session['selected_master_id'] = None
        request.session['selected_schedule_id'] = None
        return redirect('profile', pk=user.id)
    except:
        return redirect('booking_time')


class RecordDeleteView(DeleteView):
    model = models.Record
    template_name = 'record_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = None
        if 'user_id' in self.request.session:
            user = models.MyUser.objects.get(id=self.request.session['user_id'])
        context['user'] = user
        context['record'] = models.Record.objects.get(id=self.kwargs['pk'])

        return context

    def get_success_url(self):
        if self.object.user.email:
            send_mail(
                "Запись отменена",
                f"Здравствуйте, {self.object.user.name}!\n\nВаша запись на {self.object.service}"
                f" с мастером {self.object.master} на {self.object.datetime.date} в {self.object.datetime.time} была отменена.",
                settings.DEFAULT_FROM_EMAIL,
                [self.object.user.email],
                fail_silently=False,
            )
        return reverse_lazy('profile', kwargs={'pk': self.object.user.pk})


class UserProfileView(DetailView):
    model = models.MyUser
    template_name = 'profile.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = None
        if 'user_id' in self.request.session:
            user = models.MyUser.objects.get(id=self.request.session['user_id'])
        context['user'] = user

        review = models.Review.objects.filter(user=user).first()
        context['review'] = review

        context['records'] = models.Record.objects.filter(user=user)

        return context


class EditProfileView(UpdateView):
    model = models.MyUser
    template_name = 'edit_profile.html'
    context_object_name = 'user'
    fields = ['name', 'phone', 'email', 'picture', 'birthday']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = None
        if 'user_id' in self.request.session:
            user = models.MyUser.objects.get(id=self.request.session['user_id'])
        context['user'] = user

        return context

    def form_valid(self, form):
        current_password = self.request.POST.get('current_password')
        new_password = self.request.POST.get('new_password')
        confirm_new_password = self.request.POST.get('confirm_new_password')
        phone = self.request.POST.get('phone')
        email = self.request.POST.get('email')
        name = self.request.POST.get('name')
        birthday = self.request.POST.get('birthday')

        if not name:
            messages.error(self.request, "Имя обязательно для заполнения.")
            return self.form_invalid(form)

        if not phone or not (phone.startswith('+7') and len(phone) == 12 and phone[1:].isdigit()):
            messages.error(self.request, "Номер телефона должен быть в формате +7XXXXXXXXXX.")
            return self.form_invalid(form)

        if not birthday:
            messages.error(self.request, "Дата рождения обязательна для заполнения.")
            return self.form_invalid(form)

        if models.MyUser.objects.exclude(id=self.object.id).filter(phone=phone).exists():
            messages.error(self.request, "Пользователь с таким номером телефона уже существует.")
            return self.form_invalid(form)

        if email:
            email_regex = r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,6}$'
            if not re.match(email_regex, email):
                messages.error(self.request, "Неверный формат email.")
                return self.form_invalid(form)

            if models.MyUser.objects.exclude(id=self.object.id).filter(email=email).exists():
                messages.error(self.request, "Пользователь с таким email уже существует.")
                return self.form_invalid(form)

        if not check_password(current_password, self.object.password):
            messages.error(self.request, "Неверный текущий пароль.")
            return self.form_invalid(form)

        if new_password:
            if new_password != confirm_new_password:
                messages.error(self.request, "Новые пароли не совпадают.")
                return self.form_invalid(form)
            else:
                self.object.password = make_password(new_password)

        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.object.pk})


class ReviewView(CreateView):
    model = models.Review
    template_name = 'review.html'
    fields = ['text', 'grade']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = None
        if 'user_id' in self.request.session:
            user = models.MyUser.objects.get(id=self.request.session['user_id'])
        context['user'] = user

        return context

    def form_valid(self, form):
        user_id = self.request.session.get('user_id')
        user = get_object_or_404(models.MyUser, pk=user_id)

        form.instance.user = user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.object.user.pk})


class DeleteReviewView(DeleteView):
    model = models.Review
    template_name = 'review_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = None
        if 'user_id' in self.request.session:
            user = models.MyUser.objects.get(id=self.request.session['user_id'])
        context['user'] = user

        return context

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.object.user.pk})


class UpdateReviewView(UpdateView):
    model = models.Review
    template_name = 'review_update.html'
    fields = ['text', 'grade']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = None
        if 'user_id' in self.request.session:
            user = models.MyUser.objects.get(id=self.request.session['user_id'])
        context['user'] = user

        return context

    def form_valid(self, form):
        user_id = self.request.session.get('user_id')
        user = get_object_or_404(models.MyUser, pk=user_id)

        form.instance.user = user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.object.user.pk})


def gallery(request):
    user = None
    if 'user_id' in request.session:
        user = models.MyUser.objects.get(id=request.session['user_id'])
    return render(request, 'gallery.html', {'user': user})