from django.db import models

# Create your models here.
class WeatherInfo(models.Model):
    # 省份
    province = models.CharField(max_length=20, null=False)
    # 省份code
    province_code = models.CharField(max_length=20, null=False)
    # 城市
    city = models.CharField(max_length=20, null=False)
    # 城市code
    city_code = models.CharField(max_length=20, null=False)
    # 天气信息
    weather_info = models.TextField(null=False)
    # 创建时间
    create_time = models.DateTimeField(null=False, auto_now_add=True)
    # 更新时间
    update_time = models.DateTimeField(null=False, auto_now=True)