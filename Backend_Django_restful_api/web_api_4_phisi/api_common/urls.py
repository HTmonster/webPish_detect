#!/usr/bin/python3
# -*- coding:utf-8 -*-
#   ____    ____    ______________
#  |    |  |    |  |              |
#  |    |  |    |  |_____    _____|
#  |    |__|    |       |    |
#  |     __     |       |    |
#  |    |  |    |       |    |
#  |    |  |    |       |    |
#  |____|  |____|       |____|
#
# fileName:urls 
# project: pishi_web_api
# author: theo_hui
# e-mail:Theo_hui@163.com
# purpose: 用于页面导航寻址
# creatData:2019/5/19

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api_common import views

urlpatterns = [
    url(r'^api/$', views.api),#api接口
]

urlpatterns = format_suffix_patterns(urlpatterns)