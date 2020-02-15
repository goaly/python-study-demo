import requests
from lxml import  etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

res = requests.get('https://book.douban.com/top250', headers=headers)
html = etree.HTML(res.text)
result = etree.tostring(html)
print(result)