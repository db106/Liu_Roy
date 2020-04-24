import os
import json
from json import loads
from urllib import request, parse

dataid = 'F-C0032-001'

apikey = 'CWB-2B1A8353-B912-422F-82EF-9FFEA7941993'

format = 'json'

url = 'https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/{0}?Authorization={1}&format={2}'.format(dataid, apikey, format)

# print(url)

path_dir = 'E:\專題\weather'
if not os.path.exists(path_dir):
    os.mkdir(path_dir)

result = request.urlopen(url)
# print(result)
resp = loads(result.read())
# print(resp)

for i in range(0,22):
    locationsName = resp['cwbopendata']['dataset']["location"][i]["locationName"]
    # print(locationsName)
    high = resp['cwbopendata']['dataset']["location"][i]["weatherElement"][1]['time'][1]['parameter']['parameterName']

    low = resp['cwbopendata']['dataset']["location"][i]["weatherElement"][2]['time'][1]['parameter']['parameterName']

    ci = resp['cwbopendata']['dataset']["location"][i]["weatherElement"][3]['time'][1]['parameter']['parameterName']

    pop = resp['cwbopendata']['dataset']["location"][i]["weatherElement"][4]['time'][1]['parameter']['parameterName']


    # print('地區 : ' + locationsName,  ',', '最高溫 : ' + high, ',', '最低溫 : ' + low, ',', '舒適度 : ' + ci, ',', '降雨機率 : ' + pop, '%')

    save_data_dict = {'地區': locationsName,
                      '最高溫': high,
                      '最低溫': low,
                      '舒適度': ci,
                      '降雨機率': pop,
                      }

    print(save_data_dict)

    save_data_js = json.dumps(save_data_dict, ensure_ascii=False)
    with open(path_dir + '\\' + 'weather.json', 'a', encoding='utf8') as f:
        f.write(save_data_js+'\n')


