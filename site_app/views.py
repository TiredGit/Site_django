from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, DetailView, ListView, TemplateView

from django_filters.views import FilterView
from site_app.filters import MasterFilter

from site_app import models

import re

from django.core.mail import send_mail
from django.conf import settings


class MainView(FilterView):
    model = models.Master
    template_name = 'main.html'
    context_object_name = 'masters'
    filterset_class = MasterFilter

    def get_filterset(self, filterset_class):
        # Получаем выбранную категорию из параметров запроса
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
    request.session.flush()  # Удаляем данные сессии
    return redirect('login')


def booking(request):
    user = None
    if 'user_id' in request.session:
        user = models.MyUser.objects.get(id=request.session['user_id'])
        return render(request, 'booking.html', {'user': user, 'show_modal': False})
    else:
        return render(request, 'booking.html', {'user': user, 'show_modal': True})

class UserProfileView(UpdateView):
    model = models.MyUser
    template_name = 'profile.html'
    context_object_name = 'user'
    fields = ['name', 'phone', 'email', 'picture', 'birthday']
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        user_id = self.request.session.get('user_id')
        if user_id:
            return models.MyUser.objects.get(id=user_id)
        return None

    def form_valid(self, form):
        current_password = self.request.POST.get('current_password')
        new_password = self.request.POST.get('new_password')
        confirm_new_password = self.request.POST.get('confirm_new_password')

        if not check_password(current_password, self.object.password):
            messages.error(self.request, "Неверный текущий пароль.")
            return redirect(f'{reverse_lazy("profile")}?edit=true')

        if new_password:
            if new_password != confirm_new_password:
                messages.error(self.request, "Новые пароли не совпадают.")
                return redirect(f'{reverse_lazy("profile")}?edit=true')
            else:
                self.object.password = make_password(new_password)

        phone = form.cleaned_data.get('phone')
        if models.MyUser.objects.exclude(id=self.object.id).filter(phone=phone).exists():
            messages.error(self.request, "Пользователь с таким номером телефона уже существует.")
            return redirect(f'{reverse_lazy("profile")}?edit=true')

        email = form.cleaned_data.get('email')
        if email and models.MyUser.objects.exclude(id=self.object.id).filter(email=email).exists():
            messages.error(self.request, "Пользователь с таким email уже существует.")
            return redirect(f'{reverse_lazy("profile")}?edit=true')

        self.object.save()
        return super().form_valid(form)


#def profile(request):
#    user = models.MyUser.objects.get(id=request.session['user_id'])
#
#    if request.method == 'POST':
#        name = request.POST.get('name')
#        phone = request.POST.get('phone')
#        birthday = request.POST.get('birthday')
#        current_password = request.POST.get('current_password')
#        new_password = request.POST.get('new_password')
#        confirm_new_password = request.POST.get('confirm_new_password')
#
#        if not check_password(current_password, user.password):
#            messages.error(request, "Неверный текущий пароль.")
#            return redirect('profile')
#
#        if models.MyUser.objects.filter(phone=phone).exists():
#            messages.error(request, "Пользователь с таким номером телефона уже существует.")
#            return redirect('profile')
#
#        user.name = name
#        user.phone = phone
#        user.birthday = birthday
#
#        if new_password:
#            if new_password == confirm_new_password:
#                user.password = make_password(new_password)
#            else:
#                messages.error(request, "Новые пароли не совпадают.")
#                return redirect('profile')
#
#        user.save()
#        return redirect('profile')
#
#    return render(request, 'profile.html', {'user': user})

def gallery(request):
    user = None
    if 'user_id' in request.session:
        user = models.MyUser.objects.get(id=request.session['user_id'])
    return render(request, 'gallery.html', {'user': user})