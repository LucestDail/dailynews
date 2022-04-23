import traceback
from datetime import datetime, timedelta
from .models import News, News_Analysis_Raw, News_Company, News_Analysis_Count_Company, News_Analysis_Word_Analysis_Company
from konlpy.tag import Okt
import time
import requests
from bs4 import BeautifulSoup
import warnings
from collections import Counter
import random
warnings.filterwarnings("ignore")


def scrap():
    print('django bs4news scrap crontab started -------------------')
    news_company = News_Company.objects.all()
    for current_job_target_company in news_company:
        current_job_target_company_code = current_job_target_company.News_Company_Code
        print('current step =====================================')
        print(current_job_target_company_code)
        current_datetime = datetime.now()
        format = '%Y%m%d'
        target_date = datetime.strftime(current_datetime, format)
        target_company = current_job_target_company_code
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
                                    articleTitle = visitSoup.find(class_='media_end_head_headline').text.strip()
                                    articleBody = visitSoup.find(id='dic_area').text.strip()
                                    articleCompany = url[url.find('oid') + 4:url.find('oid') + 7]
                                    if type(visitSoup.find(class_='byline')) is None:
                                        articleBy = '기자 정보 없음'
                                    else:
                                        articleBy = visitSoup.find(class_='byline').text.strip()
                                    articleTime = visitSoup.find(
                                        class_='media_end_head_info_datestamp_time').text.strip()
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
                                    time.sleep(random.uniform(0, 1.0))
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
        print('current step =====================================')
    print('django bs4news scrap crontab ended -------------------')


def news_analysis_create_morphs():
    print('django bs4news news_analysis_create_morphs crontab started -------------------')
    news_company = News_Company.objects.all()
    for current_job_target_company in news_company:
        current_job_target_company_code = current_job_target_company.News_Company_Code
        print('current step =====================================')
        print(current_job_target_company_code)
        current_datetime = datetime.now()
        target_company = current_job_target_company_code
        okt = Okt()
        from_date = current_datetime - timedelta(days=1)
        to_date = current_datetime
        target_news_data = News.objects.filter(News_CreateDT__range=(from_date, to_date), News_company=target_company)
        print('====== target data count ======')
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


def news_analysis_create_news_dashboard_data():
    print('django bs4news news_analysis_create_news_dashboard_data crontab started -------------------')
    news_company = News_Company.objects.all()
    for current_job_target_company in news_company:
        current_job_target_company_code = current_job_target_company.News_Company_Code
        print('current step =====================================')
        print(current_job_target_company_code)
        print('job start ========================================')
        print(datetime.now())
        print('job started =====================================>')
        target = 0
        success = 0
        fail = 0

        current_datetime = datetime.now()
        target_company = current_job_target_company_code

        check_date = datetime.today() - timedelta(days=1)
        input_date = str(check_date.year) + '-' + str(check_date.month) + '-' + str(check_date.day)
        from_date = datetime.strptime(input_date, '%Y-%m-%d').date()
        from_date = datetime.combine(from_date, datetime.min.time())
        to_date = datetime.combine(from_date, datetime.max.time())
        target_news_data = News_Analysis_Raw.objects.filter(News_Analysis_CreateDT__range=(from_date, to_date),
                                                            News_Analysis_Company=target_company)

        target_news_data_analysis_jsonStr = ''
        target_company_count = len(target_news_data)

        target_temp_save = []
        for target_data_element in target_news_data:
            target_news_content = target_data_element.News_Morphs.split(',')
            for target_news_data_morphs_element in target_news_content:
                target_temp_save.append(target_news_data_morphs_element)
        target_result = Counter(target_temp_save)
        target_most_word_50 = target_result.most_common(50)

        for target_most_word_50_element in target_most_word_50:
            target_news_data_analysis_jsonStr += '{"tag":"'
            target_news_data_analysis_jsonStr += str(target_most_word_50_element[0])
            target_news_data_analysis_jsonStr += '",'
            target_news_data_analysis_jsonStr += '"weight":'
            target_news_data_analysis_jsonStr += str(target_most_word_50_element[1])
            target_news_data_analysis_jsonStr += '},'

        News_Analysis_Count_Company, News_Analysis_Word_Analysis_Company
        if(News_Analysis_Count_Company.objects.filter(News_Analysis_Count_Company_Code=target_company,
                                                      News_Analysis_Count_Company_CreateDT__range=(from_date, to_date))):
            fail += 1
            target += 1
        else:
            News_Analysis_Count_Company_Input = News_Analysis_Count_Company(
                News_Analysis_Count_Company_Code=target_company,
                News_Analysis_Count_Company_CreateDT=from_date,
                News_Analysis_Count_Company_UpdateDT=current_datetime,
                News_Analysis_Count_Company_Count=target_company_count
            )
            News_Analysis_Count_Company_Input.save()
            success += 1
            target += 1

        if (News_Analysis_Word_Analysis_Company.objects.filter(News_Analysis_Word_Analysis_Company_Code=target_company,
                                            News_Analysis_Word_Analysis_Company_CreateDT__range=(from_date, to_date))):
            fail += 1
            target += 1
        else:
            News_Analysis_Word_Analysis_Company_Input = News_Analysis_Word_Analysis_Company(
                News_Analysis_Word_Analysis_Company_Code=target_company,
                News_Analysis_Word_Analysis_Company_CreateDT=from_date,
                News_Analysis_Word_Analysis_Company_UpdateDT=current_datetime,
                News_Analysis_Word_Analysis_Company_Data=target_news_data_analysis_jsonStr
            )
            News_Analysis_Word_Analysis_Company_Input.save()
            success += 1
            target += 1

        print('====== analysis result ======')
        print(' | count (should be 2)')
        print(target)
        print(' | success (2 : all success, 1 : something duplicated, 0 : all duplicated)')
        print(success)
        print(' | fail (maybe duplicate)')
        print(fail)
    print('django bs4news news_analysis_create_news_dashboard_data crontab ended -------------------')