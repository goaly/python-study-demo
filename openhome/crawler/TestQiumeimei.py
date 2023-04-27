import requests
from lxml import etree
import time

# 定义请求头
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 '
                  'Safari/537.36'
}

f = open('D:/360极速浏览器下载/糗妹妹段子.txt', 'a+', encoding="utf-8")


def write_file(texts):
    if texts:
        for text in texts:
            print(text)
            f.write(text + '\n')


def get_info(url):
    res = requests.get(url, headers=headers)
    selector = etree.HTML(res.text)
    url_infos = selector.xpath('//div[@class="panel clearfix"]')
    for info in url_infos:
        title = info.xpath('div[1]/h2/a/text()')[0]
        write_file(['\n\n' + title])

        content = info.xpath('div[@class="main"]/div[2]/p/text()')
        if content:
            write_file(content)
        else:
            content = info.xpath('div[@class="main"]/p/text()')
            if content:
                write_file(content)
            else:
                content = info.xpath('div[@class="main"]/div[2]/text()')
                if content:
                    write_file(content)


if __name__ == '__main__':

    # 爬取糗妹妹上的段子
    urls = ['https://www.qiumeimei.com/text/page/{}'.format(str(i)) for i in range(1, 10)]
    for i, url in enumerate(urls):
        print('=======================第', i + 1, '次爬取糗妹妹上的段子，URL:', url)
        get_info(url)
        time.sleep(7)

f.close()
