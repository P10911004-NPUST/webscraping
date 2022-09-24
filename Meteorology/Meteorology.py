#  Please enter the date that you wanna start from and end to 

start_year, start_month, start_day = 2021, 9, 1
end_year, end_month, end_day = 2021, 12, 3

# --------------------------------------------------------------

import os
import bs4, requests
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

os.getcwd()

try:
    os.mkdir("C0R190_ChiShan_daily")
except:
    pass

folder_date_list = os.listdir("C0R190_ChiShan_daily")

exist_date = []
for i in folder_date_list:
    split_result = i.split('.')
    exist_date.append(split_result[0])
exist_date = np.array(exist_date, dtype='datetime64').tolist()
    
url='https://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do'


start = datetime.date(year=start_year, month=start_month, day=start_day)
end = datetime.date(year=end_year, month=end_month, day=end_day)
duration = end - start

date_list = []
for i in range(int(duration.days)):
    date_list.append(
        start + datetime.timedelta(days=i)
        )

implement_list = [imp for imp in date_list]
for i in exist_date:
    if i in date_list:
        implement_list.remove(i)
        
  
df1_1 = pd.DataFrame()
for i in range(len(implement_list)):
    URL = url\
        + '?'\
        + 'command=viewMain&'\
        + 'station=C0R190&'\
        + 'stname=%25E8%25B5%25A4%25E5%25B1%25B1&'\
        + 'datepicker='\
        + str(implement_list[i])
    html = requests.get(URL)
    sp = bs4.BeautifulSoup(html.text,'lxml')  # 解析網站
    txt = sp.text.split()  # 以split分隔讀取到的網頁內容並存成list
    print(f'Getting {implement_list[i]}')  # 讀取一夜成功則輸出提示一次
    data = txt[144:]
    colnames = np.array(data[:20])
    colnames = np.delete(colnames, [4,6,19])
    data_list = data[20:]
    data_value = np.array(data_list).reshape(-1, 17)
    df1 = pd.DataFrame(data = data_value, columns = colnames)
    df1['DATE'] = str(implement_list[i])
    df1.insert(0, 'DATE', df1.pop('DATE'))
    
    df1.to_csv("C0R190_ChiShan_daily/%s.csv" % implement_list[i],
               index=False,
               sep=',')    
    df1_1 = pd.concat([df1_1,df1], axis=0)
    

folder_date_list2 = os.listdir("C0R190_ChiShan_daily")
df2 = pd.DataFrame()
for i in folder_date_list2:
    _df2 = pd.read_csv("C0R190_ChiShan_daily/%s" % i)
    df2 = pd.concat([df2, _df2], axis=0)
df2.to_csv("All_Data.csv",
           index=False,
           sep=',')  

df3 = df2[['DATE','Temperature']].replace({'/':np.nan}).dropna()
df3 = df3.replace({'...':np.nan}).dropna()
df3 = df3.replace({'X':np.nan}).dropna()
df3['Temperature'] = np.float64(df3['Temperature'])

df_stat = df3.groupby('DATE').agg([np.max, np.min, np.mean])
df_stat = df_stat.rename(columns={'amax':'Tmax','amin':'Tmin','mean':'Tmean'})
df_stat = df_stat['Temperature']

df_stat['GDD'] = ((df_stat.Tmax + df_stat.Tmean) / 2) - 10
df_stat['DATE'] = np.array(df_stat.index, dtype='datetime64')


from matplotlib.font_manager import fontManager
from matplotlib import rcParams
fontManager.ttflist

rcParams['font.family'] = 'Palatino Linotype'
rcParams['axes.unicode_minus'] = False

plt.figure(figsize=(15,9), dpi=600)
plt.plot_date(df_stat.DATE, df_stat.Tmean, fmt='d',
              label='Tmean', linestyle='solid', color='black')
plt.plot_date(df_stat.DATE, df_stat.Tmax, fmt='r',
              label='Tmax', linestyle='--', color='red')
plt.plot_date(df_stat.DATE, df_stat.Tmin, fmt='r',
              label='Tmin', linestyle='--', color='blue')
plt.fill_between(df_stat.DATE, df_stat.Tmean, df_stat.Tmax,
                color = 'red', alpha=0.2, linewidth=0)
plt.fill_between(df_stat.DATE, df_stat.Tmean, df_stat.Tmin,
                color = 'blue', alpha=0.2, linewidth=0)
#plt.xticks(rotation=0)
plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
#plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
#plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=10))
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel('DATE', labelpad=20, fontsize=14)
plt.ylabel('Temperature ($^\circ$C)', labelpad=20, fontsize=14)
plt.legend(loc='upper center', bbox_to_anchor=(0.5,1.05), ncol=3)
plt.savefig("Daily_Data.jpg", dpi=600, bbox_inches='tight')

df_stat['AGDD'] = np.cumsum(df_stat.GDD)
plt.figure(figsize=(15,9), dpi=600)
plt.plot_date(df_stat.DATE, df_stat.AGDD, fmt='d',
              linestyle='solid', color='black')
plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel('DATE', labelpad=20, fontsize=14)
plt.ylabel('AGDD ($^\circ$C)', labelpad=20, fontsize=14)
plt.savefig("AGDD.jpg", dpi=600, bbox_inches='tight')