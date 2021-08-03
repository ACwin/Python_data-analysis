# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
import re
import urllib.request, urllib.error
import xlwt
import sqlite3


def main():
    baseurl = "https://movie.douban.com/top250?start="
    datalist = getData(baseurl)
    savepath = "豆瓣电影Top250.xls"
    # 保存数据
    saveData(datalist, savepath)
    # askURL("https://movie.douban.com/top250?start=0")


# 定义全局变量
# 获取影片详情链接的规则
findLink = re.compile(r'<a href="(.*?)">')  # 创建正则表达式对象，表示规则（字符串的模式）
# 影片图片
findImaSrc = re.compile(r'<img.*src="(.*?)"', re.S)  # re.S让换行符包含在字符中
# 影片片名
findTitle = re.compile(r'<span class="title">(.*)</span>')
# 影片的评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
# 找到评价人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')
# 找到概况
findIng = re.compile(r'<span class="inq">(.*)</span>')
# 找到影片的相关内容
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)


# 爬取网页
def getData(baseurl):
    datalist = []
    for i in range(0, 10):  # 调用获取页面信息的函数10次
        url = baseurl + str(i * 25)
        html = askURL(url)  # 保存已经获取到的网页源码
        # 2，逐一解析数据
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="item"):  # 查找符合要求的字符串，形成列表
            # print(item)                                 #测试：查看电影item全部信息
            data = []  # 保存一部电影的所有信息
            item = str(item)  # 将其转化为字符串

            # 获取影片详情的链接
            link = re.findall(findLink, item)[0]  # re库用来通过正则表达式查找指定的字符串（这里查找的是电影的链接）
            data.append(link)  # 在列表中追加link

            imgSrc = re.findall(findImaSrc, item)[0]
            data.append(imgSrc)  # 追加图片

            titles = re.findall(findTitle, item)  # 片名可能只有一个中文名，也有可能另外一个外国名

            if (len(titles) == 2):  # 同时拥有中文名字和外国名字
                ctitle = titles[0]
                data.append(ctitle)  # 追加中文名字
                otitle = titles[1].replace("/", "")  # 获取外国名的时候将前的’/‘替换为空（去掉无关的符号）
                data.append(otitle)  # 追加外文名字
            else:
                data.append(titles[0])  # 一个或多个只添加第一个名字
                data.append(' ')  # 留空，占位

            rating = re.findall(findRating, item)[0]
            data.append(rating)  # 添加评分

            judgeNum = re.findall(findJudge, item)[0]
            data.append(judgeNum)  # 添加评论人数

            inq = re.findall(findIng, item)
            if len(inq) != 0:
                inq = inq[0].replace("。", "")  # 去掉句号
                data.append(inq)  # 添加概述
            else:
                data.append(" ")  # 如果概述为空，则添加为空

            bd = re.findall(findBd, item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?', " ", bd)  # 去掉<br/>
            bd = re.sub('/', " ", bd)  # 用空格替代/
            data.append(bd.strip())  # 去掉内容的前后的空格

            datalist.append(data)  # 把处理好的一部电影的信息放入datalist中

    # print(datalist)
    return datalist


# 得到指定一个url的网页内容
def askURL(url):
    # 模拟浏览器头部信息，向豆瓣服务器发送消息
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"}
    # 用户代理，表示告诉豆瓣服务器，我们是什么样的浏览器，本质上是告诉服务器我们可以接受什么水平的文件内容
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


# 3，保存数据
def saveData(datalist, savepath):
    print("save....")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True)
    col = ("电影详情链接", "图片链接", "影片中文名", "影片外国名", "评分", "评价人数", "概述", "相关信息")
    for i in range(0, 8):
        sheet.write(0, i, col[i])  # 列名
    for i in range(0, 250):
        print("第%d条" % (i + 1))  # 打印进度
        data = datalist[i]
        for j in range(0, 8):
            sheet.write(i + 1, j, data[j])  # 数据
    book.save(savepath)  # 保存


if __name__ == "__main__":
    # 调用函数
    main()
    print("报告！爬取完毕")

