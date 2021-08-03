import requests
from bs4 import BeautifulSoup
import os, time


class Book:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            'Referer': 'http://www.shicimingju.com/book/',
        }

    # 获取html
    def get_html(self, url):
        result = requests.get(url=url, headers=self.headers)
        return BeautifulSoup(result.text, 'lxml')

    # 获取四本书的url和书名
    def get_books(self, html):
        books = {}
        div = html.findAll("div", class_="book-item")
        for contents in div:
            book_name = contents.get_text().replace("\n", "")
            book_url = 'http://www.shicimingju.com' + contents.a['href']
            books[book_name] = book_url
        return books


    # 获取书目录
    def get_book_mulu(self,books_html):
        book_mulu_urls = []
        mulus = books_html.findAll("div", class_="book-mulu")
        for mulu in mulus:
            mulu_herfs = mulu.findAll('a')
            for mulu_herf in mulu_herfs:
                mulu_herf = 'http://www.shicimingju.com' + mulu_herf['href']
                book_mulu_urls.append(mulu_herf)
        return book_mulu_urls

    # 获取目录正文内容
    def book_mulu_content(self, book_mulu_html):
        book_texts = {}
        title = book_mulu_html.find("div", class_="card bookmark-list")
        mulu_title = title.h1.string     # 章节name
        mulu_contents = book_mulu_html.findAll('div', class_="chapter_content")
        for text in mulu_contents:
            text = text.get_text()  # 正文内容
            book_texts[mulu_title] = text
        return book_texts

    # 保存到本地
    def save_book(self, book_texts, book_name):
        if not os.path.exists(book_name):  # 判断目录存不存在，不存在就创建一个
            os.makedirs(book_name)
        for title in book_texts:
            file_path = book_name + '/' + title
            with open(file_path+'.text', 'a', encoding='utf-8')as f:
                f.write(book_texts[title])
                print('【%s】--章节下载成功！' % title)

    # 功能模块
    def func(self, url):
        books = self.get_books(self.get_html(url))
        for book_name in books:
            time.sleep(1)
            for book_mulu_url in self.get_book_mulu(self.get_html(books[book_name])):
                book_texts = self.book_mulu_content(self.get_html(book_mulu_url))
                self.save_book(book_texts,book_name)


if __name__ == '__main__':
    data = Book()
    data.func('http://www.shicimingju.com/bookmark/sidamingzhu.html')
