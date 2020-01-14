# coding: utf-8
"""
@author: Evan
@time: 2020/1/6 15:45

递归太深异常：
RecursionError: maximum recursion depth exceeded while calling a Python object

堆栈溢出异常：
Process finished with exit code -1073741571 (0xC00000FD)
"""
import sys
import threading

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq


start_url = 'https://blog.csdn.net/Yuyh131/article/details/103727321'   # 开始url
end_url = 'https://blog.csdn.net/yuyh131/article/details/81144453'      # 结束url

stop1_url = 'https://blog.csdn.net/yuyh131/article/details/84847178'    # 加载过久url，跳过处理
next1_url = 'https://blog.csdn.net/yuyh131/article/details/84772981'

number = 0      # 计数

# 解决递归过深的问题，默认1000次
sys.setrecursionlimit(1000000)


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')                                           # 设置为无界面模式
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])    # 设置为开发者模式
browser = webdriver.Chrome(options=chrome_options)


wait = WebDriverWait(browser, 10)


def index_page(url):
    """
    抓取索引页
    :param url:
    """
    global prev_url
    global number

    try:
        # 某些加载比较久的链接，做特别处理
        if url == stop1_url:
            prev_url = next1_url
            return index_page(prev_url)

        browser.get(url)
        global number
        number += 1

        prev_url = get_products()
        print(number, '’', 'prev_page：', prev_url)

        # 最后一条链接时重置url、前一条url解析错误也重置url
        if url == end_url or not prev_url:
            prev_url = start_url

        return index_page(prev_url)

    except TimeoutException:
        return index_page(url)


def get_products():
    """
    提取上一页url数据
    """
    try:
        html = browser.page_source
        doc = pq(html)
        items = doc('body > div.tool-box.vertical > ul > li.widescreen-hide > a').items()
        for item in items:
            product = {
                'url': item.attr('href'),
            }
            return product.get('url')
    except Exception:
        return start_url


def main():
    """
    """
    try:
        index_page(start_url)
        browser.close()
    except RecursionError:
        index_page(start_url)


if __name__ == '__main__':
    # 解决堆栈溢出异常问题
    threading.stack_size(200000000)
    thread = threading.Thread(target=main)
    thread.start()

