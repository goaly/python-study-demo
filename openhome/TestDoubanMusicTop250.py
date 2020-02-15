# 爬取豆瓣音乐TOP250的数据，并将数据存储到MongoDB数据库中

# 导入相应的库文件
import requests
from lxml import etree
import re
import pymongo
import time

# 连接数据库及创建据库、数据集合
# client = pymongo.MongoClient(host=['mongodb://root:452016@localhost:27018'])
client = pymongo.MongoClient('localhost', 27018)
db_auth = client.admin
db_auth.authenticate("root", "452016")
mydb = client['lys']
musictop = mydb['musictop']
# user = mydb['user']
# thyme = user.find({"username":"thyme"})
# for rec in thyme:
#     print(rec)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}


# 定义获取当前页面内豆瓣音乐的详情URL的函数
def get_url_music(url):
    html = requests.get(url, headers=headers)
    selector = etree.HTML(html.text)
    music_hrefs = selector.xpath('//a[@class="nbg"]/@href')
    for music_href in music_hrefs:
        get_music_info(music_href)


# 定义获取音乐的详情的函数
def get_music_info(url):
    html = requests.get(url, headers=headers)
    selector = etree.HTML(html.text)
    name = selector.xpath('//*[@id="wrapper"]/h1/span/text()')[0]
    author = re.findall('表演者:.*?>(.*?)</a>', html.text, re.S)[0]
    styles = re.findall('<span class="pl">流派:</span>&nbsp;(.*?) <br />', html.text, re.S)
    if len(styles) == 0:
        style = '未知'
    else:
        style = styles[0].strip()
    pubTime = re.findall('<span class="pl">发行时间:</span>&nbsp;(.*?)<br />', html.text, re.S)[0].strip()
    publishers = re.findall('出版者:.*?>&nbsp;(.*?)<br />', html.text, re.S)
    if len(publishers) == 0:
        publisher = '未知'
    else:
        publisher = publishers[0].strip()
    score = selector.xpath('//*[@id="interest_sectl"]/div/div[2]/strong/text()')[0]

    createdOn = time.strftime("%Y-%m-%d %H:%M:%S")
    info = {'name': name, 'author': author, 'style': style, 'pubTime': pubTime, 'publisher': publisher, 'score': score, 'url': url, 'createdOn': createdOn}
    #插入数据
    musictop.insert(info)


if __name__ == '__main__':
    urls = ['https://music.douban.com/top250?start={}'.format(str(i)) for i in range(0, 250, 25)]
    for url in urls:
        get_url_music(url)
        time.sleep(2)
