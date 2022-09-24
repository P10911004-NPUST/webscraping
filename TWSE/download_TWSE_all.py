import os
import numpy as np
import pandas as pd
import bs4
#import urllib.request
import requests
import random
import time
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

url = "https://www.twse.com.tw/exchangeReport/MI_INDEX?response=html&"
working_directory = "D:/jklai/Python/TWSE/html_data"

company_number = 9999
company_name = 'ALL'
start_date = date(2004, 2, 11)
end_date = date.today()

save_directory = os.path.join(working_directory + f'/{company_number}_{company_name}')

if not os.path.exists(save_directory):
    os.mkdir(save_directory)

os.chdir(save_directory)

def date_convert(date0): # 110 => 2021
    date1 = date0.split("/")
    return date(int(date1[0]) + 1911, int(date1[1]), int(date1[2])).strftime('%Y/%m/%d')

def date_range(date1, date2):
    n = 0
    while date1 + timedelta(days=n) <= date2:
        yield date1 + timedelta(days=n)
        n = n + 1

def month_range(date1, date2):
    n = 0
    while date1.replace(day=1) + relativedelta(months=n) <= date2.replace(day=1):
        yield date1.replace(day=1) + relativedelta(months=n)
        n = n + 1

def download_data(_url, _path):
    #def report_hook(count, blockSize, totalSize):
    #    print( "\rDownloading: %f%" % ((count*blockSize) / totalSize), end="")
    #def download_progress_hook(count, blockSize, totalSize):
    #    print(count, blockSize, totalSize)

    if not os.path.exists(_path):
        print("Downloading data from %s" % _url)
        #urllib.request.urlretrieve(_url, _path, reporthook=download_progress_hook)
        html = requests.get(_url)
        eval_html = bs4.BeautifulSoup(html.text, 'lxml')  # 解析網站
        txt = eval_html.text.split()  # 以split分隔讀取到的網頁內容並存成list
        df = pd.DataFrame(txt)
        df.to_csv(_path, index=False, sep=',', header=False)      
        time.sleep(random.uniform(1,10))
        
    else:
        print("File already exists!")
        
    filename = os.path.basename(_path)
    filesize = os.path.getsize(os.path.join(save_directory, filename))
    print( "File size = %.2f Mb" % (filesize/1024/1024) )
    
# MI_INDEX
for i in date_range(start_date, end_date):
    print(i.strftime('%Y%m%d'))
    _url = url + "date=%s&" % i.strftime('%Y%m%d') + "type=%s" % str(company_name)
    _path = save_directory + "/" + i.strftime('%Y%m%d') + ".csv"
    download_data(_url, _path)
print("\nMI_INDEX Download finished!") 

# Foreign
save_directory1 = os.path.join(working_directory + f'/{company_number}_{company_name}_foreign')

if not os.path.exists(save_directory1):
    os.mkdir(save_directory1)

for i in date_range(start_date, end_date):
    print(i.strftime('%Y%m%d'))
    _url = "https://www.twse.com.tw/fund/T86?response=html&" +\
         "date=%s&" % i.strftime('%Y%m%d') +\
              "selectType=01"
    _path = save_directory1 + "/" + i.strftime('%Y%m%d') + ".csv"
    download_data(_url, _path)
print("\nT86_Foreign Download finished!") 


# Short Sales
save_directory2 = os.path.join(working_directory + f'/{company_number}_{company_name}_short')

if not os.path.exists(save_directory2):
    os.mkdir(save_directory2)

for i in date_range(start_date, end_date):
    print(i.strftime('%Y%m%d'))
    _url = "https://www.twse.com.tw/exchangeReport/TWTASU?response=html&" +\
         "date=%s" % i.strftime('%Y%m%d')
    _path = save_directory2 + "/" + i.strftime('%Y%m%d') + ".csv"
    download_data(_url, _path)
print("\nTWTASU_Short-Sales Download finished!") 


# Block Trade
save_directory3 = os.path.join(working_directory + f'/{company_number}_{company_name}_foreign')

if not os.path.exists(save_directory3):
    os.mkdir(save_directory3)

for i in date_range(start_date, end_date):
    print(i.strftime('%Y%m%d'))
    _url = "https://www.twse.com.tw/block/BFIAUU?response=html&" +\
         "date=%s&" % i.strftime('%Y%m%d') + \
             "&selectType=S"
    _path = save_directory3 + "/" + i.strftime('%Y%m%d') + ".csv"
    download_data(_url, _path)
print("\nBFIAUU_Block-Trade Download finished!") 