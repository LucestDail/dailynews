from datetime import datetime, timedelta
from bs4news.models import News, News_Analysis_Raw, News_Company
from main.models import Dashboard


def dashboard_every_minute():
    # Dashboard_Total_News_Count = models.CharField(max_length=200)
    # Dashboard_Total_Analysis_Count = models.CharField(max_length=200)
    # Dashboard_Total_Analysis_Rate = models.CharField(max_length=200)
    # Dashboard_Today_count = models.CharField(max_length=200)

    print('django main dashboard_every_minute crontab started -------------------')
    news_data_count = News.objects.all()
    news_data_count_input = len(news_data_count)

    news_analysis_count_data = News_Analysis_Raw.objects.all()
    news_analysis_count = len(news_analysis_count_data)

    news_analysis_rate = round((news_analysis_count / news_data_count_input) * 100)
    today_check_date = datetime.today() - timedelta(days=1)
    today_input_date = str(today_check_date.year) + '-' + str(today_check_date.month) + '-' + str(today_check_date.day)
    today_from_date = datetime.strptime(today_input_date, '%Y-%m-%d').date()
    today_from_date = datetime.combine(today_from_date, datetime.min.time())
    today_to_date = datetime.combine(today_from_date, datetime.max.time())
    today_news_data_date = News_Analysis_Raw.objects.filter(News_Analysis_CreateDT__range=(today_from_date,
                                                                                           today_to_date))
    today_news_date_count = len(today_news_data_date)
    news_analysis_morphs = News_Analysis_Raw(
        Dashboard_Total_News_Count=news_data_count_input,
        Dashboard_Total_Analysis_Count=news_analysis_count,
        Dashboard_Total_Analysis_Rate=news_analysis_rate,
        Dashboard_Today_count=today_news_date_count,
        News_Analysis_CreateDT=datetime.now(),
    )
    news_analysis_morphs.save()

    print('django main dashboard_every_minute crontab started -------------------')