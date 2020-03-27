import os
import time
import json
import random
import requests
from bs4 import BeautifulSoup


def main():
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
    url = 'http://rtr.pbs.gov.tw/pbsmgt/RoadAllServlet?ajaxAction=roadAllCache'

    global path
    path = 'E:\\專題\\road'

    res = get_html(url, headers)
    # print(type(res.text))
    js_load(res)


def js_load(res):
    js_data = json.loads(res.text)
    # print(js_data)
    for i in range(1, 30):
        name = js_data['formData'][i]['name']
        # print(name)
        direction = js_data['formData'][i]['direction']
        # print(direction)
        fromkm = js_data['formData'][i]['fromkm']
        # print(fromkm)
        roadtype = js_data['formData'][i]['roadtype']
        # print(roadtype)
        lastmodified = js_data['formData'][i]['lastmodified']
        # print(lastmodified)
        comment = js_data['formData'][i]['comment']
        # print(comment)
        if direction != '':
            save_data_dict = {'地點': name,
                              '方向': direction,
                              '公里數': fromkm,
                              '類別': roadtype,
                              '時間': lastmodified,
                              '路況說明': comment}
            print(save_data_dict)
            save_data_js = json.dumps(save_data_dict, ensure_ascii=False)
            save_file(save_data_js)


def save_file(save_data_js):

    global path
    path = 'E:\\專題\\road'
    if not os.path.exists(path):
        os.mkdir(path)
    with open(path + '\\' + 'road' + '.json', 'a', encoding='utf8') as f:
        f.write(save_data_js)
        f.write('\n-----\n')


def get_html(url, headers):  # 訪問網頁
    try:
        response = requests.post(url, headers=headers)

        if response.status_code == 200:
            # print(response.text)
            return response
        else:
            print('請求網頁源代碼錯誤, 錯誤狀態碼：', response.status_code)
            print(url)
            time.sleep(5)
            return get_html(url, headers)
    except Exception as e:
        print(e)
        print(url)
        time.sleep(60 + float(random.randint(1, 4000)) / 100)
        return get_html(url, headers)


def soup_select(html):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.select('tr[class="tbody"]')
    print(title)
    return title


if __name__ == '__main__':
    main()
    print('Complete!!!!!!!!!!')

