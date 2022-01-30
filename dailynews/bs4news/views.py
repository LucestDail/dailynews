from datetime import datetime, timedelta

from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.db.models import Q
from .models import News
import time
import requests
from bs4 import BeautifulSoup
# Create your views here.

def index(request):
    news_list = News.objects.order_by('-News_CreateDT')[:100]
    template = loader.get_template('bs4news.html')
    context = {
        'news_list': news_list,
    }
    return HttpResponse(template.render(context, request))


def scrap(request):
    url = 'https://news.naver.com/main/list.naver?mode=LPOD&mid=sec&oid=032&listType=title&date=20220130'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        for ulElements in soup.find_all("ul", class_="type02"):
            for href in ulElements.find_all("li"):
                print(href.find("a")["href"])
                visiturl = href.find("a")["href"]
                visitResponse = requests.get(visiturl, headers=headers)
                if response.status_code == 200:
                    visitHtml = visitResponse.text
                    visitSoup = BeautifulSoup(visitHtml, 'html.parser')
                    articleTitle = visitSoup.find(id='articleTitle').text.strip()
                    articleBody = visitSoup.find(id='articleBodyContents').text.strip()
                    articleBy = visitSoup.find(class_='byline').text.strip()
                    articleTime = visitSoup.find(class_='t11').text.strip()
                    articleTimeDate = datetime.strptime(articleTime.split()[0],'%Y.%m.%d.')
                    articleTimeAP = articleTime.split()[1]
                    articleTimeHour = datetime.strptime(articleTime.split()[2], '%H:%M')
                    articleTimeHourConvert = ''
                    if(articleTimeAP == '오후'):
                        articleTimeHourConvert = timedelta(hours=12) + articleTimeHour
                    else:
                        articleTimeHourConvert = articleTimeHour
                    #articleTimeConvert = articleTimeDate.stripTime() + ' ' + articleTimeHourConvert.strptime()
                    articleTimeHourResult = datetime.strptime(articleTimeHourConvert.strftime("%H:%M"), '%H:%M').time()
                    print(articleTimeDate)
                    print(articleTimeHourResult)
                    inputarticleTime = articleTimeDate.strftime('%Y-%m-%d') + ' ' +  articleTimeHourResult.strftime('%H:%M:%S')
                    print(inputarticleTime)
                    print(articleTitle)
                    print(articleBody)
                    print(articleBy)
                    #print(articleTimeConvert.time())
                    time.sleep(5)
                    # News_from
                    # News_title
                    # News_contents
                    # News_CreateDT
                #     if(News.objects.filter(
                #         News_from=articleBy,
                #         News_title=articleTitle
                #     )):
                #         print('duplicated, next article')
                #     else:
                #         news_instance = News(
                #             News_from=articleBy,
                #             News_title=articleTitle,
                #             News_contents=articleBody,
                #             News_CreateDT=inputarticleTime
                #         )
                #         news_instance.save()
                # else:
                #     print(visitResponse.status_code)
    else:
        print(response.status_code)