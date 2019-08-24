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
# fileName:total_prediction 
# project: Fish_learning
# author: theo_hui
# e-mail:Theo_hui@163.com
# purpose: 总体的预测判断
# creatData:2019/5/20

import tensorflow as tf

from predictor.tools import Parameter
from predictor import feature_processor,url_processor

def judge_part(url_prediction,feature_prediction,url_prob,feature_prob,setting=1):
    '''
    根据两个模型的结果来决定最后的结果
    :param url_prediction: url的预测结果
    :param feature_prediction: feature的预测结果
    :param url_prob: url预测的可信概率
    :param feature_prob: feature预测的可信概率
    :param setting: 设置的强度 默认为强：1
    :return: 判断的结果
    '''

    #强提醒设置
    if setting==1:

        #只要有一个检测为恶意则输出为恶意
        if url_prediction==0 or feature_prediction==0:
            return 0
        else:
            return 1

    #弱提醒设置
    else:
        #两个模型都预测正常
        if url_prediction==1 and feature_prediction==1:
            return 1 #则返回正常
        #两个模型都预测恶意
        elif url_prediction==0 and feature_prediction==0:
            return 0 #返回恶意

        #预测分歧
        else:
            print("预测发生分歧")
            #url预测的总正确率
            url_predict_prob=url_prob*Parameter.TextCNN_accuracy+(1-feature_prob)*Parameter.standard_simpleCNN_accuracy

            #feature预测的总正确率
            feature_predict_prob=(1-url_prob)*Parameter.TextCNN_accuracy+feature_prob*Parameter.standard_simpleCNN_accuracy

            print(url_predict_prob,feature_predict_prob)
            if(url_predict_prob>feature_predict_prob):
                return url_prediction
            elif(url_predict_prob<feature_predict_prob):
                return feature_prediction
            else:
                return -1

def  Aid_predict(url):
    '''
    当前面两个模型判决不出来结果的时候，使用辅助的判决
    :param url: 目标url
    :return: 判决结果
    '''

    prediction=feature_processor.slow_feature_predict(url)

    return prediction

def predict(url,setting=1):
    '''
    根据输入的url来进行预测
    :param url: 要预测的URL
    :param setting: 设置的提醒模式
    :return: 预测的结果
    '''



    # 对url进行预测
    url_prediction,url_prob=url_processor.url_predict(url)
    print(url,"模型一预测结果",url_prediction,url_prob)

    # 对标准特征进行预测
    feature_prediction, feature_prob = feature_processor.standard_feature_predict(url)
    print(url,"模型二预测结果", feature_prediction, feature_prob)

    #使用判决器进行判决
    if feature_prediction is not None:
        print("使用判决器")
        judge_result=judge_part(url_prediction,feature_prediction,url_prob,feature_prob,setting=setting)

        #是否已经判断出结果
        if judge_result!= -1:
            return judge_result

        #否则进行辅助判决
        else:
            aid_result=Aid_predict(url)

            if aid_result:
                return aid_result
    else:
        return url_prediction

if __name__ == '__main__':
    print(predict("http://www.bawifm.org/"))