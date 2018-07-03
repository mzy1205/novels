from bs4 import BeautifulSoup
import requests
import urllib
import sys
import re
import datetime

host = 'http://www.biquge.com.tw'

_name = input("请输入书名：")
# _name = '牧神记'
f = open(_name+'.txt', 'w')
_name = urllib.request.quote(_name.encode('gbk'))

search_url = 'http://www.biquge.com.tw/modules/article/soshu.php'
pay_load = {'searchkey' : _name}
search_url = search_url + '?' + 'searchkey=' + _name
r = requests.get(search_url)
r.encoding = 'gbk'
html_doc = r.text

soup = BeautifulSoup(html_doc, 'html.parser')
regexp = re.compile("/(.+?).html")
links = soup.find_all(href=regexp)
novel = ''
# print('开始时间：')
# print(datetime.datetime.now().strftime('%Y-%m-%%d %H:%M:%S'))
for link in links:
    # print('当前链接开始的时间：')
    # print(datetime.datetime.now().strftime('%Y-%m-%%d %H:%M:%S'))
    href = link.get('href')
    href = host + href
    chapter = requests.get(href)
    chapter.encoding = 'gbk'
    chapter_doc = chapter.text
    s_soup = BeautifulSoup(chapter_doc, 'html.parser')
    title = s_soup.find('h1').get_text() + '\r\n'
    content = s_soup.find('div', id='content').get_text() + '\r\n'
    # f.write(title + '\n')
    # f.write(content + '\n')
    novel = novel + title + content

# print('链接循环结束时间，准备写文件：')
# print(datetime.datetime.now().strftime('%Y-%m-%%d %H:%M:%S'))
novel = novel.replace(u'\xa0', u' ')
f.write(novel)
f.close()
# print('写文件结束时间：')
# print(datetime.datetime.now().strftime('%Y-%m-%%d %H:%M:%S'))