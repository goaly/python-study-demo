import requests
import re
import time

from lxml import etree
from multiprocessing import Pool  # 导入相应的库文件

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 '
                  'Safari/537.36 '
}

context_path = 'https://www.guozaoke.com'


def judgement_sex(class_name):
    if class_name == ['womenIcon']:
        return '女'
    else:
        return '男'


def xpath_scraper(url):
    print('\nurl:' + url)
    res = requests.get(url, headers=headers)
    html = etree.HTML(res.text)
    topic_items = html.xpath('//div[@class="topic-item"]')
    for item in topic_items:
        node = item.xpath('div[@class="main"]/div[@class="meta"]/span[@class="node"]/a/text()')[0]
        user_name = item.xpath('div[@class="main"]/div[@class="meta"]/span[@class="username"]/a/text()')[0]
        title = item.xpath('div[@class="main"]/h3[@class="title"]/a/text()')[0]
        link = context_path + item.xpath('div[@class="main"]/h3[@class="title"]/a/@href')[0]
        print('【%s】' % node, title, 'by', user_name, link)


if __name__ == '__main__':
    urls = ['https://www.guozaoke.com/?tab=latest&p={}'.format(str(i)) for i in range(1, 5)]

    # start_1 = time.time()
    # for url in urls:
    #     xpath_scraper(url)  # 单进程
    # end_1 = time.time()
    # print('串行爬虫', end_1 - start_1)

    # start_2 = time.time()
    # pool = Pool(processes=2)  # 2个进程
    # pool.map(xpath_scraper, urls)
    # end_2 = time.time()
    # print('2个进程', end_2 - start_2)

    start_3 = time.time()
    pool = Pool(processes=4)  # 4个进程
    pool.map(xpath_scraper, urls)
    end_3 = time.time()
    print('4个进程', end_3 - start_3)
