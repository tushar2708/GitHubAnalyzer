from django.conf.urls import url
from . import views



urlpatterns = [
    url(r'^$', views.query_new, name='query_new'),
    url(r'^query_list/$', views.query_list, name='query_list'),
    url(r'^result/(?P<id>\d+)/', views.result_detail, name='result_detail'),
]
