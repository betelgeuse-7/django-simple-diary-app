from django.urls import path

from .views import Index, Login, Logout, Days, Diary

app_name = "diaryApp"

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("login/", Login.as_view(), name="login"),
    path("logout/", Logout.as_view(), name="logout"),
    path("days/", Days.as_view(), name="days"),
    path("diary/", Diary.as_view(), name="diary"),
]
