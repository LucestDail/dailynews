from django.shortcuts import render
from bs4news.models import *
from main.models import *
from bs4news.snsmodels import *
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
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize, sent_tokenize
import warnings

warnings.filterwarnings("ignore")
# Create your views here.
okt = Okt()


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
    return render(request, 'index.html', {'news_count': obj.Dashboard_Total_News_Count,
                                          'news_analysis_count': obj.Dashboard_Total_Analysis_Count,
                                          'news_analysis_rate': obj.Dashboard_Total_Analysis_Rate,
                                          'today_news_count': obj.Dashboard_Today_count,
                                          'focus_company_name': focus_company_name
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
    if 'userId' not in request.session:
        return render(request, 'login.html')
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


def requestFocusData(request):
    if 'userId' not in request.session:
        return render(request, 'login.html')
    return render(request, 'requestFocusData.html')


def analysisraw(request):
    if 'userId' not in request.session:
        return render(request, 'login.html')
    News_data = []
    if request.method == 'GET' and "page" in request.GET:
        current_page = int((request.GET["page"]))
    else:
        current_page = 1
    search_keyword = ""
    if request.method == 'GET' and 'keyword' in request.GET:
        es_protocol = "http"
        #es_host = "localhost"
        #es_host = "180.70.85.59"
        es_host = "15.164.211.132"
        #es_port = "9200"
        #es_port = "8040"
        es_port = "9200"
        es_search_word = request.GET['keyword']
        search_keyword = es_search_word
        es_url = es_protocol + "://" + es_host + ":" + es_port + "/bs4news_news_analysis_raw/_search"
        if "page" in request.GET:
            query_object = {"query": {"query_string": {"query": "*" + es_search_word + "*"}},
                            "size": 20,
                            "from": 20 * current_page,
                            "sort": {"news_analysis_createdt": "desc"}}
        else:
            query_object = {"query": {"query_string": {"query": "*" + es_search_word + "*"}},
                            "size": 20,
                            "from": 0,
                            "sort": {"news_analysis_createdt": "desc"}}
        res = requests.post(es_url, json=query_object)
        res_json = res.json()["hits"]["hits"]
        total_es_url = es_protocol + "://" + es_host + ":" + es_port + "/bs4news_news_analysis_raw/_count"
        total_query_object = {"query": {"query_string": {"query": "*" + es_search_word + "*"}}}
        total_count_res = requests.post(total_es_url, json=total_query_object)
        print(total_count_res.text)
        total_count = int(total_count_res.json()["count"])
        for one_data in res_json:
            News_data.append(one_data["_source"])
    else:
        es_protocol = "http"
        # es_host = "localhost"
        # es_host = "180.70.85.59"
        es_host = "15.164.211.132"
        # es_port = "9200"
        # es_port = "8040"
        es_port = "9200"
        es_url = es_protocol + "://" + es_host + ":" + es_port + "/bs4news_news_analysis_raw/_search"
        if "page" in request.GET:
            query_object = {"query": {"match_all": {}},
                            "size": 20,
                            "from": 20 * current_page,
                            "sort": {"news_analysis_createdt": "desc"}}
        else:
            query_object = {"query": {"match_all": {}},
                            "size": 20,
                            "from": 0,
                            "sort": {"news_analysis_createdt": "desc"}}
        res = requests.post(es_url, json=query_object)
        res_json = res.json()["hits"]["hits"]
        total_es_url = es_protocol + "://" + es_host + ":" + es_port + "/bs4news_news_analysis_raw/_count"
        total_query_object = {"query": {"match_all": {}}}
        total_count_res = requests.post(total_es_url, json=total_query_object)
        print(total_count_res.text)
        total_count = int(total_count_res.json()["count"])
        for one_data in res_json:
            News_data.append(one_data["_source"])
    news_list = News_data
    page_total = math.ceil(total_count / 20)
    page_previous = current_page - 1
    page_next = current_page + 1
    return render(request, 'analysisraw.html', {'news_list': news_list,
                                            'page_total': page_total,
                                            'page_current': current_page,
                                            'page_previous': page_previous,
                                            'page_next': page_next,
                                            'search_keyword': search_keyword})


def datapolicy(request):
    if 'userId' not in request.session:
        return render(request, 'login.html')
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
    if 'userId' not in request.session:
        return render(request, 'login.html')
    user_id = request.session['userId']
    userData = User.objects.get(User_Id=user_id)
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
    return render(request, 'keyworddashboard.html', {
                                          'focus_company_name': focus_company_name,
                                          'focus_word': focus_word,
                                          'news_data_analysis_date': news_data_analysis_date,
                                          'news_data_analysis_count': news_data_analysis_count,
                                          'news_data_analysis_counter_list': news_data_analysis_counter_list
                                          })


def mycrawl(request):
    if 'userId' not in request.session:
        return render(request, 'login.html')
    if request.method == 'GET' and 'descriptionInfo' in request.GET:
        crawl_data = BS4_NEWS_COMPANY_CRAWL.objects.filter(DESCRIPTION_INFO__contains=request.GET['descriptionInfo']).order_by('-UPDATE_DATETIME')
    else:
        crawl_data = BS4_NEWS_COMPANY_CRAWL.objects.all().order_by('-UPDATE_DATETIME')
    paginator = Paginator(crawl_data, 30)
    page = request.GET.get('page')
    try:
        crawl_list = paginator.get_page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        crawl_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        crawl_list = paginator.page(paginator.num_pages)
    return render(request, 'mycrawl.html', {'crawl_list': crawl_list})


def excludedkeyword(request):
    if 'userId' not in request.session:
        return render(request, 'login.html')
    excluded_word_data = BS4_NEWS_ANALYSIS_WORD_EXCLUDED.objects.all().order_by('-UPDATE_DATETIME')
    paginator = Paginator(excluded_word_data, 15)
    page = request.GET.get('page')
    try:
        excluded_word_data = paginator.get_page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        excluded_word_data = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        excluded_word_data = paginator.page(paginator.num_pages)
    return render(request,
                  'excludedkeyword.html',
                  {'excluded_word_list': excluded_word_data})

def excludedkeywordadd(request):
    if 'userId' not in request.session:
        return render(request, 'login.html')
    user_id = request.session['userId']
    userData = User.objects.get(User_Id=user_id)
    company_data = News_Company.objects.all()
    return render(request, 'excludedkeywordadd.html', {'user_data': userData,
                                            'company_data': company_data})

@csrf_exempt
def excludedkeywordrequest(request):
    if 'userId' not in request.session:
        return render(request, 'login.html')
    user_id = request.session['userId']
    userData = User.objects.get(User_Id=user_id)
    request_input = json.loads(request.body)
    excludedWord = request_input['excludedWord']
    descriptionInfo = request_input['descriptionInfo']
    companyCode = request_input['companyCode']

    if BS4_NEWS_ANALYSIS_WORD_EXCLUDED.objects.filter(COMPANY_CODE=companyCode,
                                                      EXCLUDED_WORD=excludedWord):
        print("duplicated, save fail")
        result = "FALSE"
    else:
        excludedword_instance = BS4_NEWS_ANALYSIS_WORD_EXCLUDED(
            COMPANY_CODE=companyCode,
            EXCLUDED_WORD=excludedWord,
            DESCRIPTION_INFO=descriptionInfo,
            UPDATE_USER=userData.User_Id,
            UPDATE_DATETIME=datetime.now(),
            CREATE_USER=userData.User_Id,
            CREATE_DATETIME=datetime.now()
        )
        excludedword_instance.save()
        print("save success")
        result = "TRUE"
    return HttpResponse(result, content_type='text')



def myscrap(request):
    if 'userId' not in request.session:
        return render(request, 'login.html')
    return render(request, 'myscrap.html')


def newsdashboard(request):

    if 'userId' not in request.session:
        return render(request, 'login.html')

    user_id = request.session['userId']
    userData = User.objects.get(User_Id=user_id)
    company_data = News_Company.objects.all()

    if request.method == 'GET' and "company1" in request.GET:
        focus1_object = News_Company.objects.get(News_Company_Name=(request.GET["company1"]))
        focus1_company_name = focus1_object.News_Company_Name
        focus1_company_code = focus1_object.News_Company_Code
    else:
        focus1_company_name = userData.User_Focus_Company
        focus1_company_code = News_Company.objects.get(News_Company_Name=focus1_company_name).News_Company_Code

    if request.method == 'GET' and "company2" in request.GET:
        focus2_object = News_Company.objects.get(News_Company_Name=(request.GET["company2"]))
        focus2_company_name = focus2_object.News_Company_Name
        focus2_company_code = focus2_object.News_Company_Code
    else:
        focus2_company_name = userData.User_Focus_Company_1
        focus2_company_code = News_Company.objects.get(News_Company_Name=focus2_company_name).News_Company_Code

    if request.method == 'GET' and "company1" in request.GET:
        focus3_object = News_Company.objects.get(News_Company_Name=(request.GET["company3"]))
        focus3_company_name = focus3_object.News_Company_Name
        focus3_company_code = focus3_object.News_Company_Code
    else:
        focus3_company_name = userData.User_Focus_Company_2
        focus3_company_code = News_Company.objects.get(News_Company_Name=focus3_company_name).News_Company_Code


    graph_focus_news_count_jsonStr = ''
    for i in range(1, 6):
        graph_check_date = datetime.today() - timedelta(days=i)
        graph_input_date = str(graph_check_date.year) + '-' + str(graph_check_date.month) + '-' + str(graph_check_date.day)
        graph_from_date = datetime.strptime(graph_input_date, '%Y-%m-%d').date()
        graph_from_date = datetime.combine(graph_from_date, datetime.min.time())
        graph_to_date = datetime.combine(graph_from_date, datetime.max.time())
        graph_news_data_date = News_Analysis_Count_Company.objects.filter(News_Analysis_Count_Company_CreateDT__range=(graph_from_date, graph_to_date))
        graph_focus1_news_count = 0
        graph_focus2_news_count = 0
        graph_focus3_news_count = 0
        graph_focus_news_count = 0
        for graph_count_target_news in graph_news_data_date:
            if graph_count_target_news.News_Analysis_Count_Company_Code == focus1_company_code\
                    or graph_count_target_news.News_Analysis_Count_Company_Code == focus2_company_code\
                    or graph_count_target_news.News_Analysis_Count_Company_Code == focus3_company_code:
                graph_focus_news_count += int(graph_count_target_news.News_Analysis_Count_Company_Count)
                if graph_count_target_news.News_Analysis_Count_Company_Code == focus1_company_code:
                    graph_focus1_news_count += int(graph_count_target_news.News_Analysis_Count_Company_Count)
                elif graph_count_target_news.News_Analysis_Count_Company_Code == focus2_company_code:
                    graph_focus2_news_count += int(graph_count_target_news.News_Analysis_Count_Company_Count)
                elif graph_count_target_news.News_Analysis_Count_Company_Code == focus3_company_code:
                    graph_focus3_news_count += int(graph_count_target_news.News_Analysis_Count_Company_Count)
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

    target_date = datetime.today() - timedelta(days=1)
    format_date = str(target_date.year) + '-' + str(target_date.month) + '-' + str(target_date.day)
    from_date = datetime.strptime(format_date, '%Y-%m-%d').date()
    from_date = datetime.combine(from_date, datetime.min.time())
    to_date = datetime.combine(from_date, datetime.max.time())
    focus1_most_word_50_jsonStr = News_Analysis_Word_Analysis_Company.objects\
        .get(News_Analysis_Word_Analysis_Company_CreateDT__range=(from_date, to_date),
             News_Analysis_Word_Analysis_Company_Code=focus1_company_code)
    focus2_most_word_50_jsonStr = News_Analysis_Word_Analysis_Company.objects \
        .get(News_Analysis_Word_Analysis_Company_CreateDT__range=(from_date, to_date),
                News_Analysis_Word_Analysis_Company_Code=focus2_company_code)
    focus3_most_word_50_jsonStr = News_Analysis_Word_Analysis_Company.objects \
        .get(News_Analysis_Word_Analysis_Company_CreateDT__range=(from_date, to_date),
                News_Analysis_Word_Analysis_Company_Code=focus3_company_code)

    return render(request, 'newsdashboard.html', {'company_data': company_data,
                                                  'graph_news_all_count': graph_focus_news_count_jsonStr,
                                                  'focus1_company_name': focus1_company_name,
                                                  'focus1_news_data': focus1_most_word_50_jsonStr.News_Analysis_Word_Analysis_Company_Data,
                                                  'focus2_company_name': focus2_company_name,
                                                  'focus2_news_data': focus2_most_word_50_jsonStr.News_Analysis_Word_Analysis_Company_Data,
                                                  'focus3_company_name': focus3_company_name,
                                                  'focus3_news_data': focus3_most_word_50_jsonStr.News_Analysis_Word_Analysis_Company_Data})


def newsraw(request):
    if 'userId' not in request.session:
        return render(request, 'login.html')
    News_data = []
    if request.method == 'GET' and "page" in request.GET:
        current_page = int((request.GET["page"]))
    else:
        current_page = 1
    search_keyword = ""
    if request.method == 'GET' and 'keyword' in request.GET:
        es_protocol = "http"
        # es_host = "localhost"
        # es_host = "180.70.85.59"
        es_host = "15.164.211.132"
        # es_port = "9200"
        # es_port = "8040"
        es_port = "9200"
        es_search_word = request.GET['keyword']
        search_keyword = es_search_word
        es_url = es_protocol + "://" + es_host + ":" + es_port + "/bs4news_news/_search"
        if "page" in request.GET:
            query_object = {"query": {"query_string": {"query": "*" + es_search_word + "*"}},
                            "size": 20,
                            "from": 20*current_page,
                            "sort": {"news_createdt": "desc"}}
        else:
            query_object = {"query": {"query_string": {"query": "*" + es_search_word + "*"}},
                            "size": 20,
                            "from": 0,
                            "sort": {"news_createdt": "desc"}}
        res = requests.post(es_url, json=query_object)
        res_json = res.json()["hits"]["hits"]
        total_es_url = es_protocol + "://" + es_host + ":" + es_port + "/bs4news_news/_count"
        total_query_object = {"query": {"query_string": {"query": "*" + es_search_word + "*"}}}
        total_count_res = requests.post(total_es_url, json=total_query_object)
        print(total_count_res.text)
        total_count = int(total_count_res.json()["count"])
        for one_data in res_json:
            News_data.append(one_data["_source"])
        related_keyword = []
        try:
            # model = Word2Vec.load("/Users/oseunghyeon/ddhmodel")
            # model = Word2Vec.load("/home/oshdb/ddhmodel")
            model = Word2Vec.load("/home/ubuntu/ddhmodel")
            related_keyword = model.wv.most_similar(search_keyword)
            related_keyword = dict(related_keyword)
            for key in related_keyword.keys():
                related_keyword[key] = math.ceil(related_keyword[key] * 100)
        except Exception:
            pass

    else:
        es_protocol = "http"
        # es_host = "localhost"
        # es_host = "180.70.85.59"
        es_host = "15.164.211.132"
        # es_port = "9200"
        # es_port = "8040"
        es_port = "9200"
        es_url = es_protocol + "://" + es_host + ":" + es_port + "/bs4news_news/_search"
        if "page" in request.GET:
            query_object = {"query": {"match_all": {}},
                            "size": 20,
                            "from": 20*current_page,
                            "sort": {"news_createdt": "desc"}}
        else:
            query_object = {"query": {"match_all": {}},
                            "size": 20,
                            "from": 0,
                            "sort": {"news_createdt": "desc"}}
        res = requests.post(es_url, json=query_object)
        print(res.text)
        res_json = res.json()["hits"]["hits"]
        total_es_url = es_protocol + "://" + es_host + ":" + es_port + "/bs4news_news/_count"
        total_query_object = {"query": {"match_all": {}}}
        total_count_res = requests.post(total_es_url, json=total_query_object)
        print(total_count_res.text)
        total_count = int(total_count_res.json()["count"])
        for one_data in res_json:
            News_data.append(one_data["_source"])
        related_keyword = []
    news_list = News_data
    page_total = math.ceil(total_count / 20)
    page_previous = current_page - 1
    page_next = current_page + 1

    return render(request, 'newsraw.html', {'news_list': news_list,
                                            'page_total': page_total,
                                            'page_current': current_page,
                                            'page_previous': page_previous,
                                            'page_next': page_next,
                                            'search_keyword': search_keyword,
                                            'related_keyword': related_keyword})


def qna(request):
    if 'userId' not in request.session:
        return render(request, 'login.html')
    return render(request, 'qna.html')


def requestcrawl(request):
    if 'userId' not in request.session:
        return render(request, 'login.html')
    return render(request, 'requestcrawl.html')


def requestscrap(request):
    if 'userId' not in request.session:
        return render(request, 'login.html')
    return render(request, 'requestscrap.html')


def sitepolicy(request):
    if 'userId' not in request.session:
        return render(request, 'login.html')
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

def companywordcloud(request):
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

    return render(request, 'companywordcloud.html', {'news_count': obj.Dashboard_Total_News_Count,
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


def keywordtimedashboard(request):

    if 'userId' not in request.session:
        return render(request, 'login.html')
    user_id = request.session['userId']
    userData = User.objects.get(User_Id=user_id)
    company_data = News_Company.objects.all()
    if request.method == 'GET' and "company" in request.GET:
        focus_object = News_Company.objects.get(News_Company_Name=(request.GET["company"]))
        focus_company_name = focus_object.News_Company_Name
        focus_company = focus_object.News_Company_Code
    else:
        focus_object = News_Company.objects.get(News_Company_Name=userData.User_Focus_Company)
        focus_company_name = focus_object.News_Company_Name
        focus_company = focus_object.News_Company_Code

    if request.method == 'GET' and "keyword" in request.GET:
        focus_word = (request.GET["keyword"])
    else:
        focus_word = userData.User_Focus_word

    news_data_analysis_date = []
    news_data_analysis_count = []
    news_data_analysis_counter = []
    news_data_analysis_ratio = []
    temp_save = []
    for i in range(0, 6):
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
                if len(news_data_morphs_element) > 1:
                    temp_save.append(news_data_morphs_element)
        temp_result = Counter(temp_save)
        temp_result_10_ratio = [(i, temp_result[i] / len(temp_save) * 100.0) for i, count in
                                temp_result.most_common(10)]
        news_data_analysis_counter.append(temp_result_10_ratio)
        news_data_analysis_ratio.append(temp_result_10_ratio)
        news_data_analysis_date.append(input_date)
        news_data_analysis_count.append(news_data_analysis_count_num)
    news_data_analysis_counter.reverse()
    news_data_analysis_count.reverse()
    news_data_analysis_counter_word = []
    news_data_analysis_counter_value = []
    for news_data_analysis_counter_element in news_data_analysis_counter:
        counter_value = []
        counter_word = []
        for n in news_data_analysis_counter_element:
            counter_word.append(n[0])
            counter_value.append(round(n[1], 2))
        news_data_analysis_counter_word.append(counter_word)
        news_data_analysis_counter_value.append(counter_value)
    news_data_analysis_counter_list = list(zip(news_data_analysis_counter_word, news_data_analysis_counter_value))
    return render(request, 'keywordtimedashboard.html', {
          'company_data': company_data,
          'focus_company_name': focus_company_name,
          'focus_word': focus_word,
          'news_data_analysis_date': news_data_analysis_date,
          'news_data_analysis_count': news_data_analysis_count,
          'news_data_analysis_counter_list': news_data_analysis_counter_list
      })

def maindashboard(request):
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

    return render(request, 'maindashboard.html', {'news_count': obj.Dashboard_Total_News_Count,
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


def twitterraw(request):
    sns_data = Twitter.objects.using('dailydata').all().order_by('-create_dt')
    paginator = Paginator(sns_data, 10)
    page = request.GET.get('page')
    try:
        sns_list = paginator.get_page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        sns_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        sns_list = paginator.page(paginator.num_pages)
    return render(request, 'twitterraw.html', {'sns_list': sns_list})

def instagramraw(request):
    sns_data = Instagram.objects.using('dailydata').all().order_by('-create_dt')
    paginator = Paginator(sns_data, 10)
    page = request.GET.get('page')
    try:
        sns_list = paginator.get_page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        sns_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        sns_list = paginator.page(paginator.num_pages)
    return render(request, 'instagramraw.html', {'sns_list': sns_list})

def dcinsideraw(request):
    sns_data = Dcinside.objects.using('dailydata').all().order_by('-create_dt')
    paginator = Paginator(sns_data, 10)
    page = request.GET.get('page')
    try:
        sns_list = paginator.get_page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        sns_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        sns_list = paginator.page(paginator.num_pages)
    return render(request, 'dcinsideraw.html', {'sns_list': sns_list})

def youtuberaw(request):
    sns_data = Youtube.objects.using('dailydata').all().order_by('-create_dt')
    paginator = Paginator(sns_data, 10)
    page = request.GET.get('page')
    try:
        sns_list = paginator.get_page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        sns_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        sns_list = paginator.page(paginator.num_pages)
    return render(request, 'youtuberaw.html', {'sns_list': sns_list})

def dcinsidedashboard(request):
    sns_data = Dcinside.objects.using('dailydata').all()
    sns_data_map = {}
    sns_data_morphs = {}
    for sns_data_element in sns_data:
        if sns_data_element._id in sns_data_map:
            sns_data_map[sns_data_element._id] = sns_data_map[sns_data_element._id] + sns_data_element.content
        else:
            sns_data_map[sns_data_element._id] = sns_data_element.content
    for key, value in sns_data_map.items():
        target_news_morphs = okt.nouns(value)
        target_news_morphs = [n for n in target_news_morphs if len(n) > 1]
        sns_data_morphs[key] = target_news_morphs
    sns_data_group = Dcinside.objects.using('dailydata').all().values('title', 'category', '_id', 'url').distinct()
    sns_data_list = []
    for sns_data_element in sns_data_group:
        if sns_data_element['_id'] in sns_data_map:
            sns_data_object = {}
            sns_data_object['id'] = sns_data_element['_id']
            sns_data_object['title'] = sns_data_element['title']
            sns_data_object['category'] = sns_data_element['category']
            sns_data_object['url'] = sns_data_element['url']
            sns_data_object['content'] = sns_data_morphs[sns_data_element['_id']]
            sns_data_list.append(sns_data_object)
    paginator = Paginator(sns_data_list, 10)
    page = request.GET.get('page')
    try:
        sns_data_list = paginator.get_page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        sns_data_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        sns_data_list = paginator.page(paginator.num_pages)
    return render(request, 'dcinsidedashboard.html', {'sns_list': sns_data_list})

def instagramdashboard(request):
    sns_data = Instagram.objects.using('dailydata').all()
    sns_data_map = {}
    sns_data_morphs = {}
    for sns_data_element in sns_data:
        if sns_data_element._id in sns_data_map:
            sns_data_map[sns_data_element._id] = sns_data_map[sns_data_element._id] + sns_data_element.content
        else:
            sns_data_map[sns_data_element._id] = sns_data_element.content
    for key, value in sns_data_map.items():
        target_news_morphs = okt.nouns(value)
        target_news_morphs = [n for n in target_news_morphs if len(n) > 1]
        sns_data_morphs[key] = target_news_morphs
    sns_data_group = Instagram.objects.using('dailydata').all().values('title', 'category', '_id', 'url').distinct()
    sns_data_list = []
    for sns_data_element in sns_data_group:
        if sns_data_element['_id'] in sns_data_map:
            sns_data_object = {}
            sns_data_object['id'] = sns_data_element['_id']
            sns_data_object['title'] = sns_data_element['title']
            sns_data_object['category'] = sns_data_element['category']
            sns_data_object['url'] = sns_data_element['url']
            sns_data_object['content'] = sns_data_morphs[sns_data_element['_id']]
            sns_data_list.append(sns_data_object)
    paginator = Paginator(sns_data_list, 10)
    page = request.GET.get('page')
    try:
        sns_data_list = paginator.get_page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        sns_data_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        sns_data_list = paginator.page(paginator.num_pages)
    return render(request, 'instagramdashboard.html', {'sns_list': sns_data_list})

def twitterdashboard(request):
    sns_data = Twitter.objects.using('dailydata').all().order_by('-create_dt')
    paginator = Paginator(sns_data, 10)
    page = request.GET.get('page')
    try:
        sns_list = paginator.get_page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        sns_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        sns_list = paginator.page(paginator.num_pages)
    return render(request, 'bs4sns.html', {'sns_list': sns_list})



def youtubedashboard(request):
    sns_data = Youtube.objects.using('dailydata').all().order_by('-create_dt')
    paginator = Paginator(sns_data, 10)
    page = request.GET.get('page')
    try:
        sns_list = paginator.get_page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        sns_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        sns_list = paginator.page(paginator.num_pages)
    return render(request, 'bs4sns.html', {'sns_list': sns_list})
