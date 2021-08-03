# -*- coding: utf-8 -*-
import requests
from lxml import etree

if __name__ == '__main__':
    #爬取页面源码数据
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'
    }
    url='https://cdata.58.com/ershoufang/'
    page_text = requests.get(url=url,headers=headers).text

    #数据解析
    tree = etree.HTML(page_text)
    #li标签对象列表
    li_list=tree.xpath('//ul[@class="house-list-wrap"]/li')
    #print(li_list)
    fp = open('58.txt','w',encoding='utf-8')
    for li in li_list:
        #./表示li标签   不加.表示的是根标签
        title = li.xpath('./div[2]/h2/a/text()')[0]
        # 房屋部分数据
        baseinfo= li.xpath('./div[2]/p/span/text()')
        #从列标中取出数据，这种方式总觉得不太好，望指正
        data = baseinfo[0]+'\t'+baseinfo[1]+'\t'+baseinfo[2]
        #价格
        price = li.xpath('./div[3]/p[2]/text()')[0]
        print(title+'\n'+data+'\n'+price+'\n\n')
        fp.write(title+'\n'+data+'\n'+price+'\n\n')



