import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}
res = requests.get('http://bj.xiaozhu.com/', headers=headers)
try:
    # print(res)
    # print(res.text)
    soup = BeautifulSoup(res.text, 'html.parser')
    # price = soup.select('#page_list > ul > li:nth-of-type(1) > div.result_btm_con.lodgeunitname > span.result_price > i')
    # print(price)
    prices = soup.select('#page_list > ul > li > div.result_btm_con.lodgeunitname > span.result_price > i')
    for price in prices:
        print(price.get_text())
except ConnectionError:
    print('拒绝连接')
