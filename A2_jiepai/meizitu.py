# coding: utf-8
"""
@author: Evan
@time: 2019/12/29 14:58
"""
import requests
from lxml import etree

Hostreferer = {
    'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Referer':'http://www.mzitu.com'
}
Picreferer = {
    'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Referer':'http://i.meizitu.net'
}


url = 'https://www.mzitu.com/page/{}'


def get_html(url):
    response = requests.get(url,headers=Hostreferer)
    html = response.text
    page = etree.HTML(html)
    title = page.xpath('//ul[@id = "pins"]//li//text()')[::2]
    img_urls = page.xpath('//img[@class ="lazy"]/@data-original')
    print()
    return zip(title, img_urls)


def get_img(url):
    for index, url in get_html(url):
        with open('../images/{}.jpg'.format(index), 'wb+') as f:
            res = requests.get(url, headers=Picreferer)
            f.write(res.content)


if __name__ == '__main__':
    i = int(input('爬几页:'))
    for j in range(1, i+1):
        url = 'https://www.mzitu.com/page/{}'.format(j)
        print('正在爬取第{}页'.format(j))
        get_img(url)

