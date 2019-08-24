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
# fileName:user_db_op 
# project: Fish_learning
# author: theo_hui
# e-mail:Theo_hui@163.com
# purpose: 用户数据库操作
#          user数据库 记录 用户id 模型对应id,总浏览记录数，各个浏览标签记录数
# creatData:2019/6/3

import sqlite3

# #tags:
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
#              57:[1,9,63],#生活类
#              58:[18,64,65,66],#科技类
#              59:[57,58],#家庭类
#              50:[14,56],#其他兴趣类
#              }

#所有的tagid
ALL_TAG=[00,
       11,12,13,14,15,
       21,22,
       31,32,
       41,42,43,
       50,51,52,53,54,55,56,57,58,59]


#创建原始的用户数据库
#| userid |modelid|h_count|
#tag                    |tag00|
#                       |tag11|tag12|.....|tag59|
def create_db():

    '''创建一个数据库，文件名'''
    conn = sqlite3.connect('./user_portrait/db_op/database/users.db')
    # '''创建游标'''
    cursor = conn.cursor()

    # '''执行语句'''

    sql = '''create table users (
            userid int PRIMARY KEY,modelid text,
            h_count int,
            tag00 int default 0,
            tag11 int default 0,tag12 int default 0,tag13 int default 0,tag14 int default 0,tag15 int default 0,
            tag21 int default 0,tag22 int default 0,
            tag31 int default 0,tag32 int default 0,
            tag41 int default 0,tag42 int default 0,tag43 int default 0,
            tag50 int default 0,tag51 int default 0,tag52 int default 0,tag53 int default 0,tag54 int default 0,
            tag55 int default 0,tag56 int default 0,tag57 int default 0,tag58 int default 0,tag59 int default 0
            )'''

    cursor.execute(sql)

    # # '''使用游标关闭数据库的链接'''
    cursor.close()



def add_usr(usr_id,model_id_str="None",h_count=0):
    '''
    插入新的用户
    :param usr_id: 用户的id
    :param model_id: 用户的模型id
    :param h_count: 用户的历史浏览次数
    :return:
    '''
    conn = sqlite3.connect('./user_portrait/db_op/database/users.db')
    cursor = conn.cursor()

    sql="insert into users (userid,modelid,h_count)values(:u_userid,:u_modelid,:u_h_count)"

    cursor.execute(sql,{'u_userid':usr_id,'u_modelid':model_id_str,'u_h_count':h_count})

    conn.commit()

    print("添加用户",usr_id,"成功")
    cursor.close()

def get_user_by_id(user_id):
    '''
    通过用户的id查询用户信息
    :param user_id:
    :return: 用户信息 (用户id,模型id,历史浏览次数）
    '''
    conn = sqlite3.connect('./user_portrait/db_op/database/users.db')
    cursor = conn.cursor()

    sql ="select * from users where userid = (:u_userid)"
    rst=cursor.execute(sql,{'u_userid':user_id})

    user=rst.fetchone()

    print("查询到数据",user)

    cursor.close()

    return user

def get_user_count_by_id(user_id):
    '''
    通过用户的id查询用户的浏览数据信息
    :param user_id:
    :return: 历史浏览次数
    '''
    conn = sqlite3.connect('./user_portrait/db_op/database/users.db')
    cursor = conn.cursor()

    sql ="select h_count from users where userid = (:u_userid)"
    rst=cursor.execute(sql,{'u_userid':user_id})

    count=rst.fetchone()[0]

    print("查询到数据",count)

    cursor.close()

    return count

def get_user_model_by_id(user_id):
    '''
    通过用户的id查询用户的对应
    :param user_id:
    :return: 画像模型id
    '''
    conn = sqlite3.connect('./user_portrait/db_op/database/users.db')
    cursor = conn.cursor()

    sql ="select modelid from users where userid = (:u_userid)"
    rst=cursor.execute(sql,{'u_userid':user_id})

    rst=rst.fetchone()
    model=None
    if rst:
        model=rst[0]

    print("查询到数据",model)

    cursor.close()

    return model


def del_user(user_id):
    '''
    删除用户
    :param user_id: 用户的id
    :return:
    '''
    conn = sqlite3.connect('./user_portrait/db_op/database/users.db')
    cursor = conn.cursor()

    sql = "delete from users where userid=(:u_userid)"
    cursor.execute(sql, {'u_userid': user_id})

    print("删除用户",user_id)

    conn.commit()
    cursor.close()

def add_user_tag(user_id,tagid):
    '''
    增加用户的浏览记录
    :param user_id: 用户的id
    :param add_num: 要增加的数量
    '''
    #非法tag
    if tagid not in ALL_TAG:
        return

    #构造tag名字
    if tagid==0:
        tagname="tag00"
    else:
        tagname="tag"+str(tagid)

    #数据库插入
    conn = sqlite3.connect('./user_portrait/db_op/database/users.db')
    cursor = conn.cursor()

    tagadd=tagname+"="+tagname+"+1"
    sql = "update users set h_count=h_count+1,"+tagadd+" where userid=(:u_userid)"

    cursor.execute(sql, {'u_userid': user_id})

    print("用户",user_id,"浏览数据增加",tagid)

    conn.commit()
    cursor.close()

def change_model(user_id,model_id):
    '''
    修改用户对应的模型
    :param user_id: 用户的id
    :param model_id: 要修改成为的模型id
    '''
    conn = sqlite3.connect('./user_portrait/db_op/database/users.db')
    cursor = conn.cursor()

    sql = "update users set modelid=(:u_modelid) where userid=(:u_userid)"
    cursor.execute(sql, {'u_modelid': model_id, 'u_userid': user_id})

    print("用户", user_id, "模型修改成功", model_id)

    conn.commit()
    cursor.close()

if __name__ == '__main__':
    #create_db()
    add_usr(1,"2",0)
    add_user_tag(1,53)

    change_model(1,"3")
    get_user_by_id(1)
    del_user(1)