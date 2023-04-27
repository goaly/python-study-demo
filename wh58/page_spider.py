# 导入相应的库文件
import requests
from lxml import etree
import pymongo
import time

client = pymongo.MongoClient('localhost', 27018)
db_auth = client.admin
db_auth.authenticate("root", "452016")
mydb = client['lys']
wh58_url = mydb['wh58_url']
wh58_info = mydb['wh58_info']

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Connection': 'keep-alive'
}

#获取商品详情页url的函数
def get_links(channel, pages):

    list_view = '{}pn{}/'.format(channel, str(pages))
    try:
        html = requests.get(list_view, headers=headers)
        time.sleep(2)
        selector =etree.HTML(html.text)

        if selector.xpath('//tr'):
            infos = selector.xpath('//tr')
            for info in infos:
                if info.xpath('td[2]/a/@href'):
                    url = info.xpath('td[2]/a/@href')[0]
                    #插入数据库
                    wh58_url.insert_one({'url':url})
                else:
                    pass #do nothing
        else:
            pass #do nothing
    except requests.exceptions.ConnectionError:
        pass  # pass掉请求连接错误

#获取商品详细信息的函数
def get_info(url):
    html = requests.get(url, headers=headers)
    selector = etree.HTML(html.text)
    try:
        pass
        title = selector.xpath('//h1[@class="info_titile"]/text()')[0]
        if selector.xpath('//span[@class="price_now"]/i/text()'):
            price = selector.xpath('//span[@class="price_now"]/i/text()')[0]
        else:
            price = '无'
        if selector.xpath('//div[@class="palce_li"]/span/i/text()'):
            area = selector.xpath('//div[@class="palce_li"]/span/i/text()')[0]
        else:
            area = '无'
        view = selector.xpath('//p[@class="info_p"]/span[1]/text()')[0]
        if selector.xpath('//p[@class="info_p"]/span[2]/text()'):
            want = selector.xpath('//p[@class="info_p"]/span[2]/text()')[0]
        else:
            want = '无'

        info = {
            'title':title,
            'price':price,
            'area':area,
            'view':view,
            'want':want,
            'url':url
        }
        # 插入数据库
        wh58_info.insert_one(info)
    except IndexError:
        print(IndexError)
        pass  # pass掉IndexError错误