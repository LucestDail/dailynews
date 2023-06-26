import mysql.connector as database
from datetime import datetime, timedelta
import traceback
from bs4 import BeautifulSoup
import requests
import time
import random


connection = database.connect(
    user="admin",
    password="admin1234",
    host="192.168.11.21",
    database="mytools",
    port="3306")
# connection = database.connect(
#     user="admin",
#     password="admin1234",
#     host="180.70.85.89",
#     database="mytools",
#     port="8050")
cursor = connection.cursor()


def get_all_company_code():
    print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> GET ALL COMPANY CODE -> SELECT START")
    try:
        statement = "SELECT News_Company_Code FROM bs4news_news_company"
        cursor.execute(statement)
        print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> GET ALL COMPANY CODE -> SELECT SUCCESS")
    except Exception as e:
        print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> GET ALL COMPANY CODE -> SELECT FAIL")
        print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> GET ALL COMPANY CODE -> SELECT EXCEPTION STACK TRACE START")
        add_news_trace_back = traceback.format_exc()
        add_news_trace_back_message = str(e) + "\n" + str(add_news_trace_back)
        print(add_news_trace_back_message)
        print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> GET ALL COMPANY CODE -> SELECT EXCEPTION STACK TRACE END")
    print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> GET ALL COMPANY CODE -> SELECT END")
    return list(cursor.fetchall())


def check_news(news_link, news_company):
    print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> CHECK NEWS -> SELECT START")
    is_exist_news = False
    try:
        statement = "SELECT * FROM bs4news_news WHERE ETC1 = %s AND News_company = %s"
        data = (news_link, news_company)
        cursor.execute(statement, data)
        if len(cursor.fetchall()) > 0:
            is_exist_news = True
        print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> CHECK NEWS -> SELECT SUCCESS -> EXIST : " + str(is_exist_news))
    except Exception as e:
        print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> CHECK NEWS -> SELECT FAIL")
        print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> CHECK NEWS -> SELECT EXCEPTION STACK TRACE START")
        add_news_trace_back = traceback.format_exc()
        add_news_trace_back_message = str(e) + "\n" + str(add_news_trace_back)
        print(add_news_trace_back_message)
        print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> CHECK NEWS -> SELECT EXCEPTION STACK TRACE END")
        pass
    return is_exist_news


def add_news(News_from,News_title,News_Company,News_contents,News_CreateDT,ETC1,ETC2,ETC3,ETC4,ETC5,News_contents_raw):
    print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> ARTICLE SAVE -> INSERT START")
    try:
        statement = "INSERT INTO bs4news_news (News_from,News_title,News_company,News_contents,News_CreateDT,ETC1,ETC2,ETC3,ETC4,ETC5,News_contents_raw) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        data = (News_from, News_title, News_Company, News_contents, News_CreateDT, ETC1, ETC2, ETC3, ETC4, ETC5, News_contents_raw)
        cursor.execute(statement, data)
        connection.commit()
        print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> ARTICLE SAVE -> INSERT SUCCESS")
    except Exception as e:
        print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> ARTICLE SAVE -> INSERT FAIL")
        print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> ARTICLE SAVE -> EXCEPTION STACK TRACE START")
        add_news_trace_back = traceback.format_exc()
        add_news_trace_back_message = str(e) + "\n" + str(add_news_trace_back)
        print(add_news_trace_back_message)
        print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> ARTICLE SAVE -> EXCEPTION STACK TRACE END")
        pass
    print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> ARTICLE SAVE -> INSERT END")


def scrap():
    print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> SCRAP START")
    news_company = get_all_company_code()
    for News_Company_Code in news_company:
        current_job_target_company_code = str(News_Company_Code[0])
        print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> CURRENT JOB TARGET COMPANY CODE : "+ str(current_job_target_company_code))
        print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> CURRENT JOB START ")
        current_datetime = datetime.now()
        target_date = datetime.strftime(current_datetime, '%Y%m%d')
        target_company = current_job_target_company_code
        print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> CURRENT JOB TARGET DATA : "+ str(target_date))
        url = 'https://news.naver.com/main/list.naver?mode=LPOD&mid=sec&oid=' + \
              target_company + \
              '&listType=title&date=' + \
              target_date
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> CONDITION 1 CHECK(HTTP RESPONSE 200) PASS")
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                for ulElements in soup.find_all("ul", class_="type02"):
                    for href in ulElements.find_all("li"):
                        print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> SCRAP URL : " + str(href.find("a")["href"]))
                        try:
                            if check_news(href.find("a").text, target_company):
                                print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> ARTICLE DUPLICATED -> SCRAP END")
                            else:
                                visiturl = href.find("a")["href"]
                                visitResponse = requests.get(visiturl, headers=headers)
                                if response.status_code == 200:
                                    print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> CONDITION 2 CHECK(HTTP RESPONSE 200) PASS")
                                    print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> SCRAP START")
                                    try:
                                        visitHtml = visitResponse.text
                                        visitSoup = BeautifulSoup(visitHtml, 'html.parser')
                                        if type(visitSoup.find(class_='media_end_head_headline')) is None:
                                            articleTitle = '타이틀 정보 없음'
                                        else:
                                            articleTitle = visitSoup.find(class_='media_end_head_headline').text.strip()
                                        articleBody = visitSoup.find(id='dic_area').text.strip()
                                        articleBodyRaw = str(visitSoup.find(id='dic_area')).replace('data-src', 'src')
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
                                        articleTimeHourResult = datetime.strptime(articleTimeHourConvert.strftime("%H:%M"), '%H:%M').time()
                                        inputarticleTime = articleTimeDate.strftime('%Y-%m-%d') + ' ' + articleTimeHourResult.strftime('%H:%M:%S')
                                        add_news(articleBy,articleTitle,articleCompany,articleBody,inputarticleTime,'','','','','',articleBodyRaw)
                                        print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> ARTICLE SAVED -> SCRAP END")
                                    except Exception as e2:
                                        trace_back2 = traceback.format_exc()
                                        message2 = str(e2) + "\n" + str(trace_back2)
                                        print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> CONDITION 2 STACK TRACE START")
                                        print(message2)
                                        print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> CONDITION 2 EXCEPTION")
                                        print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> CONDITION 2 STACK TRACE END")
                                        pass
                                else:
                                    print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> CONDITION 2 CHECK(HTTP RESPONSE 200) FAIL")
                        except Exception as e1:
                            trace_back1 = traceback.format_exc()
                            message1 = str(e1) + "\n" + str(trace_back1)
                            print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> CONDITION 1 STACK TRACE START")
                            print(message1)
                            print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> CONDITION 1 STACK TRACE END")
                            print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> CONDITION 1 EXCEPTION")
                            pass
            else:
                print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> CURRENT JOB END")
        except Exception as e:
            trace_back = traceback.format_exc()
            message = str(e) + "\n" + str(trace_back)
            print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> CONDITION ROOT STACK TRACE START")
            print(message)
            print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> CONDITION ROOT STACK TRACE END")
            print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> EXCEPTION FROM LOOPING")
            print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> CONDITION ROOT EXCEPTION")
            pass
        print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> CURRENT JOB END")
    print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> SCRAP END")


