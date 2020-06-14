import json, csv
from pprint import pprint

with open('/home/mahj/Project/Ziru_Scrapy/ziru/files/parkinfo_new.json', 'r') as f:
    data = json.load(f)

result = []
for comm in data:
    id = comm['id']
    name = comm['name']
    build_time = comm['build_time']
    build_type = comm['build_type']
    build_area = comm['build_area']
    landscaping = comm['landscaping']
    FAR = comm['FAR']
    is_noise = comm['is_noise']
    park_v = comm['park_v']
    park_month = comm['park_month']
    park_year = comm['park_year']
    is_rent = comm['is_rent']
    has_power = comm['has_power']

    if park_year != '暂无数据' or park_month != '暂无数据':
        result.append(comm)


with open('/home/mahj/Project/Ziru_Scrapy/ziru/files/result.csv', 'w', newline='') as csvfile:
    fieldnames = ['id', 'name', 'build_time', 'build_type', 'build_area', 'landscaping', 'FAR',
                  'is_noise', 'park_v', 'park_month', 'park_year', 'is_rent', 'has_power']

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for r in result:
        writer.writerow(r)


