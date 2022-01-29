from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import News

# Create your views here.

def index(request):
    news_list = News.objects.order_by('-News_CreateDT')[:5]
    template = loader.get_template('bs4news.html')
    context = {
        'news_list': news_list,
    }
    return HttpResponse(template.render(context, request))
