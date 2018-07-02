from bs4 import BeautifulSoup
import requests
import urllib
import sys
import re

host = 'http://www.biquge.com.tw'

# _name = input("请输入书名：")
_name = '超品相师'
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
for link in links:
    href = link.get('href')
    href += host
    chapter = requests.get(href)
    chapter.encoding = 'gbk'
    chapter_doc = chapter.text
    s_soup = BeautifulSoup(chapter_doc, 'html.parser')





