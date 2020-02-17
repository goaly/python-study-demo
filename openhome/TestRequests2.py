from bs4 import BeautifulSoup
import requests
import time  # 导入相应的库文件

# 定义请求头
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 '
                  'Safari/537.36'
}


# 判断性别
def judgement_sex(class_name):
    if class_name == ['member_icol']:
        return '女'
    else:
        return '男'


# 解析每个页面
def get_links(url):
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    # 找到每一页的短租详情链接
    links = soup.select('#page_list > ul > li > a')  # links为短租详情的url列表
    for link in links:
        href = link.get('href')
        # 进入详情，解析数据
        get_info(href)


# 解析每个短租详情链接
def get_info(url):
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    titles = soup.select('div.pho_info > h4')
    addresses = soup.select('span.pr5')
    prices = soup.select('#pricePart > div.day_l > span')
    imgs = soup.select('#floatRightBox > div.js_box.clearfix > div.member_pic > a > img')
    names = soup.select('#floatRightBox > div.js_box.clearfix > div.w_240 > h6 > a')
    sexs = soup.select('#floatRightBox > div.js_box.clearfix > div.member_pic > div')

    # 用zip() 函数将以上不同类别的信息集合打包成一个元组对象
    for title, address, price, img, name, sex in zip(titles, addresses, prices, imgs, names, sexs):
        # 获取信息并通过字典的信息打印
        data = {'title': title.get_text().strip(), 'address': address.get_text().strip(), 'price': price.get_text(),
                'img': img.get('src'), 'name': name.get_text(), 'sex': judgement_sex(sex.get('class'))}
        print(data)


if __name__ == '__main__':  # 为程序的主入口
    # 构造多页URL
    urls = ['http://bj.xiaozhu.com/search-duanzufang-p{}-0/'.format(number) for number in range(1, 10)]
    for single_url in urls:
        get_links(single_url)  # 循环调用get_links函数
        time.sleep(3)  # 睡眠3秒
