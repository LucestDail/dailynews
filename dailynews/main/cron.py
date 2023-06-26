from datetime import datetime, timedelta
from bs4news.models import News, News_Analysis_Raw, News_Company
from main.models import Dashboard


def dashboard_index():
    print('django main dashboard_every_minute crontab started -------------------')
    print('job start ========================================')
    print(datetime.now())
    print('job started =====================================>')
    news_data_count = News.objects.all().count()
    news_analysis_count = News_Analysis_Raw.objects.all().count()
    news_analysis_rate = round((news_analysis_count / news_data_count) * 100)
    today_check_date = datetime.today() - timedelta(days=1)
    today_input_date = str(today_check_date.year) + '-' + str(today_check_date.month) + '-' + str(today_check_date.day)
    today_from_date = datetime.strptime(today_input_date, '%Y-%m-%d').date()
    today_from_date = datetime.combine(today_from_date, datetime.min.time())
    today_to_date = datetime.combine(today_from_date, datetime.max.time())
    recent_news_data_count = News_Analysis_Raw.objects.filter(News_Analysis_CreateDT__range=(today_from_date, today_to_date)).count()
    print('TOTAL NEWS COUNT : ' + str(news_data_count))
    print('ANALYSIS NEWS COUNT : ' + str(news_analysis_count))
    print('ANALYSIS NEWS RATE : ' + str(news_analysis_rate))
    print('RECENT NEWS COUNT : ' + str(recent_news_data_count))
    Dashboard_instance = Dashboard(
        Dashboard_Total_News_Count=news_data_count,
        Dashboard_Total_Analysis_Count=news_analysis_count,
        Dashboard_Total_Analysis_Rate=news_analysis_rate,
        Dashboard_Today_count=recent_news_data_count,
        Dashboard_CreateDT=datetime.now(),
    )
    Dashboard_instance.save()
    print('job end ========================================')
    print(datetime.now())
    print('job ended =====================================>')
    print('django main dashboard_every_minute crontab started -------------------')