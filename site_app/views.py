from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from site_app import models

import re

from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def main(request):
    user = None
    if 'user_id' in request.session:
        user = models.MyUser.objects.get(id=request.session['user_id'])
    return render(request, 'main.html', {'user': user})

def login(request):
    user = None

    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        print(f"Телефон введен: {phone}")

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

def profile(request):
    user = None
    if 'user_id' in request.session:
        user = models.MyUser.objects.get(id=request.session['user_id'])
    return render(request, 'profile.html', {'user': user})

def gallery(request):
    user = None
    if 'user_id' in request.session:
        user = models.MyUser.objects.get(id=request.session['user_id'])
    return render(request, 'gallery.html', {'user': user})