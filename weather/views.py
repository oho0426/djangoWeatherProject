from datetime import datetime
import zhdate
import requests
from django.shortcuts import render
from django.contrib import messages


# Create your views here.
def home(request):
    """首页"""
    city = {"city": "内蒙古"}
    total_data = apiInfo(city)
    for i in total_data:
        if i == 'errcode':
            messages.error(request, '请求失败:%s' % total_data['errmsg'])

    if total_data is None:
        messages.error(request, '请求失败:未知错误!')
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
        print(r)
        return r
    else:
        print("请求失败:%s" % r)