
import requests

url = 'https://v0.yiketianqi.com/api?unescape=1&version=v91&appid=43656176&appsecret=I42og6Lm&ext=&cityid='

city = '深圳'

r = requests.get(url=url, params=city)
if r:
    r = r.json()
    print(r)
else:
    print("请求失败:%s" % r)