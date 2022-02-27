from django.shortcuts import render
from bs4news.models import News, News_Analysis_Raw, News_Company
from main.models import User, Dashboard, Noticeboard
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime, timedelta
from konlpy.tag import Okt
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from django.http import HttpResponse
from collections import Counter
import json
import math


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
    focus_word = userData.User_Focus_word
    news_data_analysis_date = []
    news_data_analysis_count = []
    news_data_analysis_counter = []
    news_data_analysis_ratio = []
    wc_news_data_list = []
    temp_save = []
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
            for news_data_morphs_element in news_content:
                if focus_word in news_data_morphs_element:
                    news_data_analysis_count_num += 1
                if i == 1:
                    if len(news_data_morphs_element) > 1:
                        wc_news_data_list.append(news_data_morphs_element)
                if len(news_data_morphs_element) > 1:
                    temp_save.append(news_data_morphs_element)
        temp_result = Counter(temp_save)
        temp_result_10_ratio = [(i, temp_result[i] / len(temp_save) * 100.0) for i, count in temp_result.most_common(10)]
        news_data_analysis_counter.append(temp_result_10_ratio)
        news_data_analysis_ratio.append(temp_result_10_ratio)
        news_data_analysis_date.append(input_date)
        news_data_analysis_count.append(news_data_analysis_count_num)
    news_data_analysis_counter.reverse()
    news_data_analysis_count.reverse()
    news_data_analysis_ratio.reverse()
    news_data_analysis_counter_word = []
    news_data_analysis_counter_value = []
    for news_data_analysis_counter_element in news_data_analysis_counter:
        counter_value = []
        counter_word = []
        for n in news_data_analysis_counter_element:
            counter_word.append(n[0])
            counter_value.append(round(n[1],2))
        news_data_analysis_counter_word.append(counter_word)
        news_data_analysis_counter_value.append(counter_value)

    news_data_analysis_counter_list = list(zip(news_data_analysis_counter_word, news_data_analysis_counter_value))

    wc_result = Counter(wc_news_data_list)
    wc_most_word_50 = wc_result.most_common(50)
    wc_most_word_50_jsonStr = ''
    for wc_most_word_50_element in wc_most_word_50:
        wc_most_word_50_jsonStr += '{"tag":"'
        wc_most_word_50_jsonStr += str(wc_most_word_50_element[0])
        wc_most_word_50_jsonStr += '",'
        wc_most_word_50_jsonStr += '"weight":'
        wc_most_word_50_jsonStr += str(wc_most_word_50_element[1])
        wc_most_word_50_jsonStr += '},'

    return render(request, 'index.html', {'news_count': obj.Dashboard_Total_News_Count,
                                          'news_analysis_count': obj.Dashboard_Total_Analysis_Count,
                                          'news_analysis_rate': obj.Dashboard_Total_Analysis_Rate,
                                          'news_data': wc_most_word_50_jsonStr,
                                          'today_news_count': obj.Dashboard_Today_count,
                                          'focus_company_name': focus_company_name,
                                          'focus_word': focus_word,
                                          'news_data_analysis_date': news_data_analysis_date,
                                          'news_data_analysis_count': news_data_analysis_count,
                                          'news_data_analysis_counter_list': news_data_analysis_counter_list
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
            User_Focus_Company_1='KBS',
            User_Focus_Company_2='SBS',
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
    userFocusCompany1 = request_input['userFocusCompany1']
    userFocusCompany2 = request_input['userFocusCompany2']
    currentPassword = request_input['currentPassword']

    if userData.User_Password == currentPassword:
        userData.User_Name = userName
        userData.User_Info = '안녕하세요'
        userData.User_MobileNumber = userMobileNumber
        userData.User_Email = userEmail
        userData.User_RecentDT = datetime.now()
        userData.User_Focus_word = userFocusWord
        userData.User_Focus_Company = userFocusCompany
        userData.User_Focus_Company_1 = userFocusCompany1
        userData.User_Focus_Company_2 = userFocusCompany2
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


def analysisraw(request):
    if request.method == 'GET' and 'keyword' in request.GET:
        News_data = News_Analysis_Raw.objects.filter(News_Morphs__contains=request.GET['keyword']).order_by('-News_Analysis_CreateDT')
    else:
        News_data = News_Analysis_Raw.objects.all().order_by('-News_Analysis_CreateDT')
    paginator = Paginator(News_data, 20)
    page = request.GET.get('page')
    try:
        news_list = paginator.get_page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        news_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        news_list = paginator.page(paginator.num_pages)
    return render(request, 'analysisraw.html', {'news_list': news_list})


def datapolicy(request):
    policy_data = Noticeboard.objects.filter(Noticeboard_Type='data').order_by('-Noticeboard_CreateDT')
    paginator = Paginator(policy_data, 10)
    page = request.GET.get('page')
    try:
        policy_list = paginator.get_page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        policy_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        policy_list = paginator.page(paginator.num_pages)
    return render(request, 'datapolicy.html', {'policy_list': policy_list})


def keyworddashboard(request):
    return render(request, 'keyworddashboard.html')


def mycrawl(request):
    return render(request, 'mycrawl.html')


def mykeyword(request):
    return render(request, 'mykeyword.html')


def mynews(request):
    return render(request, 'mynews.html')


def myscrap(request):
    return render(request, 'myscrap.html')


def newsdashboard(request):

    graph_news_all_count = []
    user_id = request.session['userId']
    userData = User.objects.get(User_Id=user_id)
    print(userData)
    focus1_company_name = userData.User_Focus_Company
    focus1_company_code = News_Company.objects.get(News_Company_Name=focus1_company_name).News_Company_Code
    focus2_company_name = userData.User_Focus_Company_1
    focus2_company_code = News_Company.objects.get(News_Company_Name=focus2_company_name).News_Company_Code
    focus3_company_name = userData.User_Focus_Company_2
    focus3_company_code = News_Company.objects.get(News_Company_Name=focus3_company_name).News_Company_Code

    focus_all_data_news = []
    focus1_data_news = []
    focus2_data_news = []
    focus3_data_news = []
    graph_focus_news_count_jsonStr = ''
    for i in range(0, 7):
        graph_check_date = datetime.today() - timedelta(days=i)
        graph_input_date = str(graph_check_date.year) + '-' + str(graph_check_date.month) + '-' + str(graph_check_date.day)
        graph_from_date = datetime.strptime(graph_input_date, '%Y-%m-%d').date()
        graph_from_date = datetime.combine(graph_from_date, datetime.min.time())
        graph_to_date = datetime.combine(graph_from_date, datetime.max.time())
        graph_news_data_date = News_Analysis_Raw.objects.filter(News_Analysis_CreateDT__range=(graph_from_date, graph_to_date))
        graph_focus1_news_count = 0
        graph_focus2_news_count = 0
        graph_focus3_news_count = 0
        graph_focus_news_count = 0
        for graph_count_target_news in graph_news_data_date:
            if graph_count_target_news.News_Analysis_Company == focus1_company_code\
                    or graph_count_target_news.News_Analysis_Company == focus2_company_code\
                    or graph_count_target_news.News_Analysis_Company == focus3_company_code:
                graph_focus_news_count += 1
                focus_all_data_news.append(graph_count_target_news)
                if graph_count_target_news.News_Analysis_Company == focus1_company_code:
                    graph_focus1_news_count += 1
                    focus1_data_news.append(graph_count_target_news)
                elif graph_count_target_news.News_Analysis_Company == focus2_company_code:
                    graph_focus2_news_count += 1
                    focus2_data_news.append(graph_count_target_news)
                elif graph_count_target_news.News_Analysis_Company == focus3_company_code:
                    graph_focus3_news_count += 1
                    focus3_data_news.append(graph_count_target_news)
        graph_focus_news_count_jsonStr += '{"date":"'
        graph_focus_news_count_jsonStr += graph_input_date
        graph_focus_news_count_jsonStr += '",'
        graph_focus_news_count_jsonStr += '"focus1":'
        graph_focus_news_count_jsonStr += str(graph_focus1_news_count)
        graph_focus_news_count_jsonStr += ','
        graph_focus_news_count_jsonStr += '"focus2":'
        graph_focus_news_count_jsonStr += str(graph_focus2_news_count)
        graph_focus_news_count_jsonStr += ','
        graph_focus_news_count_jsonStr += '"focus3":'
        graph_focus_news_count_jsonStr += str(graph_focus3_news_count)
        graph_focus_news_count_jsonStr += ','
        graph_focus_news_count_jsonStr += '"focus":'
        graph_focus_news_count_jsonStr += str(graph_focus_news_count)
        graph_focus_news_count_jsonStr += '},'
        print(graph_focus_news_count_jsonStr)

    focus_temp_save = []
    for focus_data_element in focus_all_data_news:
        focus_news_content = focus_data_element.News_Morphs.split(',')
        for focus_news_data_morphs_element in focus_news_content:
            focus_temp_save.append(focus_news_data_morphs_element)
    focus_result = Counter(focus_temp_save)
    focus_most_word_100 = focus_result.most_common(50)
    focus_most_word_100_jsonStr = ''
    for focus_most_word_100_element in focus_most_word_100:
        focus_most_word_100_jsonStr += '{"tag":"'
        focus_most_word_100_jsonStr += str(focus_most_word_100_element[0])
        focus_most_word_100_jsonStr += '",'
        focus_most_word_100_jsonStr += '"weight":'
        focus_most_word_100_jsonStr += str(focus_most_word_100_element[1])
        focus_most_word_100_jsonStr += '},'
    print(focus_most_word_100_jsonStr)

    focus1_temp_save = []
    for focus1_data_element in focus1_data_news:
        focus1_news_content = focus1_data_element.News_Morphs.split(',')
        for focus1_news_data_morphs_element in focus1_news_content:
            focus1_temp_save.append(focus1_news_data_morphs_element)
    focus1_result = Counter(focus1_temp_save)
    focus1_most_word_50 = focus1_result.most_common(50)
    focus1_most_word_50_jsonStr = ''
    for focus1_most_word_50_element in focus1_most_word_50:
        focus1_most_word_50_jsonStr += '{"tag":"'
        focus1_most_word_50_jsonStr += str(focus1_most_word_50_element[0])
        focus1_most_word_50_jsonStr += '",'
        focus1_most_word_50_jsonStr += '"weight":'
        focus1_most_word_50_jsonStr += str(focus1_most_word_50_element[1])
        focus1_most_word_50_jsonStr += '},'
    print(focus1_most_word_50_jsonStr)

    focus2_temp_save = []
    for focus2_data_element in focus2_data_news:
        focus2_news_content = focus2_data_element.News_Morphs.split(',')
        for focus2_news_data_morphs_element in focus2_news_content:
            focus2_temp_save.append(focus2_news_data_morphs_element)
    focus2_result = Counter(focus2_temp_save)
    focus2_most_word_50 = focus2_result.most_common(50)
    focus2_most_word_50_jsonStr = ''
    for focus2_most_word_50_element in focus2_most_word_50:
        focus2_most_word_50_jsonStr += '{"tag":"'
        focus2_most_word_50_jsonStr += str(focus2_most_word_50_element[0])
        focus2_most_word_50_jsonStr += '",'
        focus2_most_word_50_jsonStr += '"weight":'
        focus2_most_word_50_jsonStr += str(focus2_most_word_50_element[1])
        focus2_most_word_50_jsonStr += '},'
    print(focus2_most_word_50_jsonStr)

    focus3_temp_save = []
    for focus3_data_element in focus3_data_news:
        focus3_news_content = focus3_data_element.News_Morphs.split(',')
        for focus3_news_data_morphs_element in focus3_news_content:
            focus3_temp_save.append(focus3_news_data_morphs_element)
    focus3_result = Counter(focus3_temp_save)
    focus3_most_word_50 = focus3_result.most_common(50)
    focus3_most_word_50_jsonStr = ''
    for focus3_most_word_50_element in focus3_most_word_50:
        focus3_most_word_50_jsonStr += '{"tag":"'
        focus3_most_word_50_jsonStr += str(focus3_most_word_50_element[0])
        focus3_most_word_50_jsonStr += '",'
        focus3_most_word_50_jsonStr += '"weight":'
        focus3_most_word_50_jsonStr += str(focus3_most_word_50_element[1])
        focus3_most_word_50_jsonStr += '},'
    print(focus3_most_word_50_jsonStr)

    return render(request, 'newsdashboard.html', {'graph_news_all_count': graph_focus_news_count_jsonStr,
                                                  'all_news_data': focus_most_word_100_jsonStr,
                                                  'focus1_company_name': focus1_company_name,
                                                  'focus1_news_data': focus1_most_word_50_jsonStr,
                                                  'focus2_company_name': focus2_company_name,
                                                  'focus2_news_data': focus2_most_word_50_jsonStr,
                                                  'focus3_company_name': focus3_company_name,
                                                  'focus3_news_data': focus3_most_word_50_jsonStr})


def newsraw(request):
    if request.method == 'GET' and 'keyword' in request.GET:
        News_data = News.objects.filter(News_contents__contains=request.GET['keyword']).order_by('-News_CreateDT')
    else:
        News_data = News.objects.all().order_by('-News_CreateDT')
    paginator = Paginator(News_data, 20)
    page = request.GET.get('page')
    try:
        news_list = paginator.get_page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        news_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        news_list = paginator.page(paginator.num_pages)
    return render(request, 'newsraw.html', {'news_list': news_list})


def qna(request):
    return render(request, 'qna.html')


def requestcrawl(request):
    return render(request, 'requestcrawl.html')


def requestscrap(request):
    return render(request, 'requestscrap.html')


def sitepolicy(request):
    policy_data = Noticeboard.objects.filter(Noticeboard_Type='site').order_by('-Noticeboard_CreateDT')
    paginator = Paginator(policy_data, 10)
    page = request.GET.get('page')
    try:
        policy_list = paginator.get_page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        policy_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        policy_list = paginator.page(paginator.num_pages)
    return render(request, 'sitepolicy.html', {'policy_list': policy_list})


def techsupport(request):
    return render(request, 'techsupport.html')