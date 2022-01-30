from _datetime import datetime, timedelta
import time

import requests
from bs4 import BeautifulSoup


url = 'https://news.naver.com/main/list.naver?mode=LPOD&mid=sec&oid=032&listType=title&date=20220130'
headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36" }
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
                articleTitle = visitSoup.find(id='articleTitle')
                articleBody = visitSoup.find(id='articleBodyContents')
                articleBy = visitSoup.find(class_='byline')
                articleTime = visitSoup.find(class_='t11')
                article = visitSoup.select('body')
                print(articleTitle.text.strip())
                print(articleBody.text.strip())
                print(articleBy.text.strip())
                textTime = articleTime.text.strip()
                print(articleTime.text.strip())
                print(textTime.split())
                textTimeDate = textTime.split()[0]
                print(textTimeDate)
                textTimeHour = datetime.strptime(textTime.split()[2], '%H:%M')
                print(timedelta(hours=12) + textTimeHour)
                print(textTimeHour)
                time.sleep(5)
            else :
                print(visitResponse.status_code)
else :
    print(response.status_code)