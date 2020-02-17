import requests
import re
from bs4 import BeautifulSoup

# 定义请求头
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 '
                  'Safari/537.36'
}

res = requests.get('http://bj.xiaozhu.com/', headers=headers)
try:
    # print(res)
    print(res.text)
    soup = BeautifulSoup(res.text, 'html.parser')

    print('==============================soup.select')
    # price = soup.select('#page_list > ul > li:nth-of-type(1) > div.result_btm_con.lodgeunitname > div:nth-of-type(
    # 1) > span.result_price > i') print(price)
    prices = soup.select('#page_list > ul > li > div.result_btm_con.lodgeunitname > div:nth-of-type(1) > '
                         'span.result_price > i')
    for i, price in enumerate(prices):
        print(i, ' ', price.get_text())

    print('==============================re.findall')
    # 正则表达式查找
    prices = re.findall('<span class="result_price">&#165;<i>(.*?)</i>', res.text)
    for i, price in enumerate(prices):
        print(i, ' ', price)
except ConnectionError:
    print('拒绝连接')
