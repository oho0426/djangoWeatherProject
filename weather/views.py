import json
import re
import zhdate
import requests
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from weather import weatherAPI
from django.http import JsonResponse
from django.utils import timezone
from .models import WeatherInfo


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
    today_date = timezone.now().strftime("%Y-%m-%d")
    today_m_d = "%s月%s日" % (timezone.now().month, timezone.now().day)
    # 转换农历日期

    zh_date = zhdate.ZhDate.from_datetime(timezone.now())
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


def reJsonResponse(code=0, text=None, msg='success', contentType='application/json'):
    res = {'code': code, 'msg': msg}
    res['data'] = text
    return JsonResponse(res, content_type=contentType)


def provinceData(request):
    """
    获取省份code
    :param request:GET请求
    :return:返回全国所有省份
    """
    try:
        if request.method == 'GET':
            weather_API = weatherAPI.WeatherAPI()
            provinceJson = weather_API.getProvince()
            if provinceJson:
                return reJsonResponse(0, provinceJson)
            else:
                return reJsonResponse(1, provinceJson, msg='fail')
        else:
            return reJsonResponse(1, msg='请求方法错误！')
    except Exception as e:
        return reJsonResponse(1, msg=str(e))


def citiesData(request):
    """
    根据省份code获取城市信息
    :param request:GET请求
    :return:返回省份下所有的城市code/名称
    """
    try:
        if request.method == 'GET':
            weather_API = weatherAPI.WeatherAPI()
            provinceCode = request.GET.get('provinceCode')
            if not provinceCode:
                provinceCode = 'ABJ'
            citiesJson = weather_API.getCities(provinceCode)
            if citiesJson:
                return reJsonResponse(0, citiesJson)
            else:
                return reJsonResponse(1, citiesJson, msg='fail')
        else:
            return reJsonResponse(1, msg='请求方法错误！')
    except Exception as e:
        return reJsonResponse(1, msg=str(e))


def weatherInfo(request):
    """
    根据城市ID获取天气信息
    :param request:POST请求
    :return:返回json格式的天气信息
    """
    try:
        if request.method == 'POST':
            weather_API = weatherAPI.WeatherAPI()
            cityCode = request.POST.get('cityCode')
            provinceCode = request.POST.get('provinceCode')
            if not cityCode:
                raise ValueError("城市code不能为空！")

            # 去数据库查询，如果时间大于15分钟，则调用接口更新数据
            searchTime = timezone.now() - timezone.timedelta(minutes=15)
            searchWeatherInfo = WeatherInfo.objects.filter(
                province_code=provinceCode,
                city_code=cityCode,
                create_time__gte=searchTime
            ).order_by('-id').first()
            weatherJson = None
            if searchWeatherInfo:
                print(searchWeatherInfo.create_time)
                weatherJson = json.loads(searchWeatherInfo.weather_info)
            # 如果没有查到数据或数据超过15分钟，则请求接口，插入数据
            if not weatherJson:
                # 请求接口，获取信息
                weatherJson = weather_API.getWeatherInfo(cityCode)
                # 设置表字段数据
                province = weatherJson['real']['station']['province']
                city = weatherJson['real']['station']['city']
                weather_info = json.dumps(weatherJson)
                WeatherInfo.objects.create(
                    province=province,
                    province_code=provinceCode,
                    city=city,
                    city_code=cityCode,
                    weather_info=weather_info
                )

            if weatherJson:
                return reJsonResponse(0, weatherJson)
            else:
                return reJsonResponse(1, weatherJson, msg='fail')
        else:
            return reJsonResponse(1, msg='请求方法错误！')
    except Exception as e:
        return reJsonResponse(1, msg=str(e))
