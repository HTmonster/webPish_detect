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
# fileName:getPsychologyFeatures.py 
# project: Fish_learning
# author: theo_hui
# e-mail:Theo_hui@163.com
# purpose: 根据url获取通过神经网络模型得到其所属的分类编码
# notice: 基于语料丰富度及速度的考虑，目前使用网络接口进行判断，
#          但是后续会收集语料，训练定制的 更加贴合社工判断的文本分类模型
# creatData:2019/5/20


import json
import requests
from bs4 import BeautifulSoup
from QcloudApi.qcloudapi import QcloudApi  #腾讯云文本分类SDK
from translation import iciba
from langdetect import detect


#请求的参数
module = 'wenzhi'
action = 'TextClassify'
config = {
    'Region': 'gz',
    'secretId': 'AKIDDCvVr4YvOFrHVU9yVt2zkK9i13qSlwls',
    'secretKey': '5vU5RfpsOkupa5OofJiuvFX5Jo7O3Yhf',
    'method': 'POST'
}

#下载页面请求头参数
headers = {'user-agent':
               "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)"}


#类型整合对应表
# code_table={0:[0,65535],#其他分类 未知类等
#              11:[43,44,45,51],#色情类
#              12:[28,59],#求职类
#              13:[13,32,81,80,79,78,77,76,75,74,73,72,71],#金融类
#              14:[7,67],#下载类
#              15:[15,],#住所类
#              21:[17,],#教育类
#              22:[10,11,31],#医药类
#              31:[60],#宗教类
#              32:[21],#社交类
#              41:[12,22],#广告营销类
#              42:[52,47,23,41,42],#猎奇类
#              43:[3,8,62,61,95],#知识类
#              51:[2],#游戏类
#              52:[4,94,93,92,91,89,88,87,86],#体育类
#              53:[5,6,84,83,82],#影视类
#              54:[55,85],#娱乐类
#              55:[54],#博彩类
#              56:[16],#动漫类
#              57:[1,9,14,18,19,56,57,58,66,65,64,63],#其他兴趣类
#              }
# #tags:
code_table={0:[0,65535],#其他分类 未知类等
             11:[43,44,45,51],#色情类
             12:[28,59],#求职类
             13:[13,32,81,80,79,78,77,76,75,74,73,72,71],#金融类
             14:[7,67],#下载类
             15:[15,],#住所类
             21:[17,],#教育类
             22:[10,11,31],#医药类
             31:[60],#宗教类
             32:[21],#社交类
             41:[12,22],#广告营销类
             42:[52,47,23,41,42],#猎奇类
             43:[3,8,62,61,95],#知识类
             51:[2],#游戏类
             52:[4,94,93,92,91,89,88,87,86],#体育类
             53:[5,6,84,83,82],#影视类
             54:[55,85],#娱乐类
             55:[54],#博彩类
             56:[16],#动漫类
             57:[1,9,63],#生活类
             58:[18,64,65,66],#科技类
             59:[57,58],#家庭类
             50:[14,56],#其他兴趣类
             }


def get_html_text_by_file(fileName):
    '''
    通过已经下载的html文件 提取其中的文本信息
    :param fileName: html文件
    :return: 提取的文件信息
    '''
    try:
        with open(fileName, 'r', encoding='utf-8', errors='ignore') as f:
            html = f.read()

        soup = BeautifulSoup(html, 'lxml')

        # 去除script与style
        [s.extract() for s in soup(['script', 'style'])]

        # 提取文本 拼接为一串
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)

        print(text)

        # tansor = Translator()
        #
        # print(tansor.detect(text).lang)
        # if tansor.detect(text).lang == 'en':
        #     text = tansor.translate(text, dest="zh-cn").text
        # print(text)
        try:
            print(detect(text))
            if detect(text) != 'zh-cn':
                text = iciba(text, dst='zh')
            print(text)
        except:
            pass

        return text

    except IOError:
        return None




def get_html_text(url):
    '''
    通过URL获取页面内容
    并提取其中的文本信息
    :param url: 目标url
    :return: 提取得到的文本信息
    '''

    #下载页面内容
    try:
        req=requests.get(url,headers=headers,timeout=3)
        req.encoding = req.apparent_encoding
        html=req.text
        #print(html)

        soup = BeautifulSoup(html, 'lxml')

        #去除script与style
        [s.extract() for s in soup(['script','style'])]

        #提取文本 拼接为一串
        text=soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)

        print(text)

        # tansor=Translator()
        #
        # print(tansor.detect(text).lang)
        # if tansor.detect(text).lang=='en':
        #     text=tansor.translate(text,dest="zh-cn").text
        # print(text)

        try:
            print(detect(text))
            if detect(text) != 'zh-cn':
                text = iciba(text, dst='zh')
            print(text)
        except:
            pass

        return text
    except:
        return None




def get_small_classification(content):
    '''
    通过网络文本分类api进行查询初步的分类结果
    :param contxt: 要查询的文本内容
    :return: 查询的结果 dict 所属类型
    '''
    #提交参数
    action_params = {
        'content':content,
    }

    #请求
    try:
        service = QcloudApi(module, config)
        # 打印生成的请求URL，不发起请求
        #print(service.generateUrl(action, action_params))

        # 调用接口，发起请求，并打印返回结果
        rst=json.loads(str(service.call(action, action_params),'utf8'))
        #print(rst)

        #请求成功
        if rst['code'] == 0:

            #找到最匹配分类
            classification=rst['classes'][0]
            classification_code=classification['class_num']

            print(classification)

            return classification_code
        else:
            return None
    except :
        return None

def classification_encode(old_code):
    '''
    对分类依据需求金字塔进行重新分类
    :param old_code: 原有所属类的编码
    :return: 编码结果  例如（1000,12） 代表 生理需求类  求职小类
    '''

    #输出向量编码
    cate_code,class_code=0,0

    #遍历查找对应值
    for key,value in code_table.items():
        if old_code in value:
            cate_code=key//10*1000
            class_code=key


    print(cate_code,class_code)

    return (cate_code,class_code)


def get_psychology_features_by_url(url):
    '''
    根据url判断这个页面内容所属的心理学分类层次，得到心理学特征代码

    主要是对上面三个函数封装
    :param url: 目标url
    :return: 心理学特征代码 例如（1000,12）
    '''

    #下载页面并提取文字
    content=get_html_text(url)

    #错误处理
    if content is None:
        return (0,0)

    #通过深度学习分类模型获得初步分类
    class_code=get_small_classification(content)

    #错误处理
    if class_code is None:
        return (0,0)

    #根据马斯洛需求理论对这些进行分类编码
    PsyFeature_vector=classification_encode(class_code)

    return PsyFeature_vector


def get_psychology_features_by_file(fileName):
    '''
    根据已经下载的文件判断这个页面内容所属的心理学分类层次，得到心理学特征代码

    主要是对上面三个函数封装
    :param fileName: 目标html文件
    :return: 心理学特征代码 例如（1000,12）
    '''

    #下载页面并提取文字
    content=get_html_text_by_file(fileName)

    #错误处理
    if content is None:
        return (0,0)

    #通过深度学习分类模型获得初步分类
    class_code=get_small_classification(content)

    #错误处理
    if class_code is None:
        return (0,0)

    #根据马斯洛需求理论对这些进行分类编码
    PsyFeature_vector=classification_encode(class_code)

    return PsyFeature_vector

def count_page_input_by_url(url):
    '''
    通过url统计页面的密码类型输入答标签数
    :param url:
    :return: (input_num,pwd_input_num)
    '''

    try:

        req = requests.get(url, headers=headers, timeout=3)
        req.encoding = req.apparent_encoding
        html = req.text
        # print(html)

        soup = BeautifulSoup(html, 'lxml')

        input_cnt=len(soup.find_all("input"))
        pwd_input_cnt=len(soup.find_all("input",attrs={"type":"password"}))

        print((input_cnt,pwd_input_cnt))

        return (input_cnt,pwd_input_cnt)
    except:
        return 0,0


def count_page_input_by_file(fileName):
    '''
    通过url统计页面的密码类型输入答标签数
    :param url:
    :return: (input_num,pwd_input_num)
    '''

    try:

        with open(fileName, 'r', encoding='utf-8', errors='ignore') as f:
            html = f.read()

        soup = BeautifulSoup(html, 'lxml')

        input_cnt = len(soup.find_all("input"))
        pwd_input_cnt = len(soup.find_all("input", attrs={"type": "password"}))

        print((input_cnt, pwd_input_cnt))

        return (input_cnt, pwd_input_cnt)
    except:
        return (-1, -1)

if __name__ == '__main__':
    #print(get_psychology_features("http://www.iep.utm.edu/aestheti/"))
    #print(get_psychology_features_by_url("https://en.wikipedia.org/wiki/How-to"))
    #count_page_input_by_url("https://shop.dma.org/")
    #count_page_input_by_file("test.html")
    #print(get_psychology_features_by_file("test.html"))

    text="English is good"

    print(detect("你好呀"))
    if detect(text) == 'en':
        text=iciba(text, dst = 'zh')
    print(text)