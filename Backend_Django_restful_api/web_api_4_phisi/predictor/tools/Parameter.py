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
# fileName:Parameter 
# project: Fish_learning
# author: theo_hui
# e-mail:Theo_hui@163.com
# purpose: 参数类 用来指示处理url的参数设置
# creatData:2019/5/18


max_seq_length=30
embedding_size=50
padding_taken="<PADDING>"

#word2vec模型
word2vec_model_path="./predictor/model/word2vec/50_30/trained_word2vec.model"
word2vec_incre=False  #是否更新

#TextCNN模型
TextCNN_model_path="./predictor/model/TextCNN/50_30/checkpoints/model-2200"
TextCNN_meta_path="./predictor/model/TextCNN/50_30/checkpoints/model-2200.meta"

#标准的simpleNN模型
standard_simpleNN_model_path="./predictor/model/simpleNN/standard/checkpoints/model-10000"
standard_simpleNN_meta_path="./predictor/model/simpleNN/standard/checkpoints/model-10000.meta"

#特征提取慢的simpleNN模型
slow_simpleNN_model_path="./predictor/model/simpleNN/slow/checkpoints/model-6000"
slow_simpleNN_meta_path="./predictor/model/simpleNN/slow/checkpoints/model-6000.meta"


#每个模型的正确率
TextCNN_accuracy=0.98
standard_simpleCNN_accuracy=0.85
slow_simpleCNN_accuracy=0.70