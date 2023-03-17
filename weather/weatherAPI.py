import json
import time

import requests


class WeatherAPI:
    domain = 'http://www.nmc.cn'

    def timeStamp(self):
        return time.time()

    def getProvince(self):
        path = '/rest/province/all'
        timeStamp = self.timeStamp()
        params = {
            "_": timeStamp
        }
        provinceData = requests.get(url=self.domain + path, params=params)
        content = provinceData.content
        res = json.loads(content.decode('utf-8'))

        if res:
            return res
        else:
            print("未知错误！")

    def getCities(self, province):
        timeStamp = self.timeStamp()
        provinceCode = province
        if provinceCode:
            path = '/rest/province/%s' % provinceCode
        else:
            raise ValueError("省份code不能为空！")
        params = {
            '_': timeStamp
        }
        res = requests.get(url=self.domain + path, params=params)
        cityCode = json.loads(res.content.decode('utf-8'))
        if cityCode:
            return cityCode
        else:
            print("未知错误！")

    def getWeatherInfo(self, city):
        timeStamp = self.timeStamp()
        cityCode = city
        path = '/rest/weather'
        if not cityCode:
            raise ValueError("城市code不能为空！")
        params = {
            'stationid': cityCode,
            '_': timeStamp
        }
        res = requests.get(url=self.domain + path, params=params)
        weatherInfo = json.loads(res.content.decode('utf-8'))
        if weatherInfo:
            return weatherInfo
        else:
            print("未知错误！")
