from lxml import etree
import requests
import random
import time
import csv
import re
headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
    'cookie' : 'll="118088"; bid=yiGUey7WS7s; _vwo_uuid_v2=D84F02149AA36D0B6FA4F41B29BFC8A53|ba693980c9f906e4f903392f22cfdea4; gr_user_id=bd3c8d92-11df-4592-92b2-88e7c29d4131; viewed="21371175_34985248_34893628_34861737_33385402_1454809"; __gads=ID=f8e6531ebdf6b4f6-225dba1f51c50016:T=1608771142:RT=1608771142:S=ALNI_MZD_cEsfbC7rqyS1kxPf34UWKoQhg; douban-fav-remind=1; dbcl2="238045093:HrICBFdes2U"; push_noty_num=0; push_doumail_num=0; __utmv=30149280.23804; ck=0dzK; ap_v=0,6.0; __utma=30149280.1338646787.1605867382.1623200072.1623322686.33; __utmb=30149280.0.10.1623322686; __utmc=30149280; __utmz=30149280.1623322686.33.30.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
    'referer': 'https://movie.douban.com/subject/34841067/comments?percent_type=h&limit=20&status=P&sort=new_score',
}
f = open('你好李焕英_好评_所有字段.csv', 'w', encoding='utf-8-sig', newline="")  # 创建文件对象
csv_write = csv.DictWriter(f, fieldnames=['评论者', '评分等级', '评论日期', '点赞数', '评论内容'])
#csv_write.writeheader()

#定义一个函数，获取评论作者、评论等级、评论日期、点赞数、评论内容

def get_value(tree):
    # 评论作者
    reviewer = tree.xpath("//div[@class='comment-item ']//span[@class='comment-info']/a/text()")
    # 评分等级
    score = tree.xpath("//div[@class='comment-item ']//span[@class='comment-info']/span[2]/@title")
    # 评论日期
    comment_date = tree.xpath("//div[@class='comment-item ']//span[@class='comment-time ']/text()")
    # 点赞数
    vote_count = tree.xpath("//div[@class='comment-item ']//span[@class='votes vote-count']/text()")
    # 评论内容
    comments = tree.xpath("//p[@class=' comment-content']/span/text()")

    # 去除评论日期的换行符及空格
    comment_date = list(map(lambda date: re.sub('\s+', '', date), comment_date))  # 去掉换行符制表符
    comment_date = list(filter(None, comment_date))  # 去掉上一步产生的空元素

    return reviewer, score, comment_date, vote_count, comments
 #定义一个函数，将获取到的数据写入csv文件
def write_csv(reviewer, score, comment_date, vote_count, comments):
    for j in range(20):
        data_dict = {'评论者': reviewer[j], '评分等级': score[j], '评论日期': comment_date[j], '点赞数': vote_count[j],
                     '评论内容': comments[j]}
        csv_write.writerow(data_dict)

#开始爬取前10页豆瓣短评
#指爬取到页面源码数据
for i in range(10): # 为了方便展示，只爬取10页
    url = 'https://movie.douban.com/subject/34841067/comments?percent_type=l&start={}&limit=20&status=P&sort=new_score'.format(i * 20)
    page_text = requests.get(url=url, headers=headers).text
    tree = etree.HTML(page_text)
    reviewer, score, comment_date, vote_count, comments = get_value(tree)
    write_csv(reviewer, score, comment_date, vote_count, comments)
    print('第{}页爬取成功'.format(i + 1))
    time.sleep(random.randint(5, 10))  # 设置睡眠时间间隔
print("---------------")
print("所有评论爬取成功")