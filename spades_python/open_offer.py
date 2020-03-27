import os
import json
import random
import requests
from time import sleep
from bs4 import BeautifulSoup


def get_html(url, headers):    # 訪問網頁
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # print(response.text)
            return response
        else:
            print('請求網頁源代碼錯誤, 錯誤狀態碼：', response.status_code)
            print(url)
            sleep(5)
            return get_html(url,headers)
    except Exception as e:
        print(e)
        print(url)
        sleep(60 + float(random.randint(1, 4000)) / 100)
        return get_html(url,headers)
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}

# 開檔
path_dir = 'E:\專題\openrice'
if not os.path.exists(path_dir):
    os.mkdir(path_dir)

country = '台北市'   # 手動更改影響json 新竹 宜蘭
search_tag = 'taipei'   # 手動更改英文 hsinchu yilan
search_tag1 = 'attraction'   # 手動更改英文 attraction 或是 restaurant
page = 1
count = 0
new_content = []

for k in range(1, 28):
    url = 'https://travel.openrice.com/taiwan/%s/%s/sr1.htm?ST=1&page=%s' % (search_tag, search_tag1, k)
    # print(url)
    res = get_html(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    # print(soup)
    title = soup.select('div[class="roundcontentbox"] span[class="Restgreenlink f016b"] a')
    # print(title)
    for i in title:
        # print(i.text)
        string = i.text
        list = ['*', '|', '\\', ':', '\"', '<', '>', ']', '[', '? ', '/', '《', '》', '・', '/', '，', '「', '」', '！', '｜', '【', '】', '？', '、', '.', '’', '–', '～', '?', ' ']
        for c in list:
            # --- 景點
            try:
                string = string.replace(c, '')
            except:
                string = 'NA'

        # --- 文章網址
        try:
            article_url = 'https://travel.openrice.com' + i['href']
            # print(article_url)
        except:
            # print(article_url)
            article_url = 'NA'

        # print(article_url)
        res1 = get_html(article_url, headers=headers)
        soup = BeautifulSoup(res1.text, 'html.parser')
        # print(res1.text)

        # --- 作者
        # author = soup.select('div[class="f016 aligncenter bluelink"]')
        # print(author)

        # --- 發文時間

        # print(time.text[-10:])
        try:
            time = soup.select('div[class="floatL"]')[0]
            time = time.text[-10:]
            # print(time)
        except:
            time = 'NA'

        # --- 地址
        address = soup.select('table[class="f016"] td')
        # print(address)
        try:
            address = [b.text for b in address][1]
            print(address)
        except:
            address = 'NA'
            # print(address)

        c = soup.select('div[class="roundcontentbox"] span[class="f016b reviewgreenlink"]')
        d = soup.select('div[class="roundcontentbox"] div[class="f016 reviewbody"] ')
        # print(c)
        try:
            for b in c:
                each_title = c[c.index(b)].text
                # print(author)
                content = d[c.index(b)].text

                if content not in new_content:
                    count += 1
                    # print(context)
                    # 存成json格式
                    if search_tag1 == 'attraction':
                        save_data_dict = {'文章網址': article_url,
                                          '發文時間': time,
                                          '標題': each_title,
                                          '景點名稱': string,
                                          '文章內容': content,
                                          '留言': 'NA',
                                          '地址': address,
                                          '縣市': country}
                    elif search_tag1 == 'restaurant':
                        save_data_dict = {'文章網址': article_url,
                                          '發文時間': time,
                                          '標題': each_title,
                                          '餐廳名稱': string,
                                          '美食名稱': 'NA',
                                          '文章內容': content,
                                          '留言': 'NA',
                                          '地址': address,
                                          '縣市': country}

                    save_data_js = json.dumps(save_data_dict, ensure_ascii=False)
                    # print(type(json))
                    path_dir_each = path_dir + '\\' + search_tag + '_' + search_tag1
                    if not os.path.exists(path_dir_each):
                        os.mkdir(path_dir_each)

                    with open(path_dir_each + '\\' + string + '.json', 'a', encoding='utf8') as f:
                        f.write(save_data_js)
                        f.write('\n-----\n')
                    new_content.append(content)
                else:
                    continue
        except:
            author = 'NA'
            content = 'NA'
    print('Complete!!!!!!!!!!')
count = str(count)

def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    return r.status_code

    # 修改為你要傳送的訊息內容


message = '爬了 : ' + count + ' 篇文章'
# 修改為你的權杖內容
token = '9egPV4gL4zLa17A1djM3N5ZUatGi3S2nUwls52NmZJ5'

lineNotifyMessage(token, message)

        #     # 同整存檔內容
        #     total = '標題 : \n' + i.text + '\n內文 : \n' + j.text + '\n'
        #     # print(total)
        #
        #     # 建個別資料夾
        #     path_dir_each = path_dir + '\\' + string
        #     if not os.path.exists(path_dir_each):
        #         os.mkdir(path_dir_each)
        #
        #     # 寫入檔案
        #     with open(path_dir_each + '\\' + i.text + str(len(os.listdir(path_dir_each))) + '.txt', 'w', encoding='utf8') as f:
        #         f.write(total)
        #
        # img_url_list = soup.select('div[class="singlereviewphoto"] [class="IMGBox"] img')
        # # print(img_url_list)
        # for img_url_each in img_url_list:
        #     img_url = ('https://travel.openrice.com' + img_url_each['src'])
        #     # print(img_url)
        #     img_name = (img_url_list.index(img_url_each))
        #     # print(img_name)
        #
        #     location = path_dir_each + '/%s_%s.jpg' % (string.replace('/', ''), img_name)
        #     request.urlretrieve(img_url, location)
            # print('\tDone')
    # print('Complete!!!!!!!!!!')







