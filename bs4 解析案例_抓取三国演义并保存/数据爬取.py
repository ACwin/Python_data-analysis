# -*- coding: utf-8 -*-
# bs4 解析案例
import lxml
import requests
from bs4 import BeautifulSoup
if __name__ == '__main__':
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'
}
    #爬取首页信息
    url='http://www.shicimingju.com/book/sanguoyanyi.html'
    page_text=requests.get(url=url,headers=headers).text

    #在首页中解析出章节标题和详情页的url
    #1、实例化BeautifulSoup对象
    soup=BeautifulSoup(page_text,'lxml')
    #2、解析章节标题和url
    li_list = soup.select('.book-mulu > ul > li')
    #文本文件相关
    fp = open('./三国演义.txt','w',encoding='utf-8')
    for li in li_list:
        title=li.a.string
        detail_url='http://www.shicimingju.com'+li.a['href']
        #对详情页进行请求
        detail_page_text=requests.get(url=detail_url,headers=headers).text
        #解析出详情页中的相关的章节内容
        detail_soup=BeautifulSoup(detail_page_text,'lxml')
        div_tag=detail_soup.find('div',class_='chapter_content')
        #解析出的章节内容
        content=div_tag.text
        fp.write(title+':'+'\n'+content+'\n')
        print(title,"获取成功")
    print("三国演义爬取完成")





