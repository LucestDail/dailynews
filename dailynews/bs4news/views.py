import sys
import traceback
from datetime import datetime, timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from konlpy.tag import Okt
from .models import *
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize, sent_tokenize
import time
import requests
import re
from bs4 import BeautifulSoup
import warnings
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import urllib.request
import zipfile
from lxml import etree
from pathlib import Path

warnings.filterwarnings("ignore")
# Create your views here.

def chart(request):
    news_data_all = News.objects.all()
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

    return render(request, 'bs4chart.html', {'news_data': news_data_string})


def graph(request):
    focus_word = '코로나'
    news_data_analysis_date = []
    news_data_analysis_count = []
    for i in range(0, 7):
        check_date = datetime.today() - timedelta(days=i)
        input_date = str(check_date.year) + '-' + str(check_date.month) + '-' + str(check_date.day)
        from_date = datetime.strptime(input_date, '%Y-%m-%d').date()
        from_date = datetime.combine(from_date, datetime.min.time())
        to_date = datetime.combine(from_date, datetime.max.time())
        news_data_date = News_Analysis_Raw.objects.filter(News_CreateDT__range=(from_date, to_date))
        for news_element in news_data_date:
            news_content = [n for n in news_content if n == focus_word]
        news_data_analysis_date.append(input_date)
        news_data_analysis_count.append(len(news_content))
    return render(request, 'bs4graph.html', {'focus_word': focus_word,
                                             'news_data_analysis_date': news_data_analysis_date,
                                             'news_data_analysis_count': news_data_analysis_count
                                             })


def index(request):
    if request.method == 'GET' and 'company' in request.GET:
        News_data = News.objects.filter(News_company=request.GET['company']).order_by('-News_CreateDT')
    else:
        News_data = News.objects.all().order_by('-News_CreateDT')
    paginator = Paginator(News_data, 10)
    page = request.GET.get('page')
    try:
        news_list = paginator.get_page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        news_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        news_list = paginator.page(paginator.num_pages)
    return render(request, 'bs4news.html', {'news_list': news_list})


def scrap(request):
    if request.method == 'GET' and 'company' in request.GET and 'date' in request.GET:
        url = 'https://news.naver.com/main/list.naver?mode=LPOD&mid=sec&oid='+ request.GET['company']\
              + '&listType=title&date=' + request.GET['date']
    elif request.method == 'GET' and 'company' in request.GET:
        url = 'https://news.naver.com/main/list.naver?mode=LPOD&mid=sec&oid='+ request.GET['company']\
              + '&listType=title'
    else:
        url = 'https://news.naver.com/main/list.naver?mode=LPOD&mid=sec&oid=032&listType=title'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            for ulElements in soup.find_all("ul", class_="type02"):
                for href in ulElements.find_all("li"):
                    print(href.find("a")["href"])
                    visiturl = href.find("a")["href"]
                    try:
                        visitResponse = requests.get(visiturl, headers=headers)
                        if response.status_code == 200:
                            try:
                                visitHtml = visitResponse.text
                                visitSoup = BeautifulSoup(visitHtml, 'html.parser')
                                articleTitle = visitSoup.find(class_='media_end_head_headline').text.strip()
                                articleBody = visitSoup.find(id='dic_area').text.strip()
                                articleCompany = url[url.find('oid')+4:url.find('oid')+7]
                                if type(visitSoup.find(class_='byline')) is None:
                                    articleBy = '기자 정보 없음'
                                else:
                                    articleBy = visitSoup.find(class_='byline').text.strip()
                                articleTime = visitSoup.find(class_='media_end_head_info_datestamp_time').text.strip()
                                articleTimeDate = datetime.strptime(articleTime.split()[0],'%Y.%m.%d.')
                                articleTimeAP = articleTime.split()[1]
                                articleTimeHour = datetime.strptime(articleTime.split()[2], '%H:%M')
                                if(articleTimeAP == '오후'):
                                    articleTimeHourConvert = timedelta(hours=12) + articleTimeHour
                                else:
                                    articleTimeHourConvert = articleTimeHour
                                articleTimeHourResult = datetime.strptime(articleTimeHourConvert.strftime("%H:%M"), '%H:%M').time()
                                inputarticleTime = articleTimeDate.strftime('%Y-%m-%d') + ' ' + articleTimeHourResult.strftime('%H:%M:%S')
                                time.sleep(random.uniform(0, 1.0))
                                # News_from
                                # News_title
                                # News_contents
                                # News_CreateDT
                                if(News.objects.filter(
                                    News_from=articleBy,
                                    News_title=articleTitle
                                )):
                                    print('duplicated, next article')
                                else:
                                    news_instance = News(
                                        News_from=articleBy,
                                        News_title=articleTitle,
                                        News_contents=articleBody,
                                        News_CreateDT=inputarticleTime,
                                        News_company=articleCompany
                                    )
                                    news_instance.save()
                                    print('save success')
                            except Exception:
                                pass
                        else:
                            print(visitResponse.status_code)
                            print("end work")
                    except Exception:
                        pass
        else:
            print(response.status_code)
            print("end work")
    except Exception:
        pass


