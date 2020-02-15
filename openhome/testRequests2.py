from bs4 import BeautifulSoup
import requests
import time  # 导入相应的库文件

# 定义请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}


def judgement_sex(class_name):
    if class_name == ['member_icol']:
        return '女'
    else:
        return '男'


def get_links(url):
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    links = soup.select('#page_list > ul > li > a')  # links为url列表
    for link in links:
        href = link.get('href')
        get_info(href)


def get_info(url):
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    titles = soup.select('div.pho_info > h4')
    addresses = soup.select('span.pr5')
    prices = soup.select('#pricePart > div.day_l > span')
    imgs = soup.select('#floatRightBox > div.js_box.clearfix > div.member_pic > a > img')
    names = soup.select('#floatRightBox > div.js_box.clearfix > div.w_240 > h6 > a')
    sexs = soup.select('#floatRightBox > div.js_box.clearfix > div.w_240 > h6 > a')

    for title, address, price, img, name, sex in zip(titles, addresses, prices, imgs, names, sexs):
        # 获取信息并通过字典的信息打印
        data = {'title': title.get_text().strip(), 'address': address.get_text().strip(), 'price': price.get_text(),
                'img': img.get('src'), 'name': name.get_text(), 'sex': judgement_sex(sex.get('class'))}
        print(data)


if __name__ == '__main__':  # 为程序的主入口
    # 构造多页URL
    urls = ['http://bj.xiaozhu.com/search-duanzufang-p{}-0/'.format(number) for number in range(1, 14)]
    for single_url in urls:
        get_links(single_url)  # 循环调用get_links函数
        time.sleep(2)  # 睡眠2秒
