'''自动打卡测试'''
import re
import datetime
import json
import time
from selenium import webdriver
# 引入ActionChains类
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.select import Select

caps = webdriver.DesiredCapabilities().FIREFOX
# （从Firefox 48开始）的每个版本，其中属性marionette需要设置为true（默认或通过配置）
# 如果您使用的是旧版Firefox版本（直到Firefox 47.x），GeckoDriver仍然可以使用，但是必须将属性marionette显式设置为false
# caps["marionette"] = False
binary = FirefoxBinary('C:/Program Files/Mozilla Firefox/firefox.exe',
                       log_file=open('D:/360极速浏览器下载/TestAutoClock.log', 'wb'))
driver = webdriver.Firefox(firefox_binary=binary, capabilities=caps, timeout=60)

try:
    url = 'https://auth.zkh360.com/server/signin.html?client_id=002033&redirect_uri=http%3A%2F%2Fauth.zkh360.com%2Fserver' \
          '%2Foauth%2Fauthorize%3Fresponse_type%3Dcode%26client_id%3D002033%26redirect_uri%3Dhttp%253A%252F%252Foa.zkh360' \
          '.com%252Fwui%252Fcas-entrance.jsp%253Fpath%253Dhttps%25253A%25252F%25252Foa.zkh360.com%25252Fwui%25252Findex' \
          '.html%252523%25252Fmain%2526ssoType%253DOAUTH2%2526ssoType%253DOAUTH2 '
    driver.get(url)

    # 隐式等待
    driver.implicitly_wait(3)

    input_username = driver.find_element_by_css_selector('input#username.login_input')
    input_password = driver.find_element_by_css_selector('input#password.login_input')

    uname = ''
    pwd = ''
    with open('autoClockInCfg.json') as cfg:
        json_cfg = json.load(cfg)
        uname = json_cfg['username']
        pwd = json_cfg['password']

    if uname.strip() == '' or pwd.strip() == '':
        raise ValueError('用户或密码为空！')

    input_username.send_keys(uname)
    input_password.send_keys(pwd)
    driver.find_element_by_css_selector('button#loginButton').click()
    print('==============安全中心登录成功')
    driver.implicitly_wait(8)
    time.sleep(8)
    # 得到执行完js的代码True
    # with open('autoClockIn_PageSource.html', 'w', encoding='utf8') as fp:
    #     fp.write(driver.page_source)
    top_menu = driver.find_element_by_css_selector('.e9header-top-menu > div:nth-of-type(1)')
    ActionChains(driver).move_to_element(top_menu).perform()
    print('==============显示顶部功能瓷片')
    driver.implicitly_wait(1)
    time.sleep(1)
    menu_flow = driver.find_element_by_css_selector('div.e9header-top-menu-item:nth-of-type(2)')
    ActionChains(driver).click(menu_flow).perform()
    print('==============切换到流程模块')
    time.sleep(3)
    left_menu_flow_li = driver.find_element_by_xpath("//span[@id='num_12']/../..")
    left_menu_flow_li.click()
    print('==============点击“新建流程”')
    time.sleep(2)
    link_clock_in = driver.find_element_by_xpath("//a[@title='ZKH每日健康打卡']")
    link_clock_in.click()
    print('==============点击“ZKH每日健康打卡”')
    time.sleep(2)
    handles = driver.window_handles  # 获取当前窗口句柄集合（列表类型）
    driver.switch_to.window(handles[1])  # 切换到新的网页窗口
    print('==============切换到新的网页窗口')
    time.sleep(3)

    print('==============开始填写表单')
    # 目前所在地
    print('填写目前所在地...')
    input_cur_loc = driver.find_element_by_xpath("//input[@id='field11028']")
    input_cur_loc.send_keys('湖北省武汉市')

    # 是否已回工作地
    print('填写是否已回工作地...')
    driver.find_element_by_xpath("//div[@id='weaSelect_1']").click()
    time.sleep(4)
    driver.find_element_by_xpath("//li[@title='是'][@role='menuitem']").click()
    time.sleep(1)

    # 可到办公室上班时间
    print('填写可到办公室上班时间...')
    driver.find_element_by_xpath("//div[@id='weaSelect_2']").click()
    time.sleep(1)
    driver.find_element_by_xpath("//li[@title='复工时间待定'][@role='menuitem']").click()
    time.sleep(1)

    # 目前上班形式
    print('填写目前上班形式...')
    driver.find_element_by_xpath("//div[@id='weaSelect_3']").click()
    time.sleep(1)
    driver.find_element_by_xpath("//li[@title='居家办公'][@role='menuitem']").click()
    time.sleep(1)

    # 已上班的办公室名称
    print('填写已上班的办公室名称...')
    input_worked_office_nm = driver.find_element_by_xpath("//input[@id='field11190']")
    input_worked_office_nm.send_keys('无')

    # 不能去办公室现场办公的原因
    print('填写不能去办公室现场办公的原因...')
    driver.find_element_by_xpath("//div[@id='weaSelect_4']").click()
    time.sleep(1)
    driver.find_element_by_xpath("//li[@title='已返回-工作地办公室不允许上班'][@role='menuitem']").click()
    time.sleep(1)

    # 目前健康状况--无症状
    print('填写目前健康状况...')
    driver.find_element_by_css_selector(".field11037_swapDiv").click()
    time.sleep(1)
    print('==============表单填写完毕')

    btn_submit = driver.find_element_by_xpath("//button[@title='提交']")
    btn_submit.click()
    # time.sleep(1)
    print('==============表单已提交')

except Exception as ex:
    print(ex)
    pass

# driver.quit()  # 退出浏览器
