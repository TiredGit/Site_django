from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView


from site_app import models


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

        if not (phone.startswith('+7') and len(phone) == 12 and phone[1:].isdigit()):
            messages.error(request, "Неверный формат номера")
            return redirect('register')

        if password1 != password2:
            messages.error(request, "Пароли не совпадают.")
            return redirect('register')

        if models.MyUser.objects.filter(phone=phone).exists():
            messages.error(request, "Пользователь с таким номером телефона уже существует.")
            return redirect('register')

        hashed_password=make_password(password1)

        user = models.MyUser.objects.create(name=name, phone=phone, password=hashed_password, birthday=birthday)

        request.session['user_id'] = user.id
        request.session['user_name'] = user.name
        return redirect('main')

    return render(request, 'register.html', {'user': user})


def logout(request):
    request.session.flush()  # Удаляем данные сессии
    return redirect('login')


def booking(request):
    user = None
    if 'user_id' in request.session:
        user = models.MyUser.objects.get(id=request.session['user_id'])
    return render(request, 'booking.html', {'user': user})

def profile(request):
    user = None
    if 'user_id' in request.session:
        user = models.MyUser.objects.get(id=request.session['user_id'])
    return render(request, 'profile.html', {'user': user})