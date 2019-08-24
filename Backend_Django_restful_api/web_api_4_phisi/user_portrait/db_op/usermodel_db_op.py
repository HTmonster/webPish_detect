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
# fileName:usermodel_db_op 
# project: Fish_learning
# author: theo_hui
# e-mail:Theo_hui@163.com
# purpose: 对用户(画像）模型数据库的操作
# creatData:2019/6/3、

import sqlite3


#创建原始的用户数据库
# |modelid|
#   |vul1|vul2|vul3|vul4|vul5| 最容易受害的5种类型网页,也是重点保护检测的对象的
#   |cnt1|cnt2|cnt3|cnt4|cnt5| 这5种类型对应的确认检测为恶意的次数 用于动态演变
#   |other|othercnt| 候选的替换 用于动态演变

# modelid编码方式 |57:75|23:10|12:05|11:05|13:05| 代表本画像的人最喜欢访问 57 23 12 11 13这五类网页
#                 所占比例75% 10% 5% 5% 5% 细粒度为 %5

def parse_modelid(modelid):
    '''
    因为模型的id编码方式，所以可以解析出model的信息
    :param modelid: model的ID
    '''
    #转为字符串
    modelid_str=str(modelid)

    #合法判断
    if len(modelid_str)!=20:
        return None

    tag1=int(modelid_str[  : 2]);per1=int(modelid_str[ 2: 4])
    tag2=int(modelid_str[ 4: 6]);per2=int(modelid_str[ 6: 8])
    tag3=int(modelid_str[ 8:10]);per3=int(modelid_str[10:12])
    tag4=int(modelid_str[12:14]);per4=int(modelid_str[14:16])
    tag5=int(modelid_str[16:18]);per5=int(modelid_str[18:20])

    return ([tag1,tag2,tag3,tag4,tag5],[per1,per2,per3,per4,per5])


def buid_modelid(tagNames,tagPers):
    '''
    根据标签构造模型的ID名称
    :param tagNames: 前五位标签名称
    :param tagPers: 前五位标签百分比
    :return: 模型的id 名字
    '''

    modelid_str=""

    for i in range(5):
        modelid_str+=str(tagNames[i]).zfill(2)+str(tagPers[i]).zfill(2)
    print(modelid_str)

    return modelid_str

def parse_other(othernames,othercnts):
    '''
    解析其他对应的数据
    :param othernames: other的名称，字符串 可以解析为列表
    :param othercnts:  other对应类型的数量，字符串，可以解析为列表
    :return: (others,cnts) 双列表
    '''

    try:
        others=list(othernames.split())
        cnts=list(othercnts.split())

        return (others,cnts)
    except:
        return (None,None)

def build_other(others,cnts):
    '''
    通过两个列表构造对应的other字符串 用于压缩存储
    :param others: other的名称，列表
    :param cnts:  other对应类型数量 列表
    :return: (othernames,othercnts) 对应字符串
    '''

    try:
        othernames = " ".join([str(_) for _ in others])
        othercnts = " ".join([str(_) for _ in cnts])

        return (othernames,othercnts)
    except:
        return (None,None)

def create_db():

    '''创建一个数据库，文件名'''
    conn = sqlite3.connect('./database/models.db')
    # '''创建游标'''
    cursor = conn.cursor()

    # '''执行语句'''

    sql = '''create table models (
                modelid text primary key ,
                vul1 int default 0,vul2 int default 0,vul3 int default 0,vul4 int default 0,vul5 int default 0,
                cnt1 int default 0,cnt2 int default 0,cnt3 int default 0,cnt4 int default 0,cnt5 int default 0,
                other text default "",othercnt text default "")'''

    cursor.execute(sql)

    # # '''使用游标关闭数据库的链接'''
    cursor.close()


