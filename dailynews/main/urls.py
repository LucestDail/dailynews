from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('index', views.index, name='index'),
    path('register',views.register, name='register'),
    path('forgotPassword', views.forgotPassword, name='forgotPassword')
]