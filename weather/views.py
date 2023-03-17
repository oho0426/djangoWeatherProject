import json
import re
from datetime import datetime
import zhdate
import requests
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
import weather.weatherAPI


# Create your views here.
def home(request):
    """首页"""
    city = "北京"
    if request.method == 'GET':
        search_city = request.GET.get("city")
        if search_city is not None:
            city = search_city

    i = 0
    total_data = []
    while i < 3:
        i += 1
        city_data = {"city": city}
        total_data = apiInfo(city_data)
        errcode = 'errcode'
        if errcode in total_data:
            messages.error(request, '查找错误:%s 已切换至默认城市' % total_data['errmsg'])
            city = "北京"
            continue
        else:
            break

    # 取出今天的天气数据
    today_date = datetime.today().strftime("%Y-%m-%d")
    today_m_d = "%s月%s日" % (datetime.today().month, datetime.today().day)
    # 转换农历日期

    zh_date = zhdate.ZhDate.from_datetime(datetime.today())
    zh_date = zh_date.chinese()
    print(zh_date)
    today_data = []
    for x in total_data['data']:
        if x['date'] == today_date:
            today_data = x
    # 天气图标路径
    wea_img_path = 'img/%s.png' % today_data['wea_img']

    return render(request, 'index.html', locals())


def apiInfo(city):
    """请求接口返回数据"""
    url = 'https://v0.yiketianqi.com/api?unescape=1&version=v91&appid=43656176&appsecret=I42og6Lm&ext=&cityid='
    r = requests.get(url=url, params=city)
    if r:
        r = r.json()
        return r
    else:
        print("请求失败:%s" % r)


def reResponse(code=0, text=None, msg='success', contentType='application/json'):
    res = {'code': code, 'msg': msg}
    res['data'] = text
    return HttpResponse(json.dumps(res), content_type=contentType)


def provinceData(request):
    try:
        if request.method == 'GET':
            weatherAPI = weather.weatherAPI.WeatherAPI()
            provinceJson = weatherAPI.getProvince()
            if provinceJson:
                return reResponse(0, provinceJson)
            else:
                return reResponse(1, provinceJson, msg='fail')
        else:
            return reResponse(1, msg='请求方法错误！')
    except Exception as e:
        return reResponse(1, msg=str(e))


def citiesData(request):
    try:
        if request.method == 'GET':
            weatherAPI = weather.weatherAPI.WeatherAPI()
            provinceCode = request.GET.get('provinceCode')
            if not provinceCode:
                provinceCode = 'ABJ'
            citiesJson = weatherAPI.getCities(provinceCode)
            if citiesJson:
                return reResponse(0, citiesJson)
            else:
                return reResponse(1, citiesJson, msg='fail')
        else:
            return reResponse(1, msg='请求方法错误！')
    except Exception as e:
        return reResponse(1, msg=str(e))

def weatherInfo(request):
    try:
        if request.method == 'GET':
            weatherAPI = weather.weatherAPI.WeatherAPI()
            cityCode = request.GET.get('cityCode')
            if not cityCode:
                raise ValueError("城市code不能为空！")
            weatherJson = weatherAPI.getWeatherInfo(cityCode)
            if weatherJson:
                return reResponse(0, weatherJson)
            else:
                return reResponse(1, weatherJson, msg='fail')
        else:
            return reResponse(1, msg='请求方法错误！')
    except Exception as e:
        return reResponse(1, msg=str(e))