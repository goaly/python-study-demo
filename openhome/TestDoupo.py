import requests
import re
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

f=open('D:/360极速浏览器下载/doupo.txt', 'a+')

def get_info(url):
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        # 正则表达式获取文本写入TXT文件中
        contents = re.findall('<p>(.*?)</p>', res.content.decode('utf-8'), re.S)
        for content in contents:
            f.write(content+'\n')
    else:
        pass    #响应状态码不为200就pass掉


if __name__ == '__main__':
    urls = ['http://www.doupoxs.com/doupocangqiong/{}.html'.format(str(i)) for i in range(2, 1665)]
    for url in urls:
        get_info(url)
        time.sleep(1)

f.close()