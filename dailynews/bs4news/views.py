from datetime import datetime, timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from konlpy.tag import Okt
from .models import News, News_Company, News_Analysis_Raw
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize, sent_tokenize
import time
import requests
import re
from bs4 import BeautifulSoup
import warnings
import pandas as pd

import urllib.request
import zipfile
from lxml import etree

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
    from_date = current_datetime - timedelta(days=15)
    to_date = current_datetime
    target_news_data = News.objects.filter(News_CreateDT__range=(from_date, to_date))
    print('target data count===')
    print(len(target_news_data))
    target = 0
    success = 0
    fail = 0
    for target_news_element in target_news_data:
        target_news_morphs = okt.nouns(target_news_element.News_contents)
        target_news_morphs = [n for n in target_news_morphs if len(n) > 1]
        save_morphs = ''
        count = 0
        target += 1
        for morphs_element in target_news_morphs:
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