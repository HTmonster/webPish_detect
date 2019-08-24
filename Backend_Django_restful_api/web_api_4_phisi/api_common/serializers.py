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
# fileName:serializers 
# project: REST_api
# author: theo_hui
# e-mail:Theo_hui@163.com
# purpose: 序列化对象 用于接收post对象
# creatData:2019/5/18

from rest_framework import serializers

#接受的序列化器
class RecvSerializer(serializers.Serializer):
    url=serializers.CharField(max_length=200) #要检查的url
    setting=serializers.IntegerField()        #设置的强度
    id=serializers.IntegerField()             #用户的id


#返回的Json数据模版
class ResponJson_temp():

    #预测为正常的
    normal_json={"status":"OK","result":1}
    #预测为恶意的
    malicious_json={"status":"OK","result":0}

    #未知错误
    unkown_json={"status":"ERROR","result":-1}