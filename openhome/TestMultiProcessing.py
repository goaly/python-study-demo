import requests
import re
import time
from multiprocessing import Pool    #导入相应的库文件

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

def judgement_sex(class_name):
    if class_name == ['womenIcon']:
        return '女'
    else:
        return '男'

def re_scraper(url):
    print('url:' + url)
    res = requests.get(url, headers=headers)
    ids = re.findall('<h2>(.*?)</h2>', res.text, re.S)
    levels = re.findall('<div class="articleGender \D+Icon">(.*?)</div>', res.text, re.S)
    sexs = re.findall('<div class="articleGender (.*?)">', res.text, re.S)
    contents = re.findall('<div class="content">.*?<span>(.*?)</span>', res.text, re.S)
    laughs = re.findall('<span class="stats-vote"><i class="number">(\d+)</i>', res.text, re.S)
    comments = re.findall('<i class="number">(\d+)</i> 评论', res.text, re.S)

    for id, level, sex, content, laugh, comment in zip(ids, levels, sexs, contents, laughs, comments):
        info = {
            'id': id,
            'level': level,
            'sex': judgement_sex(sex),
            'content': content,
            'laugh': laugh,
            'comment': comment
        }
        # print(info)
        return info

if __name__ == '__main__':
    urls = ['https://www.qiushibaike.com/8hr/page/{}/'.format(str(i)) for i in range(1, 36)]

    start_1 = time.time()
    for url in urls:
        re_scraper(url)     #单进程
    end_1 = time.time()
    print('串行爬虫', end_1-start_1)

    start_2 = time.time()
    pool = Pool(processes=2)    #2个进程
    pool.map(re_scraper, urls)
    end_2 = time.time()
    print('2个进程', end_2 - start_2)

    start_3 = time.time()
    pool = Pool(processes=4)  # 4个进程
    pool.map(re_scraper, urls)
    end_3 = time.time()
    print('4个进程', end_3 - start_3)
