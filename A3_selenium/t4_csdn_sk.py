# coding: utf-8
"""
@author: Evan
@time: 2020-01-08 14:39

优化：直接browser.get(url)的方式，而url从文件/数据结构/数据库中获取
"""
import re
import time

import threading
import json
import requests

from requests.exceptions import RequestException

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

number = 0      # url索引
count = 0       # 计数
url_lst = []    # 列表：存储所有url
url_lst.append('https://blog.csdn.net/Yuyh131/article/details/106574449')
url_lst.append("https://blog.csdn.net/Yuyh131/article/details/103727321")
stop1_url = 'https://blog.csdn.net/yuyh131/article/details/84847178'    # 加载过久url，跳过处理

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')                                           # 设置为无界面模式
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])    # 设置为开发者模式
browser = webdriver.Chrome(options=chrome_options)


wait = WebDriverWait(browser, 10)


def get_one_page(url):
    try:
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/json',
            'Origin': 'null',
            'Referer': 'https://blog.csdn.net/Yuyh131',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    pattern = re.compile('<h4.*?href="(.*?)".*?article-type.*?>(.*?)</span>?(\s+)(.+?)(\s+?)</a>'
                         + '.*?class="date">?(\s+)(.*?)<.*?class="num">(\d+?)</span>'
                         + '.*?class="num">(\d+?)</span>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'url': item[0],
            'date': item[6],
        }


def write_to_file(content):
    with open('result_blog.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(offset):
    url = 'https://blog.csdn.net/Yuyh131/article/list/' + str(offset)
    html = get_one_page(url)
    global url_lst

    for item in parse_one_page(html):
        print(item)
        # write_to_file(item)
        url_lst.append(item.get('url'))


def index_page():
    """
    抓取索引页
    :param url:
    """
    global number
    global count
    while True:
        try:
            number = 0 if number >= len(url_lst) else number
            if url_lst[number].lower() == stop1_url.lower():
                number += 1
                continue
            browser.get(url_lst[number])
            count += 1
            print(count, '’', 'curr_url:', url_lst[number])
            number += 1
            # time.sleep(random.randint(1, 3))
            # 控制次数
            exit() if count >= 6666 else 1
        except TimeoutException:
            index_page()


if __name__ == '__main__':
    page = 5
    for i in range(1, page+1):
        main(offset=i)
        time.sleep(4)

    thread = threading.Thread(target=index_page)
    thread.start()
