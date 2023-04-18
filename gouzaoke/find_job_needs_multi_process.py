import requests
import xlwt
import time
import datetime

from lxml import etree
from multiprocessing import Pool  # 导入相应的库文件
from multiprocessing import Manager, Lock
import itertools
from functools import partial

"""多进程查找 过早客 -> 找工作节点，前20页求职需求"""

http_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 '
                  'Safari/537.36 ',
    'Cookie': '_xsrf=6df79b59b371499fa4a7cf229ba613aa; _ga=GA1.2.715178160.1681827717; '
              '_gid=GA1.2.492443347.1681827717; '
              '__gads=ID=291f53cfd4ff54b5-22ff53b431df0012:T=1681827717:RT=1681827717:S=ALNI_Ma0NWPJ-esJQAJk'
              '-JvSPaFpf94IIg; __gpi=UID=00000bf7c7504f8f:T=1681827717:RT=1681827717:S'
              '=ALNI_Ma36yWFrBSQvtw7EfeoOKVJMuKP-A; '
              'verification="ODgzZjY4ZWU2MWJhNDc0ZjI1MzExZDM0NTZkNjVmN2IzOTYxMThjZTI1NzRmYTgxY2I4ZDc3ZjViMGQ2MTQ1YQ'
              '==|1681827733|68b371dc1684df8395602400394fecb570aded6f"; '
              'session_id="MTA0NmFlMDVkMmE2Mzg2YjliMmFkZmM0YjZmZmZiYWE0ZTZkMzFkMjhiMDc3MDcxNDRhZGQxYzk2NmFkMzFjZg'
              '==|1681827733|e0ac6d3f2bb87e8638fdcbd363255c91762f229a"; '
              'user="NzQxODY=|1681827733|7edced265b01d6016947c7796be6ba5aba2a2275"; _gat_gtag_UA_47580304_4=1 '
}

context_path = 'https://www.guozaoke.com'
LOCK = Lock()
keywords = ['招', '招聘', '招人', '招募', '岗位', '内推']


def xpath_scraper(page_data_container, url):
    page_data = []
    print('\nurl:' + url)
    res = requests.get(url, headers=http_headers)
    html = etree.HTML(res.text)
    topic_items = html.xpath('//div[@class="topic-item"]')
    for item in topic_items:
        node = item.xpath('div[@class="main"]/div[@class="meta"]/span[@class="node"]/a/text()')[0]
        user_name = item.xpath('div[@class="main"]/div[@class="meta"]/span[@class="username"]/a/text()')[0]
        title = item.xpath('div[@class="main"]/h3[@class="title"]/a/text()')[0]
        link = context_path + item.xpath('div[@class="main"]/h3[@class="title"]/a/@href')[0]

        # 查找求职贴
        is_job = False
        for key_str in keywords:
            if title.find(key_str) != -1:
                is_job = True
                break

        if is_job:
            print('【%s】' % node, title, 'by', user_name, link)
            info_data = [node, title, user_name, link]
            page_data.append(info_data)
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


if __name__ == '__main__':

    # 当多进程的代码不在 if "__name__"=="__main__"中时，报错
    sheet_data_lst = Manager().list()

    urls = ['https://www.guozaoke.com/node/job?p={}'.format(str(i)) for i in range(1, 20)]

    # start_1 = time.time()
    # for url in urls:
    #     xpath_scraper(url)  # 单进程
    # end_1 = time.time()
    # print('串行爬虫', end_1 - start_1)

    start_3 = time.time()
    # 转换成一个参数的函数
    func_arg_1 = partial(xpath_scraper, sheet_data_lst)
    process_count = 4
    pool = Pool(processes=process_count)  # 无参数时，使用所有cpu核
    pool.map(func_arg_1, urls)
    pool.close()
    pool.join()
    end_3 = time.time()
    print('%d个进程' % process_count, end_3 - start_3)

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
    now_time_stamp = datetime.datetime.now().strftime('%Y-%m-%d-%H_%M_%S')
    workbook.save('D:/360极速浏览器下载/guozaoke_job_needs_' + now_time_stamp + '.xls')
