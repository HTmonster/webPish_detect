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
# fileName:user_portrait 
# project: Fish_learning
# author: theo_hui
# e-mail:Theo_hui@163.com
# purpose: 用户画像精准防御部分
# creatData:2019/6/3

from user_portrait.db_op import user_db_op,usermodel_db_op

#当用户的数据量达到界限后开始匹配画像
BOUNDARY=100

#画像区分的细粒度（%）
FINE_GRAINED=5

def check_update_model(modelid,vuls,cnts,other):
    '''
    判断画像模型需不需要更新，若需要 则更新
    :param modelid: 模型的id
    :param vuls: 模型对应的防护对象top5 列表
    :param cnts: 模型防护对象top对应的受害次数 列表
    :param other: 其他受害情况 字符串列表 每个可以解析为列表 压缩存储
    :return:
    '''
    try:
        others,othercnts=usermodel_db_op.parse_other(other[0],other[1])

        #如果有策略替换
        if max(othercnts)>min(cnts):
            max_index=othercnts.index(max(othercnts))
            min_index=cnts.index(min(cnts))

            #交换值
            cnts[min_index],othercnts[max_index]=othercnts[max_index],cnts[min_index]
            vuls[min_index],others[max_index]=others[max_index],vuls[min_index]

            #构建other
            new_other=usermodel_db_op.build_other(others,othercnts)

            #更新
            usermodel_db_op.update_model(modelid,vuls,cnts,new_other)
    except:
        return False





def add_new_record(user_id,tag_id):
    '''
    添加一条新记录，若是新用户则创建
            新用户没有匹配的模型
    :param user_id: 用户的id
    :param tag_id: 此次浏览数据
    :return:
    '''

    user=user_db_op.get_user_by_id(user_id)

    #如果不存在则创建新用户
    if user is None:
        user_db_op.add_usr(user_id)

    user_db_op.add_user_tag(user_id,tag_id)

    #获取总浏览数据数
    count=user_db_op.get_user_count_by_id(user_id)
    print(count,"c")

    #如果用户历史数据够多，则可以匹配模型
    if count>=BOUNDARY:
        user_info=user_db_op.get_user_by_id(user_id)

        #提取标签的信息
        tags=user_info[3:]

        #print(tags)

        #匹配标签id与数目
        tags_match=list(zip(tags,user_db_op.ALL_TAG))

        #排序
        tags_sorted=sorted(tags_match,key=lambda x:x[0],reverse=True)

        #取前五值
        tags_top_5=tags_sorted[:5]

        #计算百分比
        tags_top_5_per=[]
        tags_top_5_name=[]
        for tag in tags_top_5:
            #得到百分比
            per=tag[0]*100/count
            #print(per)

            #对细粒度取余数
            remain=per%FINE_GRAINED

            # 细粒度内四舍五入
            if remain >(FINE_GRAINED/2):
                rst=int(per-remain+5)
            else:
                rst=int(per-remain)
            print(rst)
            tags_top_5_per.append(rst)

            #前5的标签名字
            tags_top_5_name.append(tag[1])

        print(tags_top_5_per)
        print(tags_top_5_name)

        modelid_str=usermodel_db_op.buid_modelid(tags_top_5_name,tags_top_5_per)

        modelid_info = usermodel_db_op.get_model(modelid_str)

        #如果是新模型则进行创建
        if modelid_info is None:
            usermodel_db_op.add_model(modelid_str)

        #用户增加新模型
        user_db_op.change_model(user_id,modelid_str)

        print(user_db_op.get_user_by_id(user_id))
    else:
        return



def get_protect_policy(userid,tagid):
    '''
    找到此用户对应画像的防御措施
    :param userid: 用户的id
    :return: 防护的重点列表 [vu1,vul2,vul3,vul4.vul5]
    '''
    #查询模型id
    modelid=user_db_op.get_user_model_by_id(userid)

    print(modelid)
    #画像模型查询到后得到画像的信息
    if modelid != "None":
        #获得画像模型信息
        modelid_info=usermodel_db_op.get_model(modelid)

        #更新历史数据
        usermodel_db_op.model_add_tag(modelid,tagid)
        print(modelid_info)

        #解析信息
        vuls=modelid_info[1]
        cnt=modelid_info[2]
        other=modelid_info[3]

        #进行更新检查
        check_update_model(modelid,vuls,cnt,other)

        #返回要重点保护的对象
        return vuls
    else:
        return None


def do_once_process(userid,tagid):
    '''
    做一次操作，主要为上面函数的操作集合
    :param userid: 用户id
    :param tagid: 页面标签id
    :return: vuls
    '''

    #先更新用户表
    add_new_record(userid,tagid)
    #再获得防护策略
    vuls=get_protect_policy(userid,tagid)

    return vuls

if __name__ == '__main__':
    # add_new_record(12345,21)
    # print(get_protect_policy(12345))
    # usermodel_db_op.main()
    do_once_process(12345,12)
