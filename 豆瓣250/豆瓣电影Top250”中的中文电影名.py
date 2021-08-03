import random
import time

import bs4
import requests

for page in range(10):
    resp = requests.get(
        url=f'https://movie.douban.com/top250?start={page * 25}',
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/83.0.4103.97 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;'
                      'q=0.9,image/webp,image/apng,*/*;'
                      'q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        },
    )
    soup = bs4.BeautifulSoup(resp.text, 'lxml')
    elements = soup.select('.info>div>a')
    for element in elements:
        span = element.select_one('.title')
        print(span.text)
    time.sleep(random.random() * 5)
