import os
import time
import json
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from itertools import combinations, permutations

path_dir = 'E:\專題\google'
if not os.path.exists(path_dir):
    os.mkdir(path_dir)

driver = Chrome('./chromedriver')

url = 'https://www.google.com.tw/maps/dir///@24.9554014,121.2384829,17z/data=!4m2!4m1!3e0?hl=zh-TW'

# search_tag = ['中壢夜市', '中原夜市', '淡水老街']
search_tag_list = []
# print(search_tag)
with open(r'E:\專題\景點名\景點.txt', 'r', encoding="utf-8") as f:
    f = f.readlines()
    for each_line in f:
        if each_line not in search_tag_list:
            search_tag_list.append(each_line)


    search_tag_list = list(combinations(search_tag_list, 2))
    for i in search_tag_list:
        # print(i)
        search_tag = i

        # print(search_tag)

        driver.get(url)
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="sb_ifc50"]/input').send_keys(search_tag[0].replace('\n', ''))   # --- 輸入起點
        # print(start)
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="sb_ifc51"]/input').send_keys(search_tag[1].replace('\n', ''))   # --- 輸入目的
        # print(k)
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="sb_ifc51"]/input').send_keys(Keys.ENTER)
        time.sleep(5)
        driver.find_element_by_css_selector('span#section-directions-trip-details-msg-0').click()
        time.sleep(3)
        # html = driver.page_source
        # print(html)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # print(soup)

        a = soup.select('h1[class="section-trip-summary-title"]')
        c = soup.select('h2[class="directions-mode-group-title"]')
        # print(c)
        address = [d.text for d in c]

        # print(b)
        for i in a:
            # print(i.text.split('-')[0])
            time.sleep(1)

            save_data_dict = {'出發地點': search_tag[0].replace('\n', ''),
                              '目的地': search_tag[1].replace('\n', ''),
                              '所需時間': i.text.split('-')[0],
                              '路徑': address}
            print(save_data_dict)

            save_data_js = json.dumps(save_data_dict, ensure_ascii=False)

            with open(path_dir + '\\' + 'use' + '.txt', 'a', encoding='utf8') as f:
                f.write(save_data_js)
                f.write('\n-----\n')



































































driver.close()
