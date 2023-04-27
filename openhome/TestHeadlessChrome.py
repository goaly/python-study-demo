import datetime
from selenium import webdriver
# 导入 WebDriverWait 包
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import DesiredCapabilities

from selenium.webdriver.chrome.options import Options

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
# 不弹出浏览器 - 加了headless不可用，豆瓣网做了反爬
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument('window-size=1920,1080')
chrome_options.add_argument('--ignore-certificate-errors')
capabilities = DesiredCapabilities.CHROME
capabilities["ACCEPT_SSL_CERTS"] = True
capabilities["acceptSslCerts"] = True
capabilities["acceptInsecureCerts"] = True
capabilities["ignore-certificate-errors"] = True
driver = webdriver.Chrome(options=chrome_options, desired_capabilities=capabilities)

# driver = webdriver.Chrome()

driver.get("https://search.douban.com/book/subject_search?search_text=python&cat=1001&start=0")

# 隐式等待
driver.implicitly_wait(3)
# 显示等待，WebDriverWait()方法使用
# WebDriverWait(driver, 3).until(
#     lambda driver: driver.find_elements_by_xpath('//div[@class="item-root"]/div[@class="detail"]'))


# 逐渐滚动浏览器窗口，令ajax逐渐加载
# for i in range(0, 10):
#     driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
#     i += 1
#     time.sleep(4)

try:
    # 得到执行完js的代码
    with open('pageSource.html', 'w', encoding='utf8') as fp:
        fp.write(driver.page_source)

        # 最大化显示宽度
        if driver.find_element(By.TAG_NAME, 'body'):
            width = driver.execute_script(
                "return Math.max(document.body.scrollWidth, document.body.offsetWidth, "
                "document.documentElement.clientWidth, document.documentElement.scrollWidth, "
                "document.documentElement.offsetWidth);")
            height = driver.execute_script(
                "return Math.max(document.body.scrollHeight, document.body.offsetHeight, "
                "document.documentElement.clientHeight, document.documentElement.scrollHeight, "
                "document.documentElement.offsetHeight);")
            driver.set_window_size(width + 100, height + 100)
        # 截屏
        driver.save_screenshot(
            'D:/360极速浏览器下载/screenshot_' + datetime.datetime.now().strftime('%Y-%m-%d-%H_%M_%S.%f') + '.png')

    print(driver.page_source, '\n')

    infos = driver.find_elements(By.XPATH, '//div[@class="item-root"]/div[@class="detail"]')
    for info in infos:
        title = info.find_element(By.XPATH, 'div[@class="title"]/a')
        name = title.text
        if name:
            print(name)

except NoSuchElementException as ex:
    print('未找到对应元素：', ex.msg)
driver.quit()
