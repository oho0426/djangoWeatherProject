from datetime import datetime
import zhdate
import requests
from django.shortcuts import render
from django.contrib import messages


# Create your views here.
def home(request):
    """首页"""
    city = "内蒙古"
    while(True):
        city_data = {"city": city}
        total_data = apiInfo(city_data)
        print(city)
        print(total_data)
        errcode = 'errcode'
        if errcode in total_data:
            messages.error(request, '请求失败:%s 默认城市北京' % total_data['errmsg'])
            city = "北京"
            continue
        else:
            break

    # 取出今天的天气数据
    today_date = datetime.today().strftime("%Y-%m-%d")
    today_m_d = "%s月%s日" % (datetime.today().month, datetime.today().day)
    # 转换农历日期

    zh_date = zhdate.ZhDate.from_datetime(datetime.today())
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