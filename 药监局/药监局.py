import re
import requests
import json

# 首页中对应的企业信息数据是通过ajax动态请求到的
if __name__== "__main__":
    url ='http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsList'
    data = {
        'on': 'true',
        'page':'2',
        'pageSize': '15',
        'productName': '',
        'conditionType': '1',
        'applyname': '',
        'applysn': '',

    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
    }
    id_list = [] #存储企业的id
    all_data_list = [] # 存储所有的企业详情数据
    json_ids = requests.post(url=url,headers=headers,data=data).json()
    for dic in json_ids['list']:
       id_list.append(dic['ID'])

    # 获取企业详情数据
       post_url = 'http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsById'
       for id in id_list:
            data = {
                'id' : id
            }
            datail_json = requests.post(url=post_url,headers=headers,data=data).json()
            #print(datail_json)
            all_data_list.append(datail_json)
    # 持久化存储
    fp = open('./allData.json','w',encoding='utf-8')
    json.dump(all_data_list,fp=fp,ensure_ascii=False)
    print('over')