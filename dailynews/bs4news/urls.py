from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('scrap', views.scrap, name='scrap'),
    path('chart', views.chart, name='chart'),
    path('graph', views.graph, name='graph'),
]