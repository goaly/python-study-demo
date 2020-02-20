import openhome.Hello as hello
import datetime
print('今天要来点什么不同吗？', hello.name, '!')

print('__name__:',__name__)

# 含微秒的日期时间
dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
print(dt_ms)