from django.shortcuts import render
from bs4news.models import News, News_Analysis_Raw, News_Company
from main.models import User, Dashboard
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
    obj = Dashboard.objects.last()
    focus_object = News_Company.objects.get(News_Company_Name=userData.User_Focus_Company)
    focus_company_name = focus_object.News_Company_Name
    focus_company = focus_object.News_Company_Code
    wc_check_date = datetime.today() - timedelta(days=1)
    wc_input_date = str(wc_check_date.year) + '-' + str(wc_check_date.month) + '-' + str(wc_check_date.day)
    wc_from_date = datetime.strptime(wc_input_date, '%Y-%m-%d').date()
    wc_from_date = datetime.combine(wc_from_date, datetime.min.time())
    wc_to_date = datetime.combine(wc_from_date, datetime.max.time())
    news_data_all = News_Analysis_Raw.objects.filter(News_Analysis_CreateDT__range=(wc_from_date, wc_to_date),
                                                     News_Analysis_Company=focus_company)
    news_data_string = ''
    for news_element in news_data_all:
        news_content = news_element.News_Morphs.split(',')
        for news_data_morphs_element in news_content:
            if len(news_data_morphs_element) > 1:
                news_data_string += ' '
                news_data_string += news_data_morphs_element

    focus_word = userData.User_Focus_word
    news_data_analysis_date = []
    news_data_analysis_count = []
    for i in range(0, 7):
        check_date = datetime.today() - timedelta(days=i)
        input_date = str(check_date.year) + '-' + str(check_date.month) + '-' + str(check_date.day)
        from_date = datetime.strptime(input_date, '%Y-%m-%d').date()
        from_date = datetime.combine(from_date, datetime.min.time())
        to_date = datetime.combine(from_date, datetime.max.time())

        news_data_date = News_Analysis_Raw.objects.filter(News_Analysis_CreateDT__range=(from_date, to_date),
                                                          News_Analysis_Company=focus_company)
        news_data_analysis_count_num = 0
        for news_element in news_data_date:
            news_content = news_element.News_Morphs.split(',')
            for n in news_content:
                if focus_word in n:
                    news_data_analysis_count_num += 1

        news_data_analysis_date.append(input_date)
        news_data_analysis_count.append(news_data_analysis_count_num)
        print(news_data_analysis_date)
        print(news_data_analysis_count)

    news_data_analysis_count.reverse()
    return render(request, 'index.html', {'news_count': obj.Dashboard_Total_News_Count,
                                          'news_analysis_count': obj.Dashboard_Total_Analysis_Count,
                                          'news_analysis_rate': obj.Dashboard_Total_Analysis_Rate,
                                          'news_data': news_data_string,
                                          'today_news_count': obj.Dashboard_Today_count,
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
            User_Focus_Company='연합뉴스',
            User_Focus_word='코로나',
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
    company_data = News_Company.objects.all()
    return render(request, 'profile.html', {'user_data': userData,
                                            'company_data': company_data})


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


def dashboard(request):
    print('django main dashboard_every_minute crontab started -------------------')
    news_data_count = News.objects.all()
    news_data_count_input = len(news_data_count)
    print(news_data_count_input)
    news_analysis_count_data = News_Analysis_Raw.objects.all()
    news_analysis_count = len(news_analysis_count_data)
    print(news_analysis_count)
    news_analysis_rate = round((news_analysis_count / news_data_count_input) * 100)
    print(news_analysis_rate)
    today_check_date = datetime.today() - timedelta(days=1)
    today_input_date = str(today_check_date.year) + '-' + str(today_check_date.month) + '-' + str(today_check_date.day)
    today_from_date = datetime.strptime(today_input_date, '%Y-%m-%d').date()
    today_from_date = datetime.combine(today_from_date, datetime.min.time())
    today_to_date = datetime.combine(today_from_date, datetime.max.time())
    today_news_data_date = News_Analysis_Raw.objects.filter(News_Analysis_CreateDT__range=(today_from_date,
                                                                                           today_to_date))
    today_news_date_count = len(today_news_data_date)
    print(today_news_date_count)
    Dashboard_instance = Dashboard(
        Dashboard_Total_News_Count=news_data_count_input,
        Dashboard_Total_Analysis_Count=news_analysis_count,
        Dashboard_Total_Analysis_Rate=news_analysis_rate,
        Dashboard_Today_count=today_news_date_count,
        Dashboard_CreateDT=datetime.now(),
    )
    Dashboard_instance.save()
    print('django main dashboard_every_minute crontab started -------------------')


def requestFocusData(request):
    return render(request, 'requestFocusData.html')