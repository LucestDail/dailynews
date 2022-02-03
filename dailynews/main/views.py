from django.shortcuts import render
from bs4news.models import News
from main.models import User
from datetime import datetime, timedelta
from konlpy.tag import Okt
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from django.http import HttpResponse


# Create your views here.


def basicTemplates(request):
    return render(request, 'basicTemplates.html')


def login(request):
    return render(request, 'login.html')


@csrf_exempt
def login_user(request):
    request_input = json.loads(request.body)
    user_id = request_input['inputId']
    user_password = request_input['inputPassword']
    if User.objects.filter(User_Id=user_id, User_Password=user_password):
        print("user exist")
        request.session["userId"] = user_id
        currentUser = User.objects.get(User_Id=user_id)
        currentUser.RecentDT = datetime.now()
        currentUser.save()
        result = "TRUE"
    else:
        print("user not exist")
        result = "FALSE"
    return HttpResponse(result, content_type='text')


def index(request):
    if 'userId' not in request.session:
        return render(request, 'login.html')
    user_id = request.session['userId']
    userData = User.objects.get(User_Id=user_id)
    focus_company_name = '경향신문'
    focus_company = '032'
    news_data_all = News.objects.filter(News_company=focus_company)
    news_count = len(news_data_all)
    okt = Okt()
    news_data_morphs = []
    for news_element in news_data_all:
        news_content = okt.nouns(news_element.News_contents)
        news_content = [n for n in news_content if len(n) > 1]
        news_data_morphs = news_data_morphs + news_content

    news_data_string = ''
    for news_data_morphs_element in news_data_morphs:
        news_data_string += ' '
        news_data_string += news_data_morphs_element

    focus_word = '것'
    news_data_analysis_date = []
    news_data_analysis_count = []
    for i in range(0, 7):
        check_date = datetime.today() - timedelta(days=i)
        input_date = str(check_date.year) + '-' + str(check_date.month) + '-' + str(check_date.day)
        from_date = datetime.strptime(input_date, '%Y-%m-%d').date()
        from_date = datetime.combine(from_date, datetime.min.time())
        to_date = datetime.combine(from_date, datetime.max.time())
        news_data_date = News.objects.filter(News_CreateDT__range=(from_date, to_date))
        for news_element in news_data_date:
            news_content = okt.nouns(news_element.News_contents)
            news_content = [n for n in news_content if n in focus_word]
        news_data_analysis_date.append(input_date)
        news_data_analysis_count.append(len(news_content))
        print(news_data_analysis_date)
        print(news_data_analysis_count)
        news_content = {}

    return render(request, 'index.html', {'news_count': news_count,
                                          'news_data': news_data_string,
                                          'focus_company_name': focus_company_name,
                                          'focus_word': focus_word,
                                          'news_data_analysis_date': news_data_analysis_date,
                                          'news_data_analysis_count': news_data_analysis_count
                                          })


def register(request):
    return render(request, 'register.html')


@csrf_exempt
def requestRegister(request):
    request_input = json.loads(request.body)
    registerId = request_input['registerId']
    registerName = request_input['registerName']
    registerPassword = request_input['registerPassword']
    if User.objects.filter(User_Id=registerId):
        print("id exist, fail")
        result = "FALSE"
    else:
        user_instance = User(
            User_Id=registerId,
            User_Name=registerName,
            User_Password=registerPassword,
            User_Info='안녕하세요',
            User_CreateDT=datetime.now(),
            User_RecentDT=datetime.now()
        )
        user_instance.save()
        print("register success")
        result = "TRUE"
    return HttpResponse(result, content_type='text')


def forgotPassword(request):
    return render(request, 'forgotPassword.html')


@csrf_exempt
def initPassword(request):
    request_input = json.loads(request.body)
    user_id = request_input['inputId']
    user_name = request_input['inputName']
    if User.objects.filter(User_Id=user_id, User_Name=user_name):
        targetUser = User.objects.get(User_Id=user_id)
        targetUser.User_Password = user_id
        targetUser.save()
        print("password init")
        result = "TRUE"
    else:
        print("user not exist")
        result = "FALSE"
    return HttpResponse(result, content_type='text')


def profile(request):
    user_id = request.session['userId']
    userData = User.objects.get(User_Id=user_id)
    return render(request, 'profile.html', {'user_data': userData})


@csrf_exempt
def requestProfile(request):
    user_id = request.session['userId']
    userData = User.objects.get(User_Id=user_id)
    request_input = json.loads(request.body)
    userName = request_input['userName']
    userMobileNumber = request_input['userMobileNumber']
    userEmail = request_input['userEmail']
    userFocusWord = request_input['userFocusWord']
    userFocusCompany = request_input['userFocusCompany']
    currentPassword = request_input['currentPassword']

    if userData.User_Password == currentPassword:
        userData.User_Name = userName
        userData.User_Info = '안녕하세요'
        userData.User_MobileNumber = userMobileNumber
        userData.User_Email = userEmail
        userData.User_RecentDT = datetime.now()
        userData.User_Focus_word = userFocusWord
        userData.User_Focus_Company = userFocusCompany
        userData.save()
        print("password pass")
        result = "TRUE"
    else:
        print("password not equal")
        result = "FALSE"
    return HttpResponse(result, content_type='text')


@csrf_exempt
def deleteProfile(request):
    user_id = request.session['userId']
    userData = User.objects.get(User_Id=user_id)
    userData.delete()
    return HttpResponse("TRUE", content_type='text')


@csrf_exempt
def requestPasswordChange(request):
    user_id = request.session['userId']
    request_input = json.loads(request.body)
    print(request_input)
    currentPassword = request_input['currentPassword']
    updatePassword = request_input['updatePassword']
    userData = User.objects.get(User_Id=user_id)
    if userData.User_Password == currentPassword:
        userData.User_Password = updatePassword
        userData.save()
        print("password pass")
        result = "TRUE"
    else:
        print("password not equal")
        result = "FALSE"
    return HttpResponse(result, content_type='text')