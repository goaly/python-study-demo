import datetime
import time
from functools import partial
from multiprocessing import Manager, Lock
from multiprocessing import Pool  # 导入相应的库文件

import re
import requests
import xlwt
from lxml import etree

"""多进程查找 过早客 """

http_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 '
                  'Safari/537.36 ',
    'Cookie': '_ga=GA1.1.1740914313.1685604234; _xsrf=0915f9eefb7c4a40a42f5106dcaa65a9; '
              'verification="MWNjZDdhNDc4YzRlYzIyMDBmYmM4OTE5OTMzMWRlNWFkM2M4ZThhZTZkMDg2M2U0M2MzMjI5NmI4NmMxYzYzZg'
              '==|1685604249|a8032618a4477a06231810b6c89871da51b67550"; '
              'session_id="ZjJhODMzMWMzZjE0OGRjNDNhNWJlMjNlNDBkZDM0ZTNiNGQ2NmYyMGQyODMwMWZmZjNkZWVjYjA5MjRhMmRjZg'
              '==|1685604249|7382d2b2b50982e7cfdd623dbcc05eb559d4d46b"; '
              'user="NzQxODY=|1685604249|d84b8c488860c98c51dd9018aad45d5473921741"; _dx_captcha_cid=99275097; '
              '_dx_uzZo5y=563409320f9849198f390ffa3e27ae2c4cf1273ef3f37d26bf3fb6bb308a28336c7ef3e2; '
              '_dx_FMrPY6=6478479abFmZilPXdE9a5QeXVTEgLt7Uhol3xpd1; '
              '__gads=ID=2fbcc3e35579384d-2276f1faaee10018:T=1685604234:RT=1685686781:S'
              '=ALNI_MboGfjxkDyzgno5LcQFmbPPWmArUw; '
              '__gpi=UID=00000c0db7ca89a4:T=1685604234:RT=1685686781:S=ALNI_MaarLECeOZiXEQkDdYHIUy-337ELg; '
              '_ga_YTS4ZXTQK4=GS1.1.1685685724.3.1.1685686820.21.0.0 '
}

context_path = 'https://www.guozaoke.com'

def xpath_scraper(page_data_container, url):
    page_data = []
    print('\nurl:' + url)
    res = requests.get(url, headers=http_headers)
    html = etree.HTML(res.text)
    topic_items = html.xpath('//div[@class="topic-item"]')
    for item in topic_items:
        item_node = item.xpath('div[@class="main"]/div[@class="meta"]/span[@class="node"]/a')[0]
        node_text = item_node.xpath('text()')[0]
        node = re.sub('/node/', '', item_node.xpath('@href')[0])
        user_name = item.xpath('div[@class="main"]/div[@class="meta"]/span[@class="username"]/a/text()')[0]
        title = item.xpath('div[@class="main"]/h3[@class="title"]/a/text()')[0]
        link = context_path + item.xpath('div[@class="main"]/h3[@class="title"]/a/@href')[0]

        # 查找求职贴
        is_matched = False
        for key_str in keywords:
            # 忽略大小写匹配
            is_matched = bool(re.search(key_str, title, re.IGNORECASE))
            if is_matched:
                break

        if is_matched:
            node_info = node_text + ' - ' + node
            print('【%s】' % node_info, title, 'by', user_name, link)
            info_data = [node_info, title, user_name, link]
            page_data.append(info_data)
    if len(page_data) > 0:
        with LOCK:
            page_data_container.append(page_data)


def init_workbook(headers):
    """初始化Excel工作表"""
    workbook = xlwt.Workbook(encoding='utf-8')
    sheet = workbook.add_sheet('sheet1')
    # 设置第一行高度 24pt
    tall_style = xlwt.easyxf('font:height 480')
    first_row = sheet.row(0)
    first_row.set_style(tall_style)
    # 创建一个样式对象，初始化样式
    style = xlwt.XFStyle()
    al = xlwt.Alignment()
    al.horz = 0x02  # 设置水平居中
    al.vert = 0x01  # 设置垂直居中
    style.alignment = al
    # 写入表头
    for h, header in enumerate(headers):
        sheet.write(0, h, header, style)

    return workbook


# 获取字符串显示在excel单元格中的等效0字符宽度，xlwt中列宽的值表示方法：默认字体0的1/256为衡量单位。
def get_col_width(txt):
    # 默认11个字符
    col_w = 11
    if txt:
        col_w = len(txt)
        zh_char_num = 0
        for ch in txt:
            if '\u4e00' <= ch <= '\u9fff':
                zh_char_num += 1
        col_w = (col_w - zh_char_num) + zh_char_num * 2
    return 256 * col_w

def save_to_workbook(save_path, sheet_data_lst):
    """将抓到的数据保存到指定路径的Excel文件中"""
    data_count = 0
    if len(sheet_data_lst) == 0:
        return data_count

    headers = ['节点', '标题', '发布人', '链接']
    col_default_w = 256 * 11
    col_widths = []
    for i in range(0, len(headers)):
        col_widths += [col_default_w]
    workbook = init_workbook(headers)
    sheet = workbook.get_sheet(0)
    # 设置链接字体颜色
    style_link_color = xlwt.easyxf('font:colour_index blue')
    row_idx = 1
    for page_data in sheet_data_lst:
        for row_data in page_data:
            data_count += 1
            for j, cellData in enumerate(row_data):
                new_col_w = get_col_width(cellData)
                if new_col_w > col_widths[j]:
                    # 更新列宽
                    col_widths[j] = new_col_w
                if cellData.startswith("http://") or cellData.startswith("https://"):
                    # 超链接
                    sheet.write(row_idx, j, xlwt.Formula('HYPERLINK("' + cellData + '";"' + cellData + '")'),
                                style_link_color)
                else:
                    sheet.write(row_idx, j, cellData)
            row_idx += 1
    # 设置列宽
    for i, col_w in enumerate(col_widths):
        sheet.col(i).width = col_w
    workbook.save(save_path)
    print('数据成功保存到: %s' % save_path)
    return data_count

LOCK = Lock()
# 版块
# node_type = ''
# node_type = 'job'
node_type = 'IT'
# 搜索关键字
keywords = ['魔法', '代理']
# 页数上限
pg_limit = 50

if __name__ == '__main__':

    # 当多进程的代码不在 if "__name__"=="__main__"中时，报错
    sheet_data_lst = Manager().list()
    node_path = '/node/' + node_type if len(node_type) > 0 else ''
    urls = ['https://www.guozaoke.com{}?p={}'.format(node_path, str(i)) for i in range(1, pg_limit)]

    start_1 = time.time()
    process_count = 4
    if process_count > 1:
        # 多进程
        # 柯里化 xpath_scraper - 转换成一个参数的函数
        func_arg_1 = partial(xpath_scraper, sheet_data_lst)
        pool = Pool(processes=process_count)  # 无参数时，使用所有cpu核
        pool.map(func_arg_1, urls)
        pool.close()
        pool.join()
    else:
        # 单进程
        for url in urls:
            xpath_scraper(sheet_data_lst, url)
    end_1 = time.time()

    now_time_stamp = datetime.datetime.now().strftime('%Y-%m-%d-%H_%M_%S')
    save_path = 'D:/360极速浏览器下载/guozaoke_search_result_' + now_time_stamp + '.xls'
    data_count = save_to_workbook(save_path, sheet_data_lst)
    print('\n%d 进程搜索 %d 个页面，共抓取到 %d 条数据，耗时 %.3f 秒' % (process_count, pg_limit, data_count, end_1 - start_1))