def elastic_template_manage():
    print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> ELASTIC TEMPLATE MANAGE JOB START")
    try:
        es_protocol = "http"
        es_host = "15.164.211.132"
        es_port = "9200"
        es_url = es_protocol + "://" + es_host + ":" + es_port + "/bs4news_news"
        res = requests.delete(es_url)
        print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> ELASTIC TEMPLATE(bs4news_news) DELETE REQUEST RESPONSE")
        print(res.text)
        print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> ELASTIC TEMPLATE DELETE JOB 1 SUCCESS")
        es_url = es_protocol + "://" + es_host + ":" + es_port + "/bs4news_news_analysis_raw"
        res = requests.delete(es_url)
        print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> ELASTIC TEMPLATE(bs4news_news_analysis_raw) DELETE REQUEST RESPONSE")
        print(res.text)
        print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> ELASTIC TEMPLATE DELETE JOB 2 SUCCESS")
    except Exception as e1:
        print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> ELASTIC TEMPLATE DELETE JOB FAIL")
        trace_back = traceback.format_exc()
        message = str(e1) + "\n" + str(trace_back)
        print(message)
    print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> ELASTIC TEMPLATE DELETE JOB END")
    print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> ELASTIC TEMPLATE PUT JOB START")
    try:
        es_protocol = "http"
        es_host = "15.164.211.132"
        es_port = "9200"
        es_url = es_protocol + "://" + es_host + ":" + es_port + "/bs4news_news"
        query_object = {
                          "settings": {
                            "number_of_shards": 1,
                            "number_of_replicas": 1
                          },
                          "mappings": {
                            "properties": {
                              "id":{
                                "type":"integer"
                              },
                              "News_from": {
                                "type": "text"
                              },
                              "News_title": {
                                "type": "text"
                              },
                              "News_company": {
                                "type": "text"
                              },
                              "News_contents": {
                                "type": "text"
                              },
                              "News_contents_raw": {
                                "type": "text"
                              },
                              "News_CreateDT": {
                                "type": "date"
                              },
                              "ETC1": {
                                "type": "text"
                              },
                              "ETC2": {
                                "type": "text"
                              },
                              "ETC3": {
                                "type": "text"
                              },
                              "ETC4": {
                                "type": "text"
                              },
                              "ETC5": {
                                "type": "text"
                              }
                            }
                          }
                        }
        res = requests.put(es_url, json=query_object)
        print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> ELASTIC TEMPLATE(bs4news_news) PUT REQUEST RESPONSE")
        print(res.text)
        print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> ELASTIC TEMPLATE PUT JOB 1 SUCCESS")
        es_url = es_protocol + "://" + es_host + ":" + es_port + "/bs4news_news_analysis_raw"
        query_object = {
                          "settings": {
                            "number_of_shards": 1,
                            "number_of_replicas": 1
                          },
                          "mappings": {
                            "properties": {
                              "id":{
                                "type":"integer"
                              },
                              "News_Analysis_from": {
                                "type": "text"
                              },
                              "News_Analysis_Title": {
                                "type": "text"
                              },
                              "News_Analysis_Company": {
                                "type": "text"
                              },
                              "News_Morphs": {
                                "type": "text"
                              },
                              "News_Analysis_CreateDT": {
                                "type": "date"
                              },
                              "ETC1": {
                                "type": "text"
                              },
                              "ETC2": {
                                "type": "text"
                              },
                              "ETC3": {
                                "type": "text"
                              },
                              "ETC4": {
                                "type": "text"
                              },
                              "ETC5": {
                                "type": "text"
                              }
                            }
                          }
                        }
        res = requests.put(es_url, json=query_object)
        print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> ELASTIC TEMPLATE(bs4news_news_analysis_raw) PUT REQUEST RESPONSE")
        print(res.text)
        print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> ELASTIC TEMPLATE PUT JOB 2 SUCCESS")
    except Exception as e2:
        print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> ELASTIC TEMPLATE PUT JOB FAIL")
        trace_back = traceback.format_exc()
        message = str(e2) + "\n" + str(trace_back)
        print(message)
    print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> ELASTIC TEMPLATE PUT JOB END")
    print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " >> ELASTIC TEMPLATE MANAGE JOB END")



#scrap()
#elastic_template_manage()
check_news('https://n.news.naver.com/mnews/article/529/0000064478?rc=N&ntype=RANKING', '529')
connection.commit()
connection.close()
