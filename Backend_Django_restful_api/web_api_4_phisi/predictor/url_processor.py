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
# fileName:url_processor 
# project: Fish_learning
# author: theo_hui
# e-mail:Theo_hui@163.com
# purpose: 对url进行处理
# creatData:2019/5/18
import re

from gensim.models import Word2Vec
import numpy as np
import tensorflow as tf

from predictor.tools import Parameter


def process_url(url):
    '''
    对URL处理
    1.清理
    2.划分
    3.对齐
    :param url: 目标的URL
    :return: 清理之后的URL 为一个数组
    '''

    # 先将字节数组转换为字符
    url_str = str(url)

    # 去掉常见的字符
    url_str = re.sub(r"http://", "", url_str)
    url_str = re.sub(r"https://", "", url_str)
    url_str = re.sub(r".html$", "", url_str)
    url_str = re.sub(r".htm$", "", url_str)

    #分隔字符
    url_str=re.split(r"[/=-?.&]",url_str)

    #print(url_str)

    #对齐
    if len(url_str)> Parameter.max_seq_length:
        url_str= url_str[:Parameter.max_seq_length]
    else:
        url_str.extend(Parameter.padding_taken for _ in range(Parameter.max_seq_length - len(url_str)))

    return url_str

def get_word2vec(processed_url):
    '''
    对处理好后的url通过word2vec得到词向量
    :param url:
    :return:
    '''
    #print(processed_url)

    #增加一个唯独
    add_url=[processed_url]

    #加载模型
    w2vModel =  Word2Vec.load(Parameter.word2vec_model_path)

    #增量训练
    w2vModel.build_vocab(add_url,update=True)
    w2vModel.train(add_url,total_examples=1,epochs=1)

    #找到词对应的向量
    url_vector=[]
    embeddingUnknown=[0.0 for _ in range(Parameter.embedding_size)]
    for word in processed_url:
        if word in w2vModel.wv.vocab:
            url_vector.append(w2vModel[word])
        else:
            url_vector.append(embeddingUnknown)

    #print(np.array([url_vector]).shape)

    return np.array([url_vector])

def url_vector_prediction(url_vector):
    '''
    对url向量进行预测
    :param url_vector: 向量数组
    :return:
    '''

    # 清除默认图的堆栈，并设置全局图为默认图
    tf.reset_default_graph()

    with tf.Session() as sess:

        #提取模型
        saver = tf.train.import_meta_graph(Parameter.TextCNN_meta_path)
        saver.restore(sess, Parameter.TextCNN_model_path)

        #得到模型
        graph=tf.get_default_graph()

        #预测操作
        prediction=graph.get_tensor_by_name("output/predictions:0")
        score=graph.get_tensor_by_name("output/score:0")

        #词输入
        input_x=graph.get_operation_by_name("input_x").outputs[0]
        keep_prob = graph.get_operation_by_name('dropout_keep_prob').outputs[0]

        # 运用softmax得到0-1之间的概率
        probability = tf.nn.softmax(score)

        #得到预测结果
        pre=sess.run(prediction,feed_dict={input_x: url_vector,keep_prob:1})[0]
        prob=max(sess.run(probability,feed_dict={input_x: url_vector,keep_prob:1}).tolist()[0])

        sess.close()

        return pre,prob

def url_predict(url):
    '''
    对url进行预测，主要为上面几个函数的综合
    :param url: 目标URL
    :return:
    '''
    #空判断
    if url is None:
        return None

    #对url进行前处理
    processed_url = process_url(url)

    #获得url向量
    url_vector = get_word2vec(processed_url)

    #进行预测
    url_prediction,url_prob=url_vector_prediction(url_vector)

    return url_prediction,url_prob

if __name__ == '__main__':

    print(url_predict("http://www.bawifm.org/"))