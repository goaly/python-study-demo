import requests
import re
import time
from bs4 import BeautifulSoup

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 '
                  'Safari/537.36'
}

f = open('D:/360极速浏览器下载/斗破苍穹.txt', 'a+')


def get_info(url):
    res = requests.get(url, headers=headers)
    if res.status_code == 200:

        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        title = soup.select_one('body > div.main > div.entry-tit > h1')
        # 章节标题
        f.write('\n\n===================================' + title.get_text() + '===================================\n')
        # 正则表达式获取文本写入TXT文件中
        contents = re.findall('<p>(.*?)</p>', res.content.decode('utf-8'), re.S)
        for content in contents:
            # 去除一些广告
            test1 = re.search('www\.doupoxs\.com', content, re.I)
            if test1 is None:
                test2 = re.search('[\(（].*?(?!收藏|求票票|顶一下).*[\)）]', content, re.I)
                if test2 is None:
                    test3 = re.search('All contents are copyrighted', content, re.I)
                    if test3 is None:
                        f.write(content + '\n')
    else:
        print('=======================HTTP响应失败，PASSED======================')
        pass  # 响应状态码不为200就pass掉


if __name__ == '__main__':

    # 爬取《斗破苍穹》全文小说
    urls = ['http://www.doupoxs.com/doupocangqiong/{}.html'.format(str(i)) for i in range(28, 1665)]
    for i, url in enumerate(urls):
        print('=======================第', i + 1, '次爬取《斗破苍穹》，URL:', url)
        get_info(url)
        time.sleep(10)

f.close()