def company(request):
    News_Company_Data = News_Company.objects.all()
    paginator = Paginator(News_Company_Data, 10)
    page = request.GET.get('page')
    try:
        news_company_page_list = paginator.get_page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        news_company_page_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        news_company_page_list = paginator.page(paginator.num_pages)
    return render(request, 'bs4company.html', {'news_company_list': news_company_page_list})


def create_morphs(request):
    if request.method == 'GET' and 'company' in request.GET and 'date' in request.GET:
        target_company = request.GET['company']
        current_datetime = request.GET['date']
    elif request.method == 'GET' and 'company' in request.GET:
        target_company = request.GET['company']
        current_datetime = datetime.now()
    else:
        current_datetime = datetime.now()
        current_minute = current_datetime.minute
        convert_minute_company = str(current_minute).zfill(3)
        # target_company = convert_minute_company
        target_company = '032'
    print('django bs4news news_analysis_create_morphs crontab started -------------------')
    # current_datetime = datetime.now()
    # current_minute = current_datetime.minute
    # convert_minute_company = str(current_minute).zfill(3)
    # target_company = convert_minute_company
    okt = Okt()
    from_date = current_datetime - timedelta(days=1)
    to_date = current_datetime
    target_news_data = News.objects.filter(News_company=target_company, News_CreateDT__range=(from_date, to_date))
    print('target data count===')
    print(len(target_news_data))
    target = 0
    success = 0
    fail = 0
    for target_news_element in target_news_data:
        excluded_word_data = BS4_NEWS_ANALYSIS_WORD_EXCLUDED.objects.filter(COMPANY_CODE=target_news_element.News_company)
        excluded_word_list = []
        if len(excluded_word_data) > 0:
            for excluded_word_data_element in excluded_word_data:
                excluded_word_list.append(excluded_word_data_element.EXCLUDED_WORD)
        target_news_morphs = okt.nouns(target_news_element.News_contents)
        target_news_morphs = [n for n in target_news_morphs if len(n) > 1]
        save_morphs = ''
        count = 0
        target += 1
        for morphs_element in target_news_morphs:
            if morphs_element not in excluded_word_list:
                save_morphs += morphs_element
                count += 1
                if count < len(target_news_morphs):
                    save_morphs += ","
        if (News_Analysis_Raw.objects.filter(
                News_Analysis_From=target_news_element.News_from,
                News_Analysis_Title=target_news_element.News_title,
                News_Analysis_Company=target_news_element.News_company
        )):
            fail += 1
        else:
            news_analysis_morphs = News_Analysis_Raw(
                News_Analysis_Company=target_news_element.News_company,
                News_Analysis_Title=target_news_element.News_title,
                News_Analysis_From=target_news_element.News_from,
                News_Morphs=save_morphs,
                News_Analysis_CreateDT=target_news_element.News_CreateDT,
            )
            news_analysis_morphs.save()
            success += 1
    print('====== analysis result ======')
    print(' | count')
    print(target)
    print(' | success')
    print(success)
    print(' | fail (maybe duplicate)')
    print(fail)
    print('django bs4news news_analysis_create_morphs crontab ended -------------------')


