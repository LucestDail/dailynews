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
    path('requestFocusData', views.requestFocusData, name='requestFocusData'),
    path('analysisraw', views.analysisraw, name='analysisraw'),
    path('datapolicy', views.datapolicy, name='datapolicy'),
    path('keyworddashboard', views.keyworddashboard, name='keyworddashboard'),
    path('mycrawl', views.mycrawl, name='mycrawl'),
    path('mykeyword', views.mykeyword, name='mykeyword'),
    path('mynews', views.mynews, name='mynews'),
    path('myscrap', views.myscrap, name='myscrap'),
    path('newsdashboard', views.newsdashboard, name='newsdashboard'),
    path('newsraw', views.newsraw, name='newsraw'),
    path('qna', views.qna, name='qna'),
    path('requestcrawl', views.requestcrawl, name='requestcrawl'),
    path('requestscrap', views.requestscrap, name='requestscrap'),
    path('sitepolicy', views.sitepolicy, name='sitepolicy'),
    path('techsupport', views.techsupport, name='techsupport'),
]