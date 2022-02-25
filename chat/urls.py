from django.urls import path
from .views import index, login_view, register, addcontact, logout_view, profile, edit

app_name = 'chat'

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),
    path('addcontact/', addcontact, name='newcontact'),
    path('profile/<str:username>', profile, name='profile'),
    path('edit/', edit, name='edit')
]
