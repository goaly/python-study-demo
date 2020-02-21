import xlwt
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


def get_curpage_data():
    page_data = []
    infos = driver.find_elements_by_xpath('//div[@class="item-root"]/div[@class="detail"]')
    for info in infos:
        str_book_info = info.find_element_by_xpath('div[@class="meta abstract"]').text
        book_infos = str_book_info.split('/')
        if len(book_infos) < 5:
            continue;

        title = info.find_element_by_xpath('div[@class="title"]/a')
        url = title.get_attribute('href')
        name = title.text

        author = book_infos[0]
        price = book_infos[-1]
        pub_date = book_infos[-2]
        publisher = book_infos[-3]
        rate = info.find_element_by_xpath('div[2]/span[2]').text
        comment_num = info.find_element_by_xpath('div[2]/span[3]').text

        print(name, url, author, publisher, pub_date, price, rate, comment_num)
        info_data = [name, url, author, publisher, pub_date, price, rate, comment_num]
        page_data.append(info_data)
    return page_data


try:
    # 爬取页数
    pageCount = 2
    headers = ['书名', '链接', '作者', '出版社', '出版日期', '价格', '得分', '评价人数']
    workbook = xlwt.Workbook(encoding='utf-8')
    sheet = workbook.add_sheet('sheet1')
    rowIdx = 1

    # 写入表头
    for h, header in enumerate(headers):
        sheet.write(0, h, header)

    sheetdata = []

    # 得到执行完js的代码
    with open('pageSource.html', 'w', encoding='utf8') as fp:
        fp.write(driver.page_source)

    maximize_window()
    # 截屏
    # driver.save_screenshot(
    #     'D:/360极速浏览器下载/screenshot_' + datetime.datetime.now().strftime('%Y-%m-%d-%H_%M_%S.%f') + '.png')

    # 打印网页源代码
    # print(driver.page_source, '\n')

    for n in range(pageCount + 1):
        sheetdata = get_curpage_data()
        if len(sheetdata) > 0:
            for rowData in sheetdata:
                for j, cellData in enumerate(rowData):
                    sheet.write(rowIdx, j, cellData)
                rowIdx += 1
            next_link = driver.find_element_by_css_selector('div.paginator > a.next')
            print('准备跳转第', n + 2, '页：', next_link.get_attribute('href'))
            next_link.click()
            driver.implicitly_wait(3)
            time.sleep(4)

    workbook.save('D:/360极速浏览器下载/pythonBookTop150.xls')

except NoSuchElementException as ex:
    print('未找到对应元素：', ex.msg)

# 退出浏览器
driver.quit()
