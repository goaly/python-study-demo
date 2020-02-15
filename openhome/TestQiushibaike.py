import requests
import re
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

#初始化列表，用于装入爬虫数据
info_lists = []


def judgement_sex(class_name):
    if class_name == ['womenIcon']:
        return '女'
    else:
        return '男'


def get_info(url):
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
        info_lists.append(info)


if __name__ == '__main__':
    urls = ['https://www.qiushibaike.com/8hr/page/{}/'.format(str(i)) for i in range(1, 36)]
    for url in urls:
        print('url:'+url)
        get_info(url)
        time.sleep(1)

    # 遍历列表，创建TXT文件
    for info_list in info_lists:
        f = open('D:/360极速浏览器下载/qiushi.txt', 'a+')
        try:
            f.write(info_list['id'] + '\n')
            f.write(info_list['level'] + '\b')
            f.write(info_list['sex'] + '\n')
            f.write(info_list['content'] + '\n')
            f.write(info_list['laugh'] + '\n')
            f.write(info_list['comment'] + '\n\n')
        except UnicodeEncodeError:
            print(UnicodeEncodeError.reason)
            pass  # pass 掉错误
