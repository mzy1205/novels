from bs4 import BeautifulSoup
import requests
import urllib
import sys
import re
import datetime
import time
import os
import platform

def check_qiut(character):
    if character == 'q':
        exit()

def main(download_name, search_url):
    if download_name is None:
        download_name = input("请输入书名：")

    download_name = 'test'
    check_qiut(download_name)
    temp_downlad = download_name
    download_name = urllib.request.quote(download_name.encode('gbk'))

    if search_url is None:
        search_url = host + '/modules/article/soshu.php'
        search_url = search_url + '?' + 'searchkey=' + download_name

    requests_res = requests.get(search_url)
    requests_res.encoding = 'gbk'
    html_doc = requests_res.text

    soup = BeautifulSoup(html_doc, 'html.parser')
    has_id_content = soup.find('div', id='content')

    if has_id_content is not None:      #有id为content的标签，没找到或者匹配到多个
        tr = soup.select('tr')
        tr_count = len(tr)
        if tr_count == 1:               #没找到
            _name = input("暂未找到该书籍，请重新输入。输入q退出：")
            check_qiut(_name)
            main(download_name=_name, search_url = None)  # 重新查找
            return

        elif tr_count > 1:              #匹配到多个
            tr_novel = soup.select("#nr")
            num = 1
            num_list = []
            num_list.append(num)
            print("共找到" + str(tr_count - 1) + "本匹配的书籍：")

            for s_novel in tr_novel:
                r = s_novel.select("td:nth-of-type(1)")
                print(str(num) + "、" + r[0].get_text() + "\r\n")
                num +=1
                num_list.append(num)

            want_download = input("请输入想下载的序号或输入q退出：")
            check_qiut(want_download)
            
            if int(want_download) in num_list:

                want_download_r = s_novel.select("td:nth-of-type(" + want_download + ")")

                # want_download_r

            else:

                print("输入错误，请重新输入")

                time.sleep(0.1)

                os_type = platform.system()             #操作系统类型。win和linux系统清屏方式不同

                if os_type == 'Windows':

                    os.system('cls')

                else:

                    os.system('clear')

                main(download_name=download_name, search_url=None)



    regexp = re.compile("/(.+?).html")

    links = soup.find_all(href=regexp)
    novel = ''

    for link in links:
        href = link.get('href')
        href = host + href
        chapter = requests.get(href)
        chapter.encoding = 'gbk'
        chapter_doc = chapter.text
        s_soup = BeautifulSoup(chapter_doc, 'html.parser')
        title = s_soup.find('h1').get_text() + '\r\n'
        content = s_soup.find('div', id='content').get_text() + '\r\n'
        novel = novel + title + content

    novel = novel.replace(u'\xa0', u' ')

    f = open(temp_downlad + '.txt', 'w')
    f.write(novel)
    f.close()
    return

host = 'http://www.biquge.com.tw'
main(download_name=None, search_url = None)

