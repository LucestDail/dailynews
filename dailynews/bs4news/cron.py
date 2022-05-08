import traceback
from datetime import datetime, timedelta
from .models import *
from konlpy.tag import Okt
import time
import requests
from bs4 import BeautifulSoup
import warnings
from collections import Counter
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from pathlib import Path
warnings.filterwarnings("ignore")


def scrap():
    print('django bs4news scrap crontab started -------------------')
    news_company = News_Company.objects.all()
    for current_job_target_company in news_company:
        current_job_target_company_code = current_job_target_company.News_Company_Code
        print('current step =====================================')
        print(current_job_target_company_code)
        print('job start ========================================')
        print(datetime.now())
        print('job started =====================================>')
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
                                print('pass 2')
                                print('scrap start ========================================')
                                print(datetime.now())
                                print('scrap started =====================================>')
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
                                        print('scrap end ========================================')
                                        print(datetime.now())
                                        print('scrap ended =====================================>')
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
                                        print('scrap end ========================================')
                                        print(datetime.now())
                                        print('scrap ended =====================================>')
                                except Exception as e:
                                    trace_back = traceback.format_exc()
                                    message = str(e) + "\n" + str(trace_back)
                                    print(e)
                                    print('Exception core')
                                    pass
                            else:
                                print(visitResponse.status_code)
                                print("end work")
                                print('job end ========================================')
                                print(datetime.now())
                                print('job ended =====================================>')
                        except Exception:
                            print(Exception)
                            print('exception from inner loop')
                            print('job end ========================================')
                            print(datetime.now())
                            print('job ended =====================================>')
                            pass
            else:
                print(response.status_code)
                print("end work, Job finished =============================")
                print('job end ========================================')
                print(datetime.now())
                print('job ended =====================================>')
        except Exception:
            print(Exception)
            print('exception from outer loop')
            print('job end ========================================')
            print(datetime.now())
            print('job ended =====================================>')
            pass
        print('total end ========================================')
        print(datetime.now())
        print('total ended =====================================>')
    print('django bs4news scrap crontab ended -------------------')


def news_analysis_create_morphs():
    print('django bs4news news_analysis_create_morphs crontab started -------------------')
    news_company = News_Company.objects.all()
    for current_job_target_company in news_company:
        current_job_target_company_code = current_job_target_company.News_Company_Code
        print('current step =====================================')
        print(current_job_target_company_code)
        print('job start ========================================')
        print(datetime.now())
        print('job started =====================================>')
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
            target += 1
            if (News_Analysis_Raw.objects.filter(
                    News_Analysis_From=target_news_element.News_from,
                    News_Analysis_Title=target_news_element.News_title,
                    News_Analysis_Company=target_news_element.News_company
            )):
                fail += 1
            else:
                excluded_word_data = BS4_NEWS_ANALYSIS_WORD_EXCLUDED.objects.filter(
                    COMPANY_CODE=target_news_element.News_company)
                excluded_word_list = []
                if len(excluded_word_data) > 0:
                    for excluded_word_data_element in excluded_word_data:
                        excluded_word_list.append(excluded_word_data_element.EXCLUDED_WORD)
                target_news_morphs = okt.nouns(target_news_element.News_contents)
                target_news_morphs = [n for n in target_news_morphs if len(n) > 1]
                save_morphs = ''
                count = 0
                for morphs_element in target_news_morphs:
                    if morphs_element not in excluded_word_list:
                        save_morphs += morphs_element
                        count += 1
                        if count < len(target_news_morphs):
                            save_morphs += ","
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
        print('job end ========================================')
        print(datetime.now())
        print('job ended =====================================>')
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

        if(News_Analysis_Count_Company.objects.filter(News_Analysis_Count_Company_Code=target_company,
                                                      News_Analysis_Count_Company_CreateDT__range=(from_date, to_date))):
            fail += 1
            target += 1
        else:
            target_news_data = News_Analysis_Raw.objects.filter(News_Analysis_CreateDT__range=(from_date, to_date),
                                                                News_Analysis_Company=target_company).count()
            target_company_count = str(target_news_data)
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
            target_news_data = News_Analysis_Raw.objects.filter(News_Analysis_CreateDT__range=(from_date, to_date),
                                                                News_Analysis_Company=target_company)
            target_temp_save = []
            for target_data_element in target_news_data:
                target_news_content = target_data_element.News_Morphs.split(',')
                for target_news_data_morphs_element in target_news_content:
                    target_temp_save.append(target_news_data_morphs_element)
            target_result = Counter(target_temp_save)
            target_most_word_50 = target_result.most_common(50)
            target_news_data_analysis_jsonStr = ''
            for target_most_word_50_element in target_most_word_50:
                target_news_data_analysis_jsonStr += '{"tag":"'
                target_news_data_analysis_jsonStr += str(target_most_word_50_element[0])
                target_news_data_analysis_jsonStr += '",'
                target_news_data_analysis_jsonStr += '"weight":'
                target_news_data_analysis_jsonStr += str(target_most_word_50_element[1])
                target_news_data_analysis_jsonStr += '},'
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
        print('job end ========================================')
        print(datetime.now())
        print('job ended =====================================>')
    print('django bs4news news_analysis_create_news_dashboard_data crontab ended -------------------')


def news_crawl_bia_selenium_every_hour():
    print('django bs4news news_analysis_create_news_dashboard_data crontab started -------------------')
    print('CRON START ========================================')
    print(datetime.now())
    print('CRON START =====================================>')
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                      "AppleWebKit/537.36 (KHTML, like Gecko)"
                      "Chrome/87.0.4280.88 Safari/537.36"
    }
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # browser = webdriver.Chrome(str(Path(__file__).resolve().parent.parent)+ '/webdriver/chromedriver_mac', chrome_options=chrome_options)
    browser = webdriver.Chrome(str(Path(__file__).resolve().parent.parent)+ '/webdriver/chromedriver_linux', chrome_options=chrome_options)
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
    print('CRON END ========================================')
    print(datetime.now())
    print('CRON END =====================================>')
    print('django bs4news news_analysis_create_news_dashboard_data crontab started -------------------')