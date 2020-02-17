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
