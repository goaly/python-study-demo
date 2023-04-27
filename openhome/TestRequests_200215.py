import requests
from bs4 import BeautifulSoup

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 '
                  'Safari/537.36'
}

try:
    res = requests.get('http://bj.xiaozhu.com', headers=headers)
    # 对返回结果进行解析，html.parser为python标准解析库
    soup = BeautifulSoup(res.text, 'html.parser')
    # 美化返回结果
    # print(soup.prettify())

    # 获取首页所有价格信息
    prices = soup.select(
        '#page_list > ul > li > div.result_btm_con.lodgeunitname > div:nth-of-type(1) > span > i')
    # 打印价格
    for price in prices:
        print(price.get_text())

except ConnectionError:
    print('拒绝连接')
