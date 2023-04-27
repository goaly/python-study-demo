import requests
import csv
from lxml import etree
import time

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 '
                  'Safari/537.36 '
}

fp = open('D:/360极速浏览器下载/pythonBookTop105.csv', 'wt', newline='', encoding='utf-8')
writer = csv.writer(fp)
writer.writerow(('name', 'url', 'author', 'publisher', 'date', 'price', 'rate', 'comment'))

urls = ['https://search.douban.com/book/subject_search?search_text=python&cat=1001&start={}'.format(str(i)) for i in
        range(0, 105, 15)]

for url in urls:
    print('url:' + url)
    # TODO 豆瓣搜索已经改成异步响应，这里请求没有返回结果，需改造
    html = requests.get(url, headers=headers)
    selector = etree.HTML(html.text)
    infos = selector.xpath('//div[@class="item-root"]/div[@class="detail"]')
    for info in infos:
        name = info.xpath('div[@class="title"]/a/text()')[0]
        url = info.xpath('div[@class="title"]/a/@href')[0]
        book_infos = info.xpath('div[@class="meta abstract"]/text()')[0]
        author = book_infos.split('/')[0]
        publisher = book_infos.split('/')[-3]
        date = book_infos.split('/')[-2]
        price = book_infos.split('/')[-1]
        rate = info.xpath('div[2]/span[2]/text()')[0]
        comments = info.xpath('div[2]/span[3]/text()')
        comment = comments[0] if len(comments) != 0 else '空'
        writer.writerow((name, url, author, publisher, date, price, rate, comment))
    time.sleep(1)

fp.close()
