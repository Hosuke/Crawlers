#!/usr/bin/python
# encoding=utf-8

from urllib.parse import quote

import requests
import time
from openpyxl import Workbook

'''
Created by Geyang(Hosuke)
'''


def generate_headers(key, city):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/62.0.3202.94 Safari/537.36',
        'Referer': 'https://www.lagou.com/jobs/list_' + quote(key) + '?px=default&city=' + quote(city),
        'Origin': 'https://www.lagou.com',
        'Host': 'www.lagou.com',
        'Cookie': 'user_trace_token=20180328091624-4c36c613-3287-4085-b9e7-03dfa4630c6c; '
                  'JSESSIONID=ABAAABAACBHABBI5CAC404D72E90AD627BD18BDF9E6526B; _ga=GA1.2.569094806.1522200035; '
                  '_gid=GA1.2.1952125761.1522200035; index_location_city=%E5%85%A8%E5%9B%BD; '
                  'LGUID=20180328092037-3869b39e-3226-11e8-a232-525400f775ce; '
                  'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1522200039; _gat=1; '
                  'LGSID=20180328112750-fe6095db-3237-11e8-a24f-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=; '
                  'PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; LGRID=20180328112750-fe609747-3237-11e8-a24f-525400f775ce; '
                  'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1522207671; TG-TRACK-CODE=index_search; '
                  'SEARCH_ID=bc2ef9644474448e8fece3bcbde1591a '
    }
    return headers


def generate_url(city):
    return 'https://www.lagou.com/jobs/positionAjax.json?px=default&city=' + quote(city) + '&needAddtionalResult=false&isSchoolJob=0'


def get_one_page(key, city):
    data = {
        'first': 'true',
        'pn': '1',
        'kd': key
    }

    url = generate_url(city)
    headers = generate_headers(key, city)
    res = requests.post(
        url,
        data=data, headers=headers)
    result = res.json()
    return result


def get_job_list(pageSize, key, city):
    info_list = []
    for pn in [x + 1 for x in range(pageSize)]:
        if pn == 1:
            is_first = 'true'
        else:
            is_first = 'false'

        data = {
            'first': is_first,
            'pn': str(pn),
            'kd': key
        }

        url = generate_url(city)
        headers = generate_headers(key, city)

        res = requests.post(
            url,
            data=data, headers=headers)
        time.sleep(2)
        result = res.json()
        jobs = result.get('content').get('positionResult').get('result')

        print("正在解析第" + str(pn) + "页...")
        print(jobs)
        if len(jobs) == 0:
            break

        for i in jobs:
            info = [i['positionName']]
            info.append(i['companyShortName'])
            info.append(i['companyFullName'])
            info.append(i['salary'])
            info.append(i['workYear'])
            info.append(i['education'])
            info.append(i['city'])
            info_list.append(info)

    return info_list


def generate_xlsx(key, rows):
    wb = Workbook()
    ws1 = wb.active
    ws1.title = key
    for row in rows:
        ws1.append(row)
    wb.save('职位信息.xlsx')


def main():
    key = input("请输入想要查询的工作岗位：")
    city = input("请输入想要工作的城市：")
    result = get_one_page(key, city)
    pageSize = result['content']['pageSize']
    time.sleep(2)
    info_list = get_job_list(pageSize, key, city)
    generate_xlsx(key, info_list)


if __name__ == '__main__':
    main()
