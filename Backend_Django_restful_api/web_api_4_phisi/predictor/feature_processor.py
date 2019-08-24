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
# fileName:feature_processor.py
# project: Fish_learning
# author: theo_hui
# e-mail:Theo_hui@163.com
# purpose: 对页面进行判断
# creatData:2019/5/20

import tensorflow as tf

from predictor.tools import getFeatures,Parameter

def standard_feature_predict(url):
    '''
    对页面使用模型进行预测
    :param url:
    :return:
    '''

    #先获得特征向量
    feature_vector,timeCount=None,0

    while(feature_vector is None):
        feature_vector=getFeatures.get_standard_feature_vector(url)
        # print("得到的",feature_vector)
        timeCount+=1
        if timeCount>=10:
            print("提取特征超时")
            return None,None

    #判断向量
    if feature_vector is None:
        return None

    # 清除默认图的堆栈，并设置全局图为默认图
    tf.reset_default_graph()

    with tf.Session() as sess:


        #提取模型
        saver = tf.train.import_meta_graph(Parameter.standard_simpleNN_meta_path)
        saver.restore(sess,Parameter.standard_simpleNN_model_path)

        #得到模型
        graph=tf.get_default_graph()

        #预测操作
        prediction=graph.get_tensor_by_name("output/predictions:0")
        y=graph.get_tensor_by_name("output/y:0")

        #运用softmax得到0-1之间的概率
        probability=tf.nn.softmax(y)

        #词输入
        input_x=graph.get_operation_by_name("x-input").outputs[0]

        #得到预测结果
        pre=sess.run(prediction,feed_dict={input_x: feature_vector})[0]
        prob=max(sess.run(probability,feed_dict={input_x: feature_vector}).tolist()[0])

        sess.close()

        return pre,prob

def slow_feature_predict(url):
    '''
    对页面使用模型进行预测
    :param url:
    :return:
    '''

    #先获得特征向量
    feature_vector=getFeatures.get_slow_feature_vector(url)

    #判断向量 返回错误
    if feature_vector is None:
        return -1

    # 清除默认图的堆栈，并设置全局图为默认图
    tf.reset_default_graph()

    with tf.Session() as sess:


        #提取模型
        saver = tf.train.import_meta_graph(Parameter.slow_simpleNN_meta_path)
        saver.restore(sess,Parameter.slow_simpleNN_model_path)

        #得到模型
        graph=tf.get_default_graph()

        #预测操作
        prediction=graph.get_tensor_by_name("output/predictions:0")
        y=graph.get_tensor_by_name("output/y:0")

        #运用softmax得到0-1之间的概率
        probability=tf.nn.softmax(y)

        #词输入
        input_x=graph.get_operation_by_name("x-input").outputs[0]

        #得到预测结果
        pre=sess.run(prediction,feed_dict={input_x: feature_vector})[0]
        prob=max(sess.run(probability,feed_dict={input_x: feature_vector}).tolist()[0])

        sess.close()

        return pre,prob


if __name__ == '__main__':
    print(standard_feature_predict("https://www.baidu.com"))
    print(slow_feature_predict("https://www.baidu.com"))