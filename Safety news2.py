# coding=utf-8

import datetime
from bs4 import BeautifulSoup
import time
import json
import requests
from operator import itemgetter
import shutil
import os

nowTime = datetime.datetime.now().strftime('%Y-%m-%d')
f = open(str(nowTime) + "-Safety_news" + '.txt', 'w+', encoding='utf-8')
f_C = open(str(nowTime) + "-Github_CVE" + '.txt', 'w+', encoding='utf-8')
f_E = open(str(nowTime) + "-Github_EXP" + '.txt', 'w+', encoding='utf-8')


def freebuf_txt():
    url = "https://www.freebuf.com"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'}
    wbdata = requests.get(url, headers=headers).text
    soup = BeautifulSoup(wbdata, 'lxml')
    # print(soup,file=f)
    news_titles = soup.find_all('span', style='margin-left:30px;margin-right:4px')
    # print(news_titles)
    news_titles1 = soup.find_all('a', class_='text text-line-2')
    # print(news_titles1)
    print('--------------------------freebuf--------------------------', file=f)

    for i, n in zip(news_titles, news_titles1):
        title = n.get_text()
        # print("title:",title)
        title2 = title.strip("\r\n").strip()
        # print("title2:",title2)
        # link = n.get("href")
        link = 'https://www.freebuf.com/' + n.get("href")
        date_f = i.string
        data_freebuf = {
            '标题': title2,
            '链接': link,
            '日期': date_f
        }
        print(data_freebuf, file=f)


def sihou_txt():
    url = "https://www.4hou.com/"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'}
    wbdata = requests.get(url, headers=headers).text
    soup = BeautifulSoup(wbdata, 'lxml')
    news_titles = soup.select("div.new_con > a")
    news_titles1 = soup.select(r"div.avatar_box.newtime > span")
    print('----------------------------4hou----------------------------', file=f)
    for i, n in zip(news_titles1, news_titles):
        date_f = n.string
        title = n.get_text()
        title2 = title.strip("\n")
        link = n.get("href")
        date_f = i.string
        data_sihou = {
            '标题': title2,
            '链接': link,
            '日期': date_f
        }
        print(data_sihou, file=f)


def anquanke():
    url = "https://www.anquanke.com/"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'}
    wbdata = requests.get(url, headers=headers).text
    soup = BeautifulSoup(wbdata, 'lxml')
    news_titles = soup.select("div.info-content > div.title > a")
    news_titles1 = soup.find_all('span', {'style': "vertical-align: middle;"})
    #    print(news_titles1)
    print('----------------------------anquanke----------------------------', file=f)
    '''
    for i in news_titles1 :
        data_f = i.text
        print (data_f)
    '''
    for i, n in zip(news_titles1, news_titles):
        title = n.get_text()
        link = 'https://www.anquanke.com/' + n.get("href")
        data_f = i.text.strip("\n")
        data_anquanke = {
            '标题': title,
            '链接': link,
            '日期': data_f
        }
        print(data_anquanke, file=f)


def getNews():
    year = time.strftime("%Y", time.localtime(time.time()))
    try:
        api = f"https://api.github.com/search/repositories?q=poc+CVE-{year}&sort=updated"
        response = requests.get(api).text
        data = json.loads(response)
        return data
    except Exception as e:
        print(e, "Github链接不通")


def parseData(index):
    item = items[index]
    cve_name = item['name']
    cve_url = item['svn_url']
    cve_des = item['description']
    if not cve_des:  # 描述为空时会返回None
        cve_des = "Null"
    content = f"{cve_name}: {cve_url}, Des: {cve_des}"
    return content


def getNews1():
    year1 = time.strftime("%Y", time.localtime(time.time()))
    try:
        api1 = f"https://api.github.com/search/repositories?q=EXP+CVE-{year1}&sort=updated"
        response1 = requests.get(api1).text
        data1 = json.loads(response1)
        return data1
    except Exception as e:
        print(e, "Github链接不通")


def parseData1(index):
    item1 = items1[index]
    cve_name1 = item1['name']
    cve_url1 = item1['svn_url']
    cve_des1 = item1['description']
    if not cve_des1:  # 描述为空时会返回None
        cve_des1 = "Null"
    content1 = f"{cve_name1}: {cve_url1}, Des: {cve_des1}"
    return content1


if __name__ == '__main__':
    freebuf_txt()
    sihou_txt()
    anquanke()
    total = 0
    total1 = 0  # 初始化
    while True:
        data = getNews()
        data1 = getNews1()
        if total != data['total_count']:
            total = data['total_count']
            items = sorted(data['items'], key=itemgetter('id'), reverse=True)  # 根据items中的id进行排序
        if total1 != data1['total_count']:
            total1 = data1['total_count']
            items1 = sorted(data1['items'], key=itemgetter('id'), reverse=True)  # 根据items中的id进行排序
            content = parseData(0)  # 返回最新的1条
            content1 = parseData1(0)  # 返回最新的1条
            print("------------------------------new_cve------------------------------", file=f_C)
            print(content, file=f_C)
            print("------------------------------new_EXP------------------------------", file=f_E)
            print(content1, file=f_E)
            #        time.sleep(60)
            break

f.close()
f_C.close()
f_E.close()

src_dir_path = str(os.getcwd())
to_dir_path = str(os.getcwd()) + '\\' + 'Github_CVE'  # 存放复制文件的文件夹
to_dir_path2 = str(os.getcwd()) + '\\' + 'Safety_news'
to_dir_path3 = str(os.getcwd()) + '\\' + 'Github_EXP'

key = '-Github_CVE'
key1 = '-Safety_news'
key2 = '-Github_EXP'
if not os.path.exists(to_dir_path):
    os.mkdir(to_dir_path, 1)
if not os.path.exists(to_dir_path2):
    os.mkdir(to_dir_path2, 1)
if not os.path.exists(to_dir_path3):
    os.mkdir(to_dir_path3, 1)
if os.path.exists(src_dir_path):
    for file in os.listdir(src_dir_path):
        # is file
        if os.path.isfile(src_dir_path + '\\' + file):
            if key in file:
                shutil.move(src_dir_path + '\\' + file, to_dir_path + '\\' + file)
            if key1 in file:
                shutil.move(src_dir_path + '\\' + file, to_dir_path2 + '\\' + file)
            if key2 in file:
                shutil.move(src_dir_path + '\\' + file, to_dir_path3 + '\\' + file)
