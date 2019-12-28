# coding: utf-8
"""
@author: Evan
@time: 2019/12/28 14:48
"""
# -*- coding: utf-8 -*-
import requests
import json
import time
import re
from urllib.parse import urlencode

base_url = 'https://www.toutiao.com/api/search/content/?'

image_path = 'E:\sp2\ '
count = 0


def get_search_page(offset):
    query_parameter = {'aid': 24, 'app_name': 'web_search', 'offset': offset, 'format': 'json', 'keyword': '街拍 图集',
        'autoload': 'true', 'count': '20', 'en_qc': '1', 'cur_tab': '1', 'from': 'search_tab', 'pd': 'synthesis',
        'timestamp': int (time.time () * 1000)}
    # 发起一次Ajax请求，一次请求大概返回20篇文章
    search_res = json.loads (requests.get (base_url + urlencode (query_parameter)).text, encoding='utf-8')['data']
    if search_res:
        for page_url in search_res:  # 每一个data成员
            if 'title' in page_url and 'share_url' in page_url:
                yield {'title': page_url['title'], 'url': page_url['share_url']}


def parse_cur_page(url):
    print ('\n', '页面解析ing：', url)
    HEADERS = {
        'cookie': 'tt_webid=6775370412135581191; s_v_web_id=a6e5268aafeb77b631f16d5594066da0; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6775370412135581191; __tasessionId=0sup5ivk21577519315526',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'referer': 'https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D+%E5%9B%BE%E9%9B%86',
        'content-type': 'application/x-www-form-urlencoded'
        }
    response = requests.get (url, headers=HEADERS)  # 如果不加HEADERS，response.text为空
    if (response.status_code == 200):
        print ('解析页面响应正常')
        pattern = re.compile ('gallery: JSON.parse\((.*?)\),', re.S)
        print ('解析当前页面中的图片集ing')
        images = re.search (pattern, response.text)
        if (images == None):
            print ("文章类型不对，没有找到图片集合", url)
            return None
        images = json.loads (images.group (1))
        # 本来是应该使用json直接解析出images，但试过后发现不对，解析异常，
        # 所以最后还是使用正则解析出图片真正的url
        pattern = re.compile ('{"url":"(.*?)",.*?uri', re.S)
        res = re.findall (pattern, images)
        for image_url in res:
            image_url = image_url.replace ('\/', '/')
            print (image_url)
            yield image_url
    else:
        print ('response 异常')


def save_image(url):
    print ('保存图片：')
    global count
    count = count + 1
    response = requests.get (url)

    if response.status_code == 200:
        with open (image_path + str (count) + ".jpg", 'wb') as f:
            f.write (response.content)
            f.close ()


def main():
    for i in range(0, 20):  # 解析20组
        for page in get_search_page(20 * i):  # 处理每次Ajax请求返回的文章链接
            for image_url in parse_cur_page (page["url"]):  # 提取每篇文章中的图片
                save_image(image_url)


if __name__ == '__main__':
    main ()
