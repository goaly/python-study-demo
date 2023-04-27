import sys
sys.path.append("..")

#导入库文件和同一文件下的程序
from multiprocessing import Pool
from wh58.channel_extract import channel_list
from wh58.page_spider import get_links

#导入版块下的所有链接并存入MongoDB
def get_all_links_from(channel):
    #默认循环101页
    for num in range(1,101):
        get_links(channel, num)

if __name__ == '__main__':
    #创建进程池
    pool = Pool(processes=4)
    #调用进程池爬取url
    pool.map(get_all_links_from, channel_list.split())