def index_morphs(request):
    if request.method == 'GET' and 'company' in request.GET and 'date' in request.GET:
        target_company = request.GET['company']
        current_datetime = request.GET['date']
    elif request.method == 'GET' and 'company' in request.GET:
        target_company = request.GET['company']
        current_datetime = datetime.now()
    else:
        current_datetime = datetime.now()
        # current_minute = current_datetime.minute
        # convert_minute_company = str(current_minute).zfill(3)
        # target_company = convert_minute_company
        target_company = '032'
    print('django bs4news news_analysis_every_hour crontab started -------------------')
    format = '%Y%m%d'
    target_date = datetime.strftime(current_datetime, format)
    # check_date = current_datetime - timedelta(hours=12)
    # input_date = str(check_date.year) + '-' + str(check_date.month) + '-' + str(check_date.day)
    from_date = current_datetime - timedelta(hours=1)
    to_date = current_datetime
    print(target_company)
    print(target_date)
    print(from_date)
    print(to_date)
    target_news_data = News_Analysis_Raw.objects.filter(News_Analysis_Company=target_company)
    for target_news_element in target_news_data:
        target_contents = target_news_element.News_Morphs.split(',')
        print(target_contents)


def word2vec(request):
    print('word2vce started -------------------')
    if request.method == 'GET' and 'word' in request.GET and 'date' in request.GET:
        target_word = request.GET['word']
        current_datetime = request.GET['date']
    elif request.method == 'GET' and 'word' in request.GET:
        target_company = request.GET['word']
        current_datetime = datetime.now()
    else:
        target_word = '경향신문'
        current_datetime = datetime.now()
    target_company = '032'
    input_date = str(current_datetime.year) + '-' + str(current_datetime.month) + '-' + str(current_datetime.day)
    from_date = datetime.strptime(input_date, '%Y-%m-%d').date()
    from_date = datetime.combine(from_date, datetime.min.time())
    to_date = datetime.combine(from_date, datetime.max.time())
    target_news_data = News_Analysis_Raw.objects.filter(News_Analysis_CreateDT__range=(from_date, to_date),
                                                        News_Analysis_Company=target_company)
    target_news_sentences = News.objects.filter(News_CreateDT__range=(from_date, to_date), News_company=target_company)
    # for target_news_element in target_news_data:
    #     print(target_news_element)
    #     sent_text = sent_tokenize(target_news_element)
    #     print(sent_text)
    #     normalized_text = []
    #     normalized_text.append(sent_text)
    #     print(normalized_text)
    #     result = [word_tokenize(sentence) for sentence in normalized_text]
    #     model = Word2Vec(sentences=result, size=100, window=5, min_count=5, workers=4, sg=0)
    #     # 임베딩 벡터 차원
    #     # window : 윈도우 크기
    #     # mincont : 최소 5번 이상 등장한 단어
    #     # sg = 0 : CBOW
    #     # sg = 1 : skip - grows
    #     model_result = model.wv.most_similar(target_word)
    #     print(model_result)
    for target_news_sentences_element in target_news_sentences:
        print('news for start ================================')
        content_text = target_news_sentences_element.News_contents
        print(content_text)
        # 입력 코퍼스에 대해서 NLTK를 이용하여 문장 토큰화를 수행.
        sent_text = sent_tokenize(content_text)
        # 각 문장에 대해서 구두점을 제거하고, 대문자를 소문자로 변환.
        normalized_text = []
        for string in sent_text:
            normalized_text.append(string)
        # 각 문장에 대해서 NLTK를 이용하여 단어 토큰화를 수행.
        result = [word_tokenize(sentence) for sentence in normalized_text]
        print('총 샘플의 개수 : {}'.format(len(result)))
        for line in result[:3]:
            print(line)
        df = pd.DataFrame(result)
        model = Word2Vec(map(eval, df['corpus'].values), sg=1, window=5, min_count=1, workers=4, iter=100)
        model_result1 = model.wv.most_similar("정부")
        model_result = model.wv.most_similar(target_word)
        print(model_result)
        print('news for ended ================================')
    print('word2vce ended -------------------')
    return render(request, 'bs4news.html', {'news_list': target_news_sentences})


def bs4scrap(request):
    if request.method == 'GET' and 'company' in request.GET and 'url' in request.GET:
        url = request.GET['url']
        company_code = request.GET['company']
    else:
        url = 'www.khan.co.kr/newest/articles'
        company_code = '032'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            for ulElements in soup.find_all("ul", class_="type02"):
                for href in ulElements.find_all("li"):
                    print(href.find("a")["href"])
                    visiturl = href.find("a")["href"]
                    try:
                        visitResponse = requests.get(visiturl, headers=headers)
                        if response.status_code == 200:
                            try:
                                visitHtml = visitResponse.text
                                visitSoup = BeautifulSoup(visitHtml, 'html.parser')
                                articleTitle = visitSoup.find(class_='media_end_head_headline').text.strip()
                                articleBody = visitSoup.find(id='dic_area').text.strip()
                                articleCompany = url[url.find('oid')+4:url.find('oid')+7]
                                if type(visitSoup.find(class_='byline')) is None:
                                    articleBy = '기자 정보 없음'
                                else:
                                    articleBy = visitSoup.find(class_='byline').text.strip()
                                articleTime = visitSoup.find(class_='media_end_head_info_datestamp_time').text.strip()
                                articleTimeDate = datetime.strptime(articleTime.split()[0],'%Y.%m.%d.')
                                articleTimeAP = articleTime.split()[1]
                                articleTimeHour = datetime.strptime(articleTime.split()[2], '%H:%M')
                                if(articleTimeAP == '오후'):
                                    articleTimeHourConvert = timedelta(hours=12) + articleTimeHour
                                else:
                                    articleTimeHourConvert = articleTimeHour
                                articleTimeHourResult = datetime.strptime(articleTimeHourConvert.strftime("%H:%M"), '%H:%M').time()
                                inputarticleTime = articleTimeDate.strftime('%Y-%m-%d') + ' ' + articleTimeHourResult.strftime('%H:%M:%S')
                                time.sleep(5)
                                # News_from
                                # News_title
                                # News_contents
                                # News_CreateDT
                                if(News.objects.filter(
                                    News_from=articleBy,
                                    News_title=articleTitle
                                )):
                                    print('duplicated, next article')
                                else:
                                    news_instance = News(
                                        News_from=articleBy,
                                        News_title=articleTitle,
                                        News_contents=articleBody,
                                        News_CreateDT=inputarticleTime,
                                        News_company=articleCompany
                                    )
                                    news_instance.save()
                                    print('save success')
                            except Exception:
                                pass
                        else:
                            print(visitResponse.status_code)
                            print("end work")
                    except Exception:
                        pass
        else:
            print(response.status_code)
            print("end work")
    except Exception:
        pass


