import traceback
from datetime import datetime, timedelta
from .models import News, News_Analysis_Raw
from konlpy.tag import Okt
import time
import requests
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore")


def scrap_every_minute():
    print('django bs4news crontab started -------------------')
    current_datetime = datetime.now()
    format = '%Y%m%d'
    current_minute = datetime.now().minute
    convert_minute_company = str(current_minute).zfill(3)
    target_date = datetime.strftime(current_datetime, format)
    target_company = convert_minute_company
    print(target_company)
    print(target_date)
    url = 'https://news.naver.com/main/list.naver?mode=LPOD&mid=sec&oid=' + \
          target_company + \
          '&listType=title&date=' + \
          target_date
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print('pass 1')
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            for ulElements in soup.find_all("ul", class_="type02"):
                for href in ulElements.find_all("li"):
                    print(href.find("a")["href"])
                    visiturl = href.find("a")["href"]
                    try:
                        visitResponse = requests.get(visiturl, headers=headers)
                        if response.status_code == 200:
                            print('pass 1')
                            try:
                                visitHtml = visitResponse.text
                                visitSoup = BeautifulSoup(visitHtml, 'html.parser')
                                articleTitle = visitSoup.find(id='articleTitle').text.strip()
                                articleBody = visitSoup.find(id='articleBodyContents').text.strip()
                                articleCompany = url[url.find('oid') + 4:url.find('oid') + 7]
                                if type(visitSoup.find(class_='byline')) is None:
                                    articleBy = '기자 정보 없음'
                                else:
                                    articleBy = visitSoup.find(class_='byline').text.strip()
                                articleTime = visitSoup.find(class_='t11').text.strip()
                                articleTimeDate = datetime.strptime(articleTime.split()[0], '%Y.%m.%d.')
                                articleTimeAP = articleTime.split()[1]
                                articleTimeHour = datetime.strptime(articleTime.split()[2], '%H:%M')
                                if (articleTimeAP == '오후'):
                                    articleTimeHourConvert = timedelta(hours=12) + articleTimeHour
                                else:
                                    articleTimeHourConvert = articleTimeHour
                                articleTimeHourResult = datetime.strptime(articleTimeHourConvert.strftime("%H:%M"),
                                                                          '%H:%M').time()
                                inputarticleTime = articleTimeDate.strftime(
                                    '%Y-%m-%d') + ' ' + articleTimeHourResult.strftime('%H:%M:%S')
                                time.sleep(5)
                                # News_from
                                # News_title
                                # News_contents
                                # News_CreateDT
                                if (News.objects.filter(
                                        News_from=articleBy,
                                        News_title=articleTitle,
                                        News_company=articleCompany
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

                            except Exception as e:
                                trace_back = traceback.format_exc()
                                message = str(e) + "\n" + str(trace_back)
                                print(e)
                                print('Exception core')
                                pass
                        else:
                            print(visitResponse.status_code)
                            print("end work")
                    except Exception:
                        print(Exception)
                        print('exception from inner loop')
                        pass
        else:
            print(response.status_code)
            print("end work, Job finished =============================")
    except Exception:
        print(Exception)
        print('exception from outer loop')
        pass
    print('django bs4news crontab ended -------------------')


def news_analysis_create_morphs():
    print('django bs4news news_analysis_create_morphs crontab started -------------------')
    current_datetime = datetime.now()
    current_minute = current_datetime.minute
    convert_minute_company = str(current_minute).zfill(3)
    target_company = convert_minute_company
    okt = Okt()
    from_date = current_datetime - timedelta(days=1)
    to_date = current_datetime
    target_news_data = News.objects.filter(News_CreateDT__range=(from_date, to_date), News_Company=target_company)
    for target_news_element in target_news_data:
        target_news_morphs = okt.nouns(target_news_element.News_contents)
        target_news_morphs = [n for n in target_news_morphs if len(n) > 1]
        save_morphs = ''
        count = 0
        success = 0
        fail = 0
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
        print(count + " / " + success + " / " + fail)
    print('django bs4news news_analysis_create_morphs crontab ended -------------------')