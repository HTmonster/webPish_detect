#!/usr/bin/python3
# -*- coding:utf-8 -*-
# fileName:getFeatures 
# project: Fish_learning
# author: theo_hui
# e-mail:Theo_hui@163.com
# purpose: 通过url获得页面的各个特征
# creatData:2019/5/20


# coding:utf-8
import time
import datetime

from bs4 import BeautifulSoup
from urllib import request
import re
import tldextract
import requests

def getProxy(targetUrl):
    # 代理服务器
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9020"

    # 代理隧道验证信息
    proxyUser = "H2AU31865TN4QX5D"
    proxyPass = "3EC455D00D4F7D78"

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
        "user": proxyUser,
        "pass": proxyPass,
    }

    proxy_handler = request.ProxyHandler({
        "http": proxyMeta,
        "https": proxyMeta,
    })

    # auth = request.HTTPBasicAuthHandler()
    # opener = request.build_opener(proxy_handler, auth, request.HTTPHandler)

    opener = request.build_opener(proxy_handler)

    request.install_opener(opener)
    resp = request.urlopen(targetUrl).read()
    return resp


# 获取URL中的域名
def getDom(url):
    ext = tldextract.extract(str(url))
    domin = ext.registered_domain
    return domin


def getHtml(fileName):
    try:
        with open(fileName, 'r', encoding='gb18030', errors='ignore') as f:
            html = f.read()
    except IOError:
        html = -1
    return html


# 判断action字段是不是仅仅是一个文件,如果
def getAction(html, targetDomin):
    actionFlag = 0
    soup = BeautifulSoup(html, "html.parser")
    formList = soup.find_all('form', attrs={'action': re.compile('.*')})
    for form in formList:
        actionStr = form.attrs['action']
        if not re.search('#+', actionStr):
            if actionStr != '' and actionStr.find('/') == -1:
                return 1
        if re.search('http|https|//.*', actionStr):
            if (getDom(actionStr) != targetDomin):
                return 1
    return actionFlag


# 判断超链接是否有很多为空(占所有链接的比率大于0.3）,超链接可疑（很多包含php）
def getHyperlink(html, targetDomin):
    hyperlinkNum = 0
    nullHyperlink = 0
    nullHyperlinkFlag = 0
    suspecLink = 0
    suspecLinkFlag = 0
    outLink = 0
    outLinkFlag = 0

    soup = BeautifulSoup(html, "html.parser")
    # aList = soup.find_all('a')
    aList = soup.find_all('a', href=re.compile('.*'))
    for a in aList:
        hyperlink = a.attrs['href']
        if hyperlink == '#' or hyperlink == 'javascript:;' or hyperlink == '':
            nullHyperlink += 1
        else:
            if re.search('.*\.php?.*|.*aspx$|.*php$|.*asp$', hyperlink):
                suspecLink += 1
            if re.search('http|https.*', hyperlink):
                if getDom(hyperlink) != targetDomin:
                    outLink += 1
        hyperlinkNum += 1
    if hyperlinkNum == 0:
        return 0, 0, 0, 1
    nullHyperlinkFlag = nullHyperlink / float(hyperlinkNum)
    suspecLinkFlag = suspecLink / float(hyperlinkNum)
    outLinkFlag = outLink / float(hyperlinkNum)
    return float('%.4f' % nullHyperlinkFlag), float('%.4f' % suspecLinkFlag), float('%.4f' % outLinkFlag), 0


# 判断css文件指向外部并且包含域名
def getOutCss(html, targetDomin):
    soup = BeautifulSoup(html, "html.parser")
    cssLinkList = soup.find_all(name='link', attrs={'type': 'text/css'})
    for cssLink in cssLinkList:
        try:
            if 'href' in str(cssLink):
                cssFile = cssLink.attrs['href']
                if re.search(r'http|https.*', cssFile):
                    if getDom(cssFile) != targetDomin:
                        return 1
        except:
            return 0
    return 0


# 获取访问的排名
def get_alexa_rank(targetDomin):
    try:
        r = getProxy("http://alexa.chinaz.com/" + targetDomin)
        soup = BeautifulSoup(r, "html.parser")
        ul = soup.find_all(class_="result_top")[1]
        try:
            li = ul.contents[1].string
        except:
            return None
        return li
    except:
        return None


# 获取注册时间，过期时间
def getWhoisInfo(targetDomin):
    try:
        r = requests.get("http://whois.chinaz.com/" + targetDomin)
        r.encoding = r.apparent_encoding
        html = r.text
        soup = BeautifulSoup(html, "html.parser")
        div = soup.find_all(class_="fr WhLeList-right")
        startTime = div[2].string
        endTime = div[3].string

        str1 = "2019-05-07"  # 当前日期
        array = time.strptime(startTime, u"%Y年%m月%d日")
        str2 = time.strftime("%Y-%m-%d", array)  # 注册时间
        array = time.strptime(endTime, u"%Y年%m月%d日")
        str3 = time.strftime("%Y-%m-%d", array)  # 过期时间
        if (len(str2) == 0):
            flag, flag2 = None, None
        else:
            year1 = datetime.datetime.strptime(str1, "%Y-%m-%d").year
            year2 = datetime.datetime.strptime(str2, "%Y-%m-%d").year
            year3 = datetime.datetime.strptime(str3, "%Y-%m-%d").year
            month1 = datetime.datetime.strptime(str1, "%Y-%m-%d").month
            month2 = datetime.datetime.strptime(str2, "%Y-%m-%d").month
            month3 = datetime.datetime.strptime(str3, "%Y-%m-%d").month
            month_diff = (year1 - year2) * 12 + (month1 - month2)
            validation_diff = (year3 - year2) * 12 + (month3 - month2)
            if (month_diff <= 6):
                flag = 1
            elif (month_diff > 6):
                flag = 0

            if (validation_diff <= 12):
                flag2 = 1
            elif (validation_diff > 12):
                flag2 = 0
        return flag, flag2
    except:
        return 2, 2

def get_standard_feature_vector(url):
    '''
    获得标准的页面特征向量
    :param url:
    :return:
    '''
    #非空判断
    if url is None:
        print("输入none")
        return None

    try:
        #补全url
        if not url.startswith("http://") and not url.startswith("https://"):
            url="http://"+url

        #获取url对应的页面
        r = requests.get(url, timeout=(3, 7))
        r.encoding = r.apparent_encoding
        html = r.text


        # 网页的域名
        targetDomin = getDom(url)
        # action表单
        actionFlag = getAction(html, targetDomin)
        # 空连接，可疑链接
        nullHyperlinkFlag, suspecLinkFlag, outLinkFlag, zeroLinkFlag = getHyperlink(html, targetDomin)
        # 指向外部域名的css文件
        outCssFlag = getOutCss(html, targetDomin)

        # 构造特征向量
        feature_vector = [actionFlag, nullHyperlinkFlag, suspecLinkFlag, outLinkFlag, zeroLinkFlag, outCssFlag]

        # print("得到特征向量", feature_vector)
        return [feature_vector]  # 二维

    except:
        return  None



def get_slow_feature_vector(url):
    '''
    获得提取速度慢的页面特征向量
    :param url:
    :return:
    '''
    # 非空判断
    if url is None:
        return None

    try:
        # 获取url对应的页面
        r = requests.get(url, timeout=(3, 7))
        r.encoding = r.apparent_encoding
        html = r.text

        # 网页的域名
        targetDomin = getDom(url)
        regTime, validTime = getWhoisInfo(targetDomin)

        # 构造特征向量
        feature_vector = [regTime, validTime]

        # 结果审核，是否为空的
        for feature in feature_vector:
            if feature is None:
                return None

        return [feature_vector]  # 二维

    except:
        return None


if __name__ == "__main__":
    print(get_standard_feature_vector("http://www.baidu.com"))
    print(get_slow_feature_vector("http://www.baidu.com"))
