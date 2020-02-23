# API调用测试
import requests
import json
import pprint

ip_location_url = 'http://ip-api.com/json/?lang=zh-CN'
place_search_url = 'http://api.map.baidu.com/place/v2/search'
baidu_ak = 'DVh60itxylKMgh3gk8fBB9veHaXCRph7'

region = ''
search_key = input('请输入要搜索的地点：')
if search_key.strip() != '':
    # region = input('请输入搜索地点所属的区域：')
    if region.strip() == '':
        res_ip = requests.get(ip_location_url)
        json_ip = json.loads(res_ip.text)
        region = json_ip['city'] or json_ip['regionName']
    if region.strip() == '':
        region = '全国'
    param = {'query': search_key, 'region': region, 'output': 'json', 'ak': baidu_ak}
    res_pl = requests.get(place_search_url, param)
    json_pl = json.loads(res_pl.text)
    pprint.pprint(json_pl)
