from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('index', views.index, name='index'),
    path('register', views.register, name='register'),
    path('forgotPassword', views.forgotPassword, name='forgotPassword'),
    path('loginUser', views.login_user),
    path('initPassword', views.initPassword),
    path('requestRegister', views.requestRegister),
    path('basicTemplates', views.basicTemplates, name='basicTemplates'),
    path('profile', views.profile, name='profile'),
    path('requestProfile', views.requestProfile),
    path('deleteProfile', views.deleteProfile),
    path('requestPasswordChange', views.requestPasswordChange),
    path('dashboard', views.dashboard),
]