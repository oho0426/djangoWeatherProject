from django.urls import re_path as url
# 版本不同可能需要改成以下形式
# from django.urls import path
# from django.urls import re_path as url
from . import views

app_name = 'weather'

urlpatterns = [
    url(r'^weather/$', views.home),
    url(r'^provincedata/$', views.provinceData),
    url(r'^citiesdata/$', views.citiesData),
    url(r'^weatherinfo/$', views.weatherInfo)
]