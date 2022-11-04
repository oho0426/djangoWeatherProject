import time
from datetime import datetime
import zhdate
import requests

# today_date = datetime.today().strftime("%Y-%m-%d")
# url = 'https://v0.yiketianqi.com/api?unescape=1&version=v91&appid=43656176&appsecret=I42og6Lm&ext=&cityid='
# city = '深圳'
# print(today_date)
# res = requests.get(url=url, params=city).json()
# today_data = []
# for x in res['data']:
#     if x['date'] == today_date:
#         today_data = x
#
# print(today_data)
today_date = datetime.today()
zh_date = zhdate.ZhDate.from_datetime(datetime.today())
print(zh_date)