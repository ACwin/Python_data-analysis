import urllib.request as request
from urllib import response
import requests


url = 'https://www.sogou.com/web'
kw = input('enter a word:')
param = {
    'query':kw
}
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
}
response = requests.get(url = url, params = param, headers = headers)
page_text = response.text
#print(len(page_text))
fileName = 'kw' + '.html'
with open(fileName, 'w', encoding='utf-8') as fp:
    fp.write(page_text)