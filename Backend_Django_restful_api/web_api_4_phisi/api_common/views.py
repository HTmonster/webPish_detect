from rest_framework import status
import random
from rest_framework.decorators import api_view
from rest_framework.response import Response

from predictor import total_prediction
from predictor.tools import getPsychologyFeatures
from user_portrait import user_portrait_processor
from api_common.serializers import RecvSerializer,ResponJson_temp

#api接口

@api_view(['GET','POST'])
def api(request):
    '''
    post 提交的data数据：
    ____1. url参数
    ____2. setting参数(1:强提醒 0:弱提醒) 返回判断结果
    ____3. id参数 用户的参数 -1表示不开启

    提交示例(json):

      {"url":"http://www.baidu.com","setting":0,"id":-1}

    返回值: json数据
    ____1. status:状态 (ok:正常 error:错误)
    ____2. result: 判断结果（1：正常 0：钓鱼）
    '''

    #如果是GET请求则提示通过POST提交
    if request.method =='GET':
        return Response({"status":400,"hit":"请通过POST提交"})
    #接受POST请求
    elif request.method == 'POST':

        #接受POST请求
        recv_serializer=RecvSerializer(data=request.data)

        #验证请求合法性
        if recv_serializer.is_valid():

            # 解析参数
            url = recv_serializer.data['url']  # url参数
            setting = recv_serializer.data['setting']  # setting参数
            id=recv_serializer.data['id']  #用户id

            print("解析结果 ", url, "", setting,"",id)


            #如果开启了用户画像定制防御模式
            if id !=-1:
                page_tag=getPsychologyFeatures.get_psychology_features_by_url(url)[1]

                print(page_tag)
                policy_vuls=user_portrait_processor.do_once_process(id,page_tag)

                #如果本次页面在容易受害的名单中
                if policy_vuls is not None and page_tag in policy_vuls:
                    #则设置为强模式
                    setting=1

            #对url进行预测
            url_predict=total_prediction.predict(url,setting)
            print("判决结果",url_predict)

            if url_predict ==1:
                #正常网站
                return Response(ResponJson_temp.normal_json,status.HTTP_200_OK)
            elif url_predict ==0:
                #恶意网站
                return Response(ResponJson_temp.malicious_json,status.HTTP_200_OK)
            else:
                #未知错误
                return Response(ResponJson_temp.unkown_json,status.HTTP_503_SERVICE_UNAVAILABLE)

        #解析不对 返回错误
        return Response(recv_serializer.errors, status.HTTP_400_BAD_REQUEST)