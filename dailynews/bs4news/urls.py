from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('scrap', views.scrap, name='scrap'),
    path('chart', views.chart, name='chart'),
    path('graph', views.graph, name='graph'),
    path('company', views.company, name='company'),
    path('morphs', views.create_morphs, name='morphs'),
    path('indexmorphs', views.index_morphs, name='indexmorphs'),
    path('word2vec', views.word2vec, name='word2vec'),
    path('word2vecrun', views.word2vecrun, name='word2vecrun'),
    path('bs4crawl', views.bs4crawl, name='bs4crawl'),
    path('bs4scrap', views.bs4scrap, name='bs4scrap'),
]