import re

# 测试正则表达式
a = 'xxIxxfsdaxxlovexxijrexxPythonxx'

infos = re.findall('xx(.*?)xx', a)
print(infos)

b = 'one1two2three3'
re1 = re.search('\d+', b)
print(re1)
print(re1.group())
re2 = re.findall('\d+', b)
print(re2)

# sub()用于替换字符串的匹配项
phone = '132-0711-3160'
newPhone = re.sub('\D+', '', phone)
print(newPhone)

# sub()用于替换字符串的匹配项
price1 = '119.00元'
if price1.find('元'):
    print(price1)
new_price1 = re.sub('[^\d\.]+', '', price1)
print(new_price1)

price2 = 'CNY 69.00'
if re.search('CNY', price2, re.I):
    print(price2)
new_price2 = re.sub('[^\d\.]+', '', price2)
print(new_price2)

result = re.search('All contents are copyrighted',
                 '2018-2019&nbsp;&copy;&nbsp;所有内容版权归原作者所有 / All contents are copyrighted by their respective authors. <br/> Powered by <a target="_blank" href="/">斗破小说网</a>', re.I)
print(result is None)
