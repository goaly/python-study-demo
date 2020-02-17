import requests
from bs4 import BeautifulSoup
import time

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 '
                  'Safari/537.36'
}


def get_info(url):
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')

    ranks = soup.select('span.pc_temp_num')
    titles = soup.select('div.pc_temp_songlist > ul > li')
    times = soup.select('span.pc_temp_tips_r > span')

    for rank, title, time in zip(ranks, titles, times):
        # 获取信息并通过字典的信息打印
        data = {'rank': rank.get_text().strip(), 'singer': title.get('title').split('-')[0].strip(),
                'song': title.get('title').split('-')[1].strip(), 'time': time.get_text().strip()}
        print(data)


if __name__ == '__main__':  # 为程序的主入口，单独运行时，才执行以下代码
    # 构造多页URL
    urls = ['http://www.kugou.com/yy/rank/home/{}-8888.html'.format(str(i)) for i in range(1, 24)]
    for i, single_url in enumerate(urls):
        print('==============酷狗TOP500，第', i + 1, '页===========> get_info(', single_url, ')')
        get_info(single_url)  # 循环调用get_info函数
        time.sleep(1)  # 睡眠1秒
