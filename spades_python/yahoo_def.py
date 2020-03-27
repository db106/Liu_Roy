import os
import json
import time
import random
import requests
from bs4 import BeautifulSoup

def main(each_region, each_target):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}

    global search_tag
    search_tag = each_region + each_target

    global country
    country = '台北市'  # 手動更改

    global path
    path = 'E:\專題\Yahoo'

    global count
    count = 0

    # 建存檔資料
    path_dir = 'E:\\專題\\Yahoo\\{0}'.format(search_tag)
    make_dir(path_dir)

    path_record_article = path_dir + '\\_record_article.txt'
    global record_article_set
    record_article_set = set()
    if os.path.exists(path_record_article):
        with open(path_record_article, 'r', encoding='utf8') as f:
            for totle in f:
                record_article_set.add(totle.replace('\n', ''))



    post_data_str = """P: 4
T: 台北景點
type: search
GATitle: 關鍵字搜尋"""

    pt = post_str_to_dict(post_data_str)

    # 換頁
    for p in range(1, 100):
        url = 'https://travel.yahoo.com.tw/ajax/LoadMore.php'
        pt['P'] = str(p)
        pt['T'] = search_tag
        print(pt)
        html = post_url(url, headers, pt)
        title = soup_select(html)
        each_article_title(title)


    # 修改為你的權杖內容
    token = '9egPV4gL4zLa17A1djM3N5ZUatGi3S2nUwls52NmZJ5'
    count = str(count)
    message = '標題 : ' + search_tag + ', 爬了 : ' + count + ' 篇文章'
    lineNotifyMessage(token, message)

def each_article_title(title):
    for each_title in title:
        # print(type(each_title["href"]))
        # print(each_title.text)
        article_url = 'https://travel.yahoo.com.tw' + each_title["href"]
        print(article_url)
        try:
            res_article = requests.get(article_url)
        # print(res_article)
        except:
            continue
        article_soup = BeautifulSoup(res_article.text, 'html.parser')
        [s.extract() for s in article_soup('figcaption')]
        # print(article_soup)

        article_time = article_soup.select('p[class="date"] ')
        article_time = article_time[0].text[-11:]

        # 標題
        article_title = article_soup.select('div[class="post_header"] h1')
        # print(article_title)


        #
        # 內文
        article = article_soup.select('div[class="post_content"]')
        # print(article)
        for i in article_title:
            place_name = i.text
            list = ['*', '|', '\\', ':', '\"', '<', '>', ']', '[', '? ', '/', '《', '》', '・', '/', '，', '「', '」', '！',
                    '｜', '【', '】', '？', '、', '.', '’', '–', '～', '?']
            for c in list:
                place_name = place_name.replace(c, '')
            # print(place_name)
            # 共存


        #
        #
        for u in article:
            content = u.text
            p = content.strip()
            # print(p)
            if each_target == '景點':
                save_data_dict = {'文章網址': article_url,
                                  '發文時間': article_time,
                                  '標題': place_name,
                                  '景點名稱': 'NA',
                                  '文章內容': p,
                                  '留言': 'NA',
                                  '地址': 'NA',
                                  '縣市': country}
            elif each_target == '美食':
                save_data_dict = {'文章網址': article_url,
                                  '發文時間': article_time,
                                  '標題': place_name,
                                  '餐廳名稱': 'NA',
                                  '美食名稱': 'NA',
                                  '文章內容': p,
                                  '留言': 'NA',
                                  '地址': 'NA',
                                  '縣市': country}

            save_data_js = json.dumps(save_data_dict, ensure_ascii=False)
            # print(type(json))
            save_file(path, place_name, save_data_js)
            total = article_time + place_name
            global record_article_set
            if total not in record_article_set:
                global count
                count += 1
                record_article_set.add(total)
                save_file(path, '_record_article', total)
                print(total)

def save_file(path_dir_each, place_name, save_data_js):
    global search_tag
    path = path_dir_each + '\\' + search_tag
    make_dir(path)

    with open(path + '\\' + place_name + '.json', 'a', encoding='utf8') as f:
        f.write(save_data_js)
        f.write('\n-----\n')

def make_dir(path_dir):
    # 將路徑切割 一層一層 建資料夾
    list = path_dir.split('\\')
    path_str = list[0]
    for each in list[1:]:
        path_str += "\\" + each
        if not os.path.exists(path_str):
            os.mkdir(path_str)

def soup_select(html):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.select('div[class="item_block"] a')[6:]
    return title

def post_url(url, headers, post_data):

    try:
        response = requests.post(url, headers=headers, data=post_data)

        response.encoding = 'utf-8'

        HTTP_Status_Code = [200, 401, 404]
        if response.status_code in HTTP_Status_Code:
            # print(response.text)
            return response.text
        else:
            print('請求網頁源代碼錯誤, 錯誤狀態碼：', response.status_code)
            print(url)
            raise
    except Exception as e:
        print('Exception =', e)
        time_sleep = 5 + float(random.randint(1, 400)) / 100
        print('Crawler 休息', time_sleep, '秒', '---url:', url)
        time.sleep(time_sleep)
        return post_url(url, headers, post_data)

def post_str_to_dict(post_data_str):
    post_data = {}

    for i in post_data_str.split('\n'):
        post_data[i.split(': ')[0]] = i.split(': ')[1]


    # print(post_data)
    return post_data

def get_html(url, headers, post_data):  # 訪問網頁
    try:

        response = requests.post(url, headers=headers, data=post_data)

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

def lineNotifyMessage(token, msg):

    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    return r.status_code

    # 修改為你要傳送的訊息內容

if __name__ == "__main__":
    tag_list_region = ['台北', '新北', '基隆', '桃園', '新竹', '宜蘭']  # 手動更改
    # tag_list_region = ['桃園', '新竹','宜蘭']  # 手動更改
    tag_list_target = ['景點', '美食']  # 手動更改

    for each_target in tag_list_target:
        for each_region in tag_list_region:
            print('開始爬:', each_region + each_target)
            main(each_region, each_target)

