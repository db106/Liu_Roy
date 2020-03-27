import requests
from bs4 import BeautifulSoup
import os

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}

# 開檔
path_dir = 'E:\\專題\\restaurant'
if not os.path.exists(path_dir):
    os.mkdir(path_dir)

search_tag = '宜蘭縣'   # 手動更改英文

page = 1
for i in range(1, 68):
    url = 'https://ifoodie.tw/explore/%s/list?page=%s' % (search_tag, i)
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    # print(soup)
    title = soup.select('div[class="jsx-1102741263 info-rows"] ')
    # print(title)

    for j in title:
        # print(j)
        title = j.select('a[class="jsx-1102741263 title-text"]')
        each_title = title[0].text
        address = j.select('div[class="jsx-1102741263 address-row"]')
        each_address = address[0].text
        tag = j.select('a[class="jsx-1102741263 category"] ')[1:]
        # print(tag)
        each_tag_list = [k.text for k in tag]
        # print()

        # 同整存檔內容
        total = '{' + '"店名":' + '"' + each_title + '"' + ',' + '"地址":' + '"' + each_address + '"' + ',' + '"tag":' + '"' + str(each_tag_list) + '"' + '}'
        # print(total)

        # # 寫入檔案
        with open(path_dir + '\\' + search_tag + '.txt', 'a', encoding='utf8') as f:
            f.write(total+"\n")
            f.write('-----\n')
    print('Complete!!!!!!!!!!')


