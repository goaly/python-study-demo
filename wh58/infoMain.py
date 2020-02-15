import sys

sys.path.append("..")
from multiprocessing import Pool
from wh58.page_spider import get_info
from wh58.page_spider import wh58_url
from wh58.page_spider import wh58_info

db_urls = [item['url'] for item in wh58_url.find()]
db_infos = [item['url'] for item in wh58_info.find()]

x = set(db_urls)
y = set(db_infos)

rest_urls = x - y

if __name__ == '__main__':
    # 创建进程池
    pool = Pool(processes=4)
    pool.map(get_info, rest_urls)
