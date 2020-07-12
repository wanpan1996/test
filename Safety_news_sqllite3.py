# coding=utf-8

import sqlite3
import datetime
from bs4 import BeautifulSoup
import time
import json
import requests
from operator import itemgetter
import shutil
import os
import hashlib

sqlite3db = 'test.db'
conn = sqlite3.connect(sqlite3db)
c = conn.cursor()
nowTime = datetime.datetime.now().strftime('%Y-%m-%d')
f = open(str(nowTime) + "-Safety_news" + '.txt', 'w+', encoding='utf-8')

def getmd5(filename):
    file_txt = open(filename, 'rb').read()
    m=hashlib.md5(file_txt)
    return m.hexdigest()

def delete_1(filepath):

    path = str(os.getcwd())
#    path = input("path: ")
#    all_md5 = {}
    all_size = {}
    total_file = 0
    total_delete = 0
    for file in os.listdir(filepath):
        total_file += 1
        real_path = os.path.join(filepath, file)
        if os.path.isfile(real_path) == True:
            size = os.stat(real_path).st_size
            name_and_md5 = [real_path, '']
            if size in all_size.keys():
                new_md5 = getmd5(real_path)
                if all_size[size][1] == '':
                    all_size[size][1] = getmd5(all_size[size][0])
                if new_md5 in all_size[size]:
                    os.remove(os.path.join(filepath, file))
                    total_delete += 1
                else:
                    all_size[size].append(new_md5)
            else:
                all_size[size] = name_and_md5

def freebuf_txt():
    url = "https://www.freebuf.com/articles/web"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'}
    wbdata = requests.get(url, headers=headers).text
    soup = BeautifulSoup(wbdata, 'lxml')
    news_titles = soup.select("div.title-left > a ")
    news_titles1 = soup.select("div.item-bottom > p > span")
    #print(news_titles1)
    print('--------------------------freebuf--------------------------', file=f)
    for i,n in zip(news_titles1,news_titles):
        title = n.get_text()
        title2 = title.strip("\n")
        #        link = n.get("href")
        link = 'https://www.freebuf.com/' + n.get("href")
        date_f = i.string
        data_freebuf = {
            '标题': title2,
            '链接': link,
            '日期': date_f
        }
        print(data_freebuf,file=f)

def sihou_txt():
    url = "https://www.4hou.com/"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'}
    wbdata = requests.get(url, headers=headers).text
    soup = BeautifulSoup(wbdata, 'lxml')
    news_titles = soup.select("div.new_con > a")
    news_titles1 = soup.select(r"div.avatar_box.newtime > span")
    print('----------------------------4hou----------------------------',file=f)
    for i,n in zip(news_titles1,news_titles):
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
        print(data_sihou,file=f)


def anquanke():
    url = "https://www.anquanke.com/"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'}
    wbdata = requests.get(url, headers=headers).text
    soup = BeautifulSoup(wbdata, 'lxml')
    news_titles = soup.select("div.info-content > div.title > a")
    news_titles1 = soup.find_all('span', {'style': "vertical-align: middle;"})
#    print(news_titles1)
    print('----------------------------anquanke----------------------------',file=f)
    '''
    for i in news_titles1 :
        data_f = i.text
        print (data_f)
    '''
    for i,n in zip(news_titles1,news_titles):
        title = n.get_text()
        link = 'https://www.anquanke.com/' + n.get("href")
        data_f = i.text.strip("\n")
        data_anquanke = {
            '标题': title,
            '链接': link,
            '日期': data_f
        }
        print(data_anquanke,file=f)

############
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
    content = f"{cve_name} --- {cve_url} --- {cve_des}"
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
    exp_name = item1['name']
    exp_url = item1['svn_url']
    exp_des = item1['description']
    if not exp_des:  # 描述为空时会返回None
        exp_des = "Null"
    content1 = f"{exp_name} --- {exp_url} --- {exp_des}"
    return content1


if __name__ == '__main__':
    freebuf_txt()
    sihou_txt()
    anquanke()
    total = 0
    total1 =0 # 初始化
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
#            print("------------------------------new_cve------------------------------")
#            print('原始数据：',content)
#            print("------------------------------new_EXP------------------------------")
 #           print('原始数据：',content1)
            #        time.sleep(60)
            break
f.close()
#处理github数据
cve_content= str(content)
exp_content1 = str(content1)
cve_content = cve_content.split("---")
exp_content1 = exp_content1.split("---")
#处理cve 格式化参数
cve_name = cve_content[0]
curl_addr = cve_content[1].lstrip().replace(',','')
cdes_string = cve_content[2].lstrip()

#处理exp 格式化参数
exp_name = exp_content1[0]
eurl_addr = exp_content1[1].lstrip().replace(',','')
edes_string = exp_content1[2].lstrip()


try:
# Create table
    c.execute('''CREATE TABLE cve (id integer primary key autoincrement, name text, url text UNIQUE, Description text)''')
    c.execute('''CREATE TABLE exp (id integer primary key autoincrement, name text, url text UNIQUE, Description text)''')
# 新建表xyz，若已有该表则忽略
# CREATE TABLE IF NOT EXISTS cvetest1
#在表mytable中插入一条记录，若存在即忽略
#cur.execute("INSERT OR IGNORE INTO mytable (id,name) VALUES ('0','狗蛋')")

except Exception as e:
#cve!
    try:
        c.execute('INSERT  INTO cve (name,url,Description) VALUES (?, ? ,?)',
                      (cve_name, curl_addr, cdes_string))
#        c.executemany('INSERT OR IGNORE INTO cve (name,url,Description) VALUES (?, ? ,?)',((cve_name, curl_addr, cdes_string)))
#,(exp_name, eurl_addr, edes_string)
# Insert a row of data
    except Exception as e:
        print("警告 cvedb数据插入失败" ,"错误：",e)
        print("重复数据为：", curl_addr)
    else:
        print("新数据插入cvedb成功!")
#exp！
    try:
        c.execute('INSERT INTO exp (name,url,Description) VALUES (?, ? ,?)',
                  (exp_name, eurl_addr, edes_string))
    #        c.executemany('INSERT OR IGNORE INTO cve (name,url,Description) VALUES (?, ? ,?)',((cve_name, curl_addr, cdes_string)))
    # ,(exp_name, eurl_addr, edes_string)
    # Insert a row of data
    except Exception as e:
        print("警告 expdb数据插入失败" ,"错误：",e)
        print("重复数据为：", eurl_addr)
    else:
        print("新数据插入expdb成功!")

else:
    print('----------------------------')
    print("Welcome to try Safety news2!")
    print('----------------------------')
    print('Create database test.db successfully!')
    print('----------------------------')
    print('cvetest.db in :',str(os.getcwd()))
    print('----------------------------')
    print('Run again to write data')
    print('----------------------------')



# Save (commit) the changes
for row in c.execute('SELECT * FROM cve ORDER BY id'):
    print('新cve数据为：',row)
for row in c.execute('SELECT * FROM exp ORDER BY id'):
    print('新exp数据为：',row)
#c.execute('delete from cve where id = 1')
#c.execute('DROP TABLE cve')
conn.commit()
conn.close()


src_dir_path = str(os.getcwd())
# 存放复制文件的文件夹
to_dir_path2 = str(os.getcwd()) + '\\' + 'Safety_news'

key1 = '-Safety_news'

if not os.path.exists(to_dir_path2):
    os.mkdir(to_dir_path2, 1)
if os.path.exists(src_dir_path):
    for file in os.listdir(src_dir_path):
        # is file
        if os.path.isfile(src_dir_path + '\\' + file):
            if key1 in file:
                shutil.move(src_dir_path + '\\' + file, to_dir_path2 + '\\' + file)
                delete_1(to_dir_path2)
