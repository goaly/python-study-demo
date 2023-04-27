import requests
from lxml import etree
import re
import pymysql
import time

conn = pymysql.connect(host='localhost', user='root', passwd='Al4g56', db='dailylog', port=3306, charset='utf8')
# 连接数据库及光标
cursor = conn.cursor()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}


def get_movie_url(pgUrl):
    html = requests.get(pgUrl, headers=headers)
    selector = etree.HTML(html.text)
    movie_hrefs = selector.xpath('//div[@class="hd"]/a/@href')
    for movie_href in movie_hrefs:
        print(movie_href)
        get_movie_info(movie_href) # 调用获取详细页信息的函数


def get_movie_info(mvUrl):
    html = requests.get(mvUrl, headers=headers)
    selector = etree.HTML(html.text)
    try:
        name = selector.xpath('//*[@id="content"]/h1/span[1]/text()')[0].strip()
        director = selector.xpath('//*[@id="info"]/span[1]/span[2]/a/text()')[0].strip()
        actors = selector.xpath('//*[@id="info"]/span[@class="actor"]/span[2]')[0]
        actor = actors.xpath('string(.)')
        style = re.findall('<span property="v:genre">(.*?)</span>', html.text, re.S)[0]
        country = re.findall('<span class="pl">制片国家/地区:</span>(.*?)<br/>', html.text, re.S)[0].strip()
        release_time = re.findall('上映日期:</span>.*?>(.*?)</span>', html.text, re.S)[0]
        time = re.findall('片长:</span>.*?>(.*?)</span>', html.text, re.S)[0]
        score = selector.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()')[0]

        # 获取信息插入数据库
        cursor.execute(
            "insert into douban_movie(name,director,actor,style,country,release_time,time,score) values(%s,%s,%s,%s,%s,%s,%s,%s)",
            (str(name), str(director), str(actor), str(style), str(country), str(release_time), str(time), str(score)))
    except IndexError:
        print(IndexError)
        pass  # pass掉IndexError错误


if __name__ == '__main__':
    # 构造urls
    urls = ['https://movie.douban.com/top250?start={}'.format(str(i)) for i in range(0, 250, 25)]
    for url in urls:
        get_movie_url(url)  # 循环获取电影信息
        time.sleep(2)  # 为防止被屏蔽，睡眠2秒
    conn.commit()
