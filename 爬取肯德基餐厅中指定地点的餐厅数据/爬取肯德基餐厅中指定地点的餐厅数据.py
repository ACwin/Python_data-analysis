import requests
import json
#1.指定url
url = 'http://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=keyword'

#2.处理url携带的参数，并封装到字典中
word = input('请输入地区：')

data = {
    'cname':'',
    'pid':'',
    'keyword':word,
    'pageIndex':'1',
    'pageSize':'10',
}
#3.进行UA伪装
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
}

#发起post请求

KFC_text = requests.post(url=url, data=data, headers=headers).json()
#6.持久化存储
fileName = word + '_KFC.json'
fp = open(fileName, 'w', encoding = 'utf-8')
json.dump(KFC_text, fp = fp, ensure_ascii = False)

print('over!')