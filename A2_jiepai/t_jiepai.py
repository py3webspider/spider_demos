# coding: utf-8
"""
@author: Evan
@time: 2019/12/30 15:44
"""
import requests
import time
import re
import os

from urllib.parse import urlencode
from requests import codes
from hashlib import md5
from multiprocessing.pool import Pool


def get_page(offset):
    # ajax方式请求页面，返回json数据
    headers = {
        'cookie': 'tt_webid=6775370412135581191; s_v_web_id=a6e5268aafeb77b631f16d5594066da0; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6775370412135581191; __tasessionId=6lk9rx4qk1577757865050',
        'referer': 'https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }

    param = {
        'aid': 24,
        'app_name': 'web_search',
        'offset': offset,
        'format': 'json',
        'keyword': '街拍',
        'autoload': 'true',
        'count': 20,
        'en_qc': 1,
        'cur_tab': 1,
        'from': 'search_tab',
        'pd': 'synthesis',
        'timestamp': int(time.time()*1000)
    }

    base_url = 'https://www.toutiao.com/api/search/content/?'
    url = base_url + urlencode(param)
    try:
        resp = requests.get(url, headers=headers)
        if resp.status_code == codes.ok:
            return resp.json()
    except requests.ConnectionError:
        return None


def parse_images(json):
    # 解析json数据，获取图片和标题，利用生成器爬取数据
    if json.get('data'):
        data = json.get('data')
        for item in data:
            if not item.get('title'):
                continue
            title = item.get('title')
            if not item.get('image_list'):
                continue
            images = item.get('image_list')
            for image in images:
                origin_image = re.sub('list.*?pgc-image', 'origin/pgc-image', image.get('url'))
                if 'list/190x124' in origin_image:
                    continue
                yield {
                    'image': origin_image,
                    'title': title
                }


def save_images(item):
    # 保存图片: 在当前文件夹下的image/
    print(item)
    img_path = 'image/'
    if not os.path.exists(img_path):
        os.makedirs(img_path)
    resp = requests.get(item.get('image'))
    if resp.status_code == codes.ok:
        title = re.sub('[/:*?"<>|\\\]', '', item['title'])
        file_path = '{}xx_{}.{}'.format(title[:10], md5(resp.content).hexdigest()[:6], 'jpg')
        full_path = img_path + file_path
        if not os.path.exists(full_path):
            with open(full_path, 'wb') as fw:
                fw.write(resp.content)
            print('Downloaded image path is %s' % full_path)
        else:
            print('Already Downloaded', full_path)


def main(offset):
    json = get_page(offset)
    if json:
        for item in parse_images(json):
            save_images(item)


GROUP_START = 0
GROUP_END = 20

if __name__ == '__main__':
    pool = Pool()
    groups = ([x*20 for x in range(GROUP_START, GROUP_END)])
    pool.map(main, groups)

    pool.close()
    pool.join()
