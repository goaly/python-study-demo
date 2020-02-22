import xlwt
import re
import datetime
import time
from selenium import webdriver
# 导入 WebDriverWait 包
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

caps = webdriver.DesiredCapabilities().FIREFOX
# （从Firefox 48开始）的每个版本，其中属性marionette需要设置为true（默认或通过配置）
# 如果您使用的是旧版Firefox版本（直到Firefox 47.x），GeckoDriver仍然可以使用，但是必须将属性marionette显式设置为false
# caps["marionette"] = False
binary = FirefoxBinary('C:/Program Files/Mozilla Firefox/firefox.exe',
                       log_file=open('D:/360极速浏览器下载/FirefoxBinary.log', 'wb'))
driver = webdriver.Firefox(firefox_binary=binary, capabilities=caps, timeout=60)

# driver = webdriver.PhantomJS()

# driver.get("https://www.baidu.com")
driver.get("https://search.douban.com/book/subject_search?search_text=python&cat=1001&start=0")

# 隐式等待
driver.implicitly_wait(10)

now_time_stamp = datetime.datetime.now().strftime('%Y-%m-%d-%H_%M_%S.%f')


# 显示等待，WebDriverWait()方法使用
# WebDriverWait(driver, 3).until(
#     lambda driver: driver.find_elements_by_xpath('//div[@class="item-root"]/div[@class="detail"]'))


# 逐渐滚动浏览器窗口，令ajax逐渐加载
# for i in range(0, 10):
#     driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
#     i += 1
#     time.sleep(4)

# 最大化窗口
def maximize_window():
    # 最大化显示宽度
    if driver.find_element_by_tag_name('body'):
        width = driver.execute_script(
            "return Math.max(document.body.scrollWidth, document.body.offsetWidth, "
            "document.documentElement.clientWidth, document.documentElement.scrollWidth, "
            "document.documentElement.offsetWidth);")
        height = driver.execute_script(
            "return Math.max(document.body.scrollHeight, document.body.offsetHeight, "
            "document.documentElement.clientHeight, document.documentElement.scrollHeight, "
            "document.documentElement.offsetHeight);")
        driver.set_window_size(width + 100, height + 100)


# 获取当前页的图书数据
def get_curpage_data():
    page_data = []
    infos = driver.find_elements_by_xpath('//div[@class="item-root"]/div[@class="detail"]')
    for info in infos:
        str_book_info = info.find_element_by_xpath('div[@class="meta abstract"]').text
        book_infos = str_book_info.split('/')
        if len(book_infos) < 5:
            continue

        title = info.find_element_by_xpath('div[@class="title"]/a')
        url = title.get_attribute('href')
        name = title.text

        author = book_infos[0]
        price = book_infos[-1]
        if re.search('CNY', price, re.I) or price.find('元'):
            # 人民币价格，去除非数值信息
            price = re.sub('[^\d\.]+', '', price)
        pub_date = book_infos[-2]
        publisher = book_infos[-3]
        rate = info.find_element_by_xpath('div[2]/span[2]').text
        comment_num = info.find_element_by_xpath('div[2]/span[3]').text

        print(name, url, author, publisher, pub_date, price, rate, comment_num)
        info_data = [name, url, author, publisher, pub_date, price, rate, comment_num]
        page_data.append(info_data)
    return page_data


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


try:
    # 爬取页数
    pageCount = 7
    headers = ['书名', '链接', '作者', '出版社', '出版日期', '价格', '得分', '评价人数']
    col_default_w = 256 * 11
    col_widths = [col_default_w, col_default_w, col_default_w, col_default_w, col_default_w, col_default_w,
                  col_default_w, col_default_w]
    workbook = xlwt.Workbook(encoding='utf-8')
    sheet = workbook.add_sheet('sheet1')
    rowIdx = 1

    # 设置第一行高度
    tall_style = xlwt.easyxf('font:height 480')  # 24pt
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

    sheetdata = []

    # 得到执行完js的代码True
    with open('pageSource.html', 'w', encoding='utf8') as fp:
        fp.write(driver.page_source)

    maximize_window()
    # 截屏
    # driver.save_screenshot(
    #     'D:/360极速浏览器下载/screenshot_' + now_time_stamp + '.png')

    # 打印网页源代码
    # print(driver.page_source, '\n')

    # 设置链接字体颜色
    style_link_color = xlwt.easyxf('font:colour_index blue')

    n = 1
    while True:
        sheetdata = get_curpage_data()
        if len(sheetdata) > 0:
            for rowData in sheetdata:
                for j, cellData in enumerate(rowData):
                    new_col_w = get_col_width(cellData)
                    if new_col_w > col_widths[j]:
                        # 更新列宽
                        col_widths[j] = new_col_w
                    if cellData.startswith("http://") or cellData.startswith("https://"):
                        # 超链接
                        sheet.write(rowIdx, j, xlwt.Formula('HYPERLINK("' + cellData + '";"' + cellData + '")'), style_link_color)
                    else:
                        sheet.write(rowIdx, j, cellData)
                rowIdx += 1
        n += 1
        if n <= pageCount:
            next_link = driver.find_element_by_css_selector('div.paginator > a.next')
            print('\n==============================准备跳转第', n, '页：', next_link.get_attribute('href'))
            next_link.click()
            driver.implicitly_wait(3)
            time.sleep(5)
        else:
            print('\n==============================爬取完毕==============================')
            break

    # 设置列宽
    for i, col_w in enumerate(col_widths):
        sheet.col(i).width = col_w
    workbook.save('D:/360极速浏览器下载/pythonBookTop100_' + now_time_stamp + '.xls')

except NoSuchElementException as ex:
    print('未找到对应元素：', ex.msg)

# 退出浏览器
driver.quit()
