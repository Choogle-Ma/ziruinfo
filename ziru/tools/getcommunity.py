import json
from pprint import pprint

with open(r'/home/mahj/PycharmProjects/ziruinfo/ziru/files/community.json', 'r') as f:
    data = json.load(f)

communities = {}
for i in data:
    if i['data'] != []:
        for community in i['data']:
            communities[community['code']] = community['name']

pprint(communities)
print(len(communities))
