from django.shortcuts import render, redirect, reverse
from django.views.generic import View

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password

from django.contrib.auth import authenticate, login, logout

from django.forms import ValidationError

from .models import Day


class Index(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('diaryApp:diary'))
        else:
            return render(request, "index.html")

    def post(self, request):
        try:
            first_name = request.POST.get("name").split(" ")[0]
            last_name = request.POST.get("name").split(" ")[1]
        except IndexError:
            raise ValidationError("Name and surname.")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password == password2:
            user = User.objects.create(
                first_name=first_name, last_name=last_name, email=email, username=username, password=make_password(password))

            user.save()

            return redirect(reverse("diaryApp:login"))
        else:
            raise ValidationError("Passwords don't match.")


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        user_pwd = User.objects.get(username=username).password

        auth = check_password(password, user_pwd)

        if auth:
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect(reverse("diaryApp:index"))
            else:
                raise ValidationError("Fail")
        else:
            raise ValidationError("Fail")


class Diary(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, "diary.html")
        else:
            return redirect(reverse('diaryApp:login'))

    def post(self, request):
        feel = request.POST.get('feelData')
        text = request.POST.get("text")

        if request.user.is_authenticated:
            if feel and text:
                day = Day.objects.create(
                    feel_point=feel, diary_text=text, owner=request.user)
                if day:
                    day.save()
                    return redirect(reverse("diaryApp:index"))
                else:
                    raise ValidationError("Invalid input.")

            else:
                raise ValidationError("Invalid input.")
        else:
            return redirect(reverse('diaryApp:login'))


class Logout(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            return redirect(reverse("diaryApp:index"))
        else:
            return redirect(reverse('diaryApp:login'))


class Days(View):
    def get(self, request):
        if request.user.is_authenticated:
            daysqs = Day.objects.filter(owner=request.user).order_by('-date')
            context = {"days": daysqs}
            return render(request, 'days.html', context)
        else:
            return redirect(reverse('diaryApp:login'))