def add_model(modelid):
    '''
    添加一个新的画像 模型
    :param modelid: 模型ID
    :return:
    '''

    #解析模型ID 根据模型的
    rst=parse_modelid(modelid)
    print(rst)

    #初始化 依据各自的其类型先设置为对应的防护对象

    conn = sqlite3.connect('./user_portrait/db_op/database/models.db')
    cursor = conn.cursor()

    sql = "insert into models (modelid,vul1,vul2,vul3,vul4,vul5)" \
                    "values(:m_modelid,:m_vul1,:m_vul2,:m_vul3,:m_vul4,:m_vul5)"

    cursor.execute(sql, {"m_modelid":modelid,
                         "m_vul1":rst[0][0],
                         "m_vul2":rst[0][1],
                         "m_vul3":rst[0][2],
                         "m_vul4":rst[0][3],
                         "m_vul5":rst[0][4],
                         })

    conn.commit()

    print("添加模型", modelid, "成功")
    cursor.close()

def get_model(modelid):
    '''
    获得模型
    :param modelid:模型的id 为字符串
    :return: 模型的信息 (modelid,[vuls],[cnts],[other,othercnt])
    '''
    conn = sqlite3.connect('./user_portrait/db_op/database/models.db')
    cursor = conn.cursor()

    sql = "select * from models where modelid = (:m_modelid)"
    rst = cursor.execute(sql, {'m_modelid': modelid})

    model = rst.fetchone()

    print("查询到模型数据", model)

    cursor.close()

    return (model[0],model[1:6],model[6:11],model[11:]) if model else None

def model_add_tag(modelid,tagid):
    '''
    为模型增加访问数目
    :param tagid: 目标的便签id
    :return:
    '''

    model_info=get_model(modelid)

    vuls=model_info[1]

    #在top5标签里
    if tagid in vuls:
        index=vuls.index(tagid)

        sql= "update models set vul"+str(index)+"=vul"+str(index)+"+1 where modelid=(:m_modelid)"
    else:
        others,cnts=parse_other(model_info[3])

        if tagid in others:
            index=others.index(tagid)
            cnts[index]+=1
        else:
            others.append(tagid)
            cnts.append(1)
        othernames,othercnts=build_other(others,cnts)

        sql="update models set other="+othernames+" othercnt="+othercnts+" where modelid=(:m_modelid)"

    conn = sqlite3.connect('./user_portrait/db_op/database/models.db')
    cursor = conn.cursor()

    cursor.execute(sql, {'m_modelid': modelid})

    print("模型修改成功", modelid)

    conn.commit()
    cursor.close()

def update_model(modelid,vuls,cnts,other):
    '''
    更新画像模型
    :param modelid: 模型id
    :param vuls: 保护策略
    :param cnts: 保护计数
    :param other: 其他类型存储信息
    :return:
    '''
    print(vuls)

    conn = sqlite3.connect('./user_portrait/db_op/database/models.db')
    cursor = conn.cursor()

    vuls_str="vul1="+str(vuls[0])+",vul2="+str(vuls[1])+",vul3="+str(vuls[2])+",vul4="+str(vuls[3])+",vul5="+str(vuls[4])
    cnts_str="cnt1="+str(cnts[0])+",cnt2="+str(cnts[1])+",cnt3="+str(cnts[2])+",cnt4="+str(cnts[3])+",cnt5="+str(cnts[4])
    other_str="other="+str(other[0])+",othercnt="+str(other[1])

    sql = "update models set "+vuls_str+","+cnts_str+","+other_str+" where modelid=(:m_modelid)"

    cursor.execute(sql, {'m_modelid': modelid})
    print("模型修改成功", modelid)

    conn.commit()
    cursor.close()

def main():
    #add_model("12345678901234567890")
    update_model("12345678901234567890", [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], ["12", "23"])
    print(get_model("12345678901234567890"))

if __name__ == '__main__':
    #create_db()
    #print(parse_other("12 13 14","23 24 25"))
    #print(build_other([1,2,3,4],[2,3,4,5]))
    #print(parse_modelid(12345678901234567890))
    add_model("12345678901234567890")
    update_model("12345678901234567890",[1,2,3,4,5],[1,2,3,4,5],["12","23"])
    print(get_model("12345678901234567890"))