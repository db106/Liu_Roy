import os
import json
import time
import requests
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys

# 開檔
path_dir = 'E:\專題\google'
if not os.path.exists(path_dir):
    os.mkdir(path_dir)

driver = Chrome('./chromedriver')

url = 'https://www.google.com/webhp'
count = 0
search_tag_set = set()
with open(r'E:\專題\景點名\台北.txt', 'r', encoding="utf-8") as f:
    f = f.readlines()
    for search_tag in f:
        search_tag = search_tag.replace('\n', '')
        if search_tag not in search_tag_set:
            search_tag_set.add(search_tag)
            # print(search_tag)

            driver.get(url)
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input').send_keys(search_tag)   # 搜索
            # print(search_tag)
            # time.sleep(5)
            if url == driver.current_url:
                driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)   # Enter
            time.sleep(1)
            html = driver.page_source
            # print(html)

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            a = soup.select('div[class="UYKlhc"]')
            # print(a)
            try:
                stop_time = a[0].text
            except:
                stop_time = 'NA'
            count += 1
            # print(type(count))

            time.sleep(1)
            save_data_dict = {'地點': search_tag,
                              '停留時間': stop_time}
            print(save_data_dict)

            save_data_js = json.dumps(save_data_dict, ensure_ascii=False)

            with open(path_dir + '\\' + 'stop' + '.txt', 'a', encoding='utf8') as f:
                f.write(save_data_js)
                f.write('\n-----\n')


count = str(count)
# print(count)
def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    return r.status_code

    # 修改為你要傳送的訊息內容


message = '爬了 : ' + count + ' 個景點'
# 修改為你的權杖內容
token = '9egPV4gL4zLa17A1djM3N5ZUatGi3S2nUwls52NmZJ5'

lineNotifyMessage(token, message)

































driver.close()