def bs4crawl(request):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                      "AppleWebKit/537.36 (KHTML, like Gecko)"
                      "Chrome/87.0.4280.88 Safari/537.36"
    }
    browser = webdriver.Chrome(str(Path(__file__).resolve().parent.parent) + '/webdriver/chromedriver_mac')
    browser.implicitly_wait(time_to_wait=5)
    bs4_news_company_list = BS4_NEWS_COMPANY.objects.all()
    input_date = str(datetime.now().year) + '-'\
                 + str(datetime.now().month) + '-'\
                 + str(datetime.now().day) + " "\
                 + str(datetime.now().hour) + ":"\
                 + str(datetime.now().minute) + ":"\
                 + str(datetime.now().second)
    from_date = datetime.strptime(input_date, '%Y-%m-%d %H:%M:%S')
    print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> JOB START")
    for bs4_news_company_element in bs4_news_company_list:
        target_company_code = bs4_news_company_element.COMPANY_CODE
        bs4_news_company_crawl_list = BS4_NEWS_COMPANY_CRAWL.objects.filter(COMPANY_CODE=target_company_code)
        print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> current target company : " + target_company_code)
        for bs4_news_company_crawl_element in bs4_news_company_crawl_list:
            target_url = bs4_news_company_crawl_element.DOMAIN_URL + bs4_news_company_crawl_element.DOMAIN_QUERY_STRING
            browser.get(target_url)
            bs4_news_company_crawl_link_xpath = bs4_news_company_crawl_element.CRAWL_LINK_TARGET
            print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> current target url : " + target_url)
            print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> search target : "
                  + bs4_news_company_crawl_link_xpath)
            print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> request proceeding...")
            try:
                target_list_group = browser.find_element(by=By.XPATH,
                                                         value=bs4_news_company_crawl_element.CRAWL_LINK_TARGET)
                print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> accessing list collect start")
                element_link_set = {find_target_element.get_attribute('href')
                                for find_target_element
                                in target_list_group.find_elements_by_tag_name("a")}
                crawl_count = len(element_link_set)
                crawl_success = 0
                crawl_fail = 0
                print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> accessing list count : " + str(len(element_link_set)))
                print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> accessing list collect end")
                for element_link_set_element in element_link_set:
                    print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> current access target_url : "
                          + element_link_set_element)
                    print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> request proceeding...")
                    try:
                        response = requests.get(element_link_set_element, headers=headers)
                        if response.status_code == 200:
                            html = response.text
                            if (BS4_NEWS_COMPANY_CRAWL_DATA.objects.filter(
                                    COMPANY_CODE=target_company_code,
                                    TARGET_CRAWL_URL=element_link_set_element
                            )):
                                print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> duplicated, next article")
                            else:
                                BS4_NEWS_COMPANY_CRAWL_DATA_INPUT = BS4_NEWS_COMPANY_CRAWL_DATA(
                                    COMPANY_CODE=target_company_code,
                                    DOMAIN_URL=bs4_news_company_crawl_element.DOMAIN_URL,
                                    DOMAIN_QUERY_STRING=bs4_news_company_crawl_element.DOMAIN_QUERY_STRING,
                                    TARGET_CRAWL_URL=element_link_set_element,
                                    TARGET_RAW_HTML_DATA=html,
                                    UPDATE_DATETIME=datetime.now(),
                                    UPDATE_USER='SYSTEM',
                                    CREATE_DATETIME=datetime.now(),
                                    CREATE_USER='SYSTEM',
                                    DESCRIPTION_INFO='NONE',
                                )
                                crawl_success += 1
                                BS4_NEWS_COMPANY_CRAWL_DATA_INPUT.save()
                                print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> save success")
                        else:
                            print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> response Error Code : "
                                  + response.status_code)
                        time.sleep(random.uniform(0, 1.0))
                    except Exception:
                        BS4_NEWS_COMPANY_CRAWL_DATA_INPUT = BS4_NEWS_COMPANY_CRAWL_DATA(
                            COMPANY_CODE=target_company_code,
                            DOMAIN_URL=bs4_news_company_crawl_element.DOMAIN_URL,
                            DOMAIN_QUERY_STRING=bs4_news_company_crawl_element.DOMAIN_QUERY_STRING,
                            TARGET_CRAWL_URL=element_link_set_element,
                            TARGET_RAW_HTML_DATA=str(traceback.format_exc()),
                            UPDATE_DATETIME=datetime.now(),
                            UPDATE_USER='SYSTEM_ERROR',
                            CREATE_DATETIME=datetime.now(),
                            CREATE_USER='SYSTEM_ERROR',
                            DESCRIPTION_INFO='NONE',
                        )
                        crawl_fail += 1
                        BS4_NEWS_COMPANY_CRAWL_DATA_INPUT.save()
                        print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> response Exception")
                        pass

                BS4_NEWS_COMPANY_CRAWL_RESULT_INPUT = BS4_NEWS_COMPANY_CRAWL_RESULT(
                    COMPANY_CODE=target_company_code,
                    DOMAIN_URL=bs4_news_company_crawl_element.DOMAIN_URL,
                    DOMAIN_QUERY_STRING=bs4_news_company_crawl_element.DOMAIN_QUERY_STRING,
                    EXECUTE_DATE=datetime.now(),
                    EXECUTE_RESULT_COUNT=str(crawl_count),
                    EXECUTE_RESULT_FAIL=str(crawl_fail),
                    EXECUTE_RESULT_SUCCESS=str(crawl_success),
                    EXECUTE_RESULT='END',
                    UPDATE_DATETIME=datetime.now(),
                    UPDATE_USER='SYSTEM',
                    CREATE_DATETIME=datetime.now(),
                    CREATE_USER='SYSTEM',
                    DESCRIPTION_INFO='NONE',
                )
                BS4_NEWS_COMPANY_CRAWL_RESULT_INPUT.save()

            except Exception:
                print(traceback.format_exc())
                print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> request Exception")
                pass
        print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> close target company : " + target_company_code)
    print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> JOB END")
    browser.close()
    input_date = str(datetime.now().year) + '-' \
                 + str(datetime.now().month) + '-' \
                 + str(datetime.now().day) + " " \
                 + str(datetime.now().hour) + ":" \
                 + str(datetime.now().minute) + ":" \
                 + str(datetime.now().second)
    to_date = datetime.strptime(input_date, '%Y-%m-%d %H:%M:%S')
    # news_list = {}
    news_list = BS4_NEWS_COMPANY_CRAWL_DATA.objects.filter(
        CREATE_DATETIME__range=(from_date, to_date),
    )
    return render(request, 'bs4newst.html', {'news_list': news_list})