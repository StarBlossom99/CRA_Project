import os
from numpy import dtype
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl 
import matplotlib.font_manager as fm

plt.rcParams['axes.unicode_minus'] = False
plt.rc('font', family='NanumBarunGothic')
plt.rcParams["figure.figsize"] = (20,15)

fontpath = 'C:/Users/User/Downloads/NanumFontSetup_TTF_GOTHIC/NanumGothic.ttf'
font = fm.FontProperties(fname=fontpath, size=15)

samsung = pd.read_csv('C:\CRAproject/today_20220119/005930.csv', parse_dates=['일자'], dtype={'종목코드' : str})
samsung = samsung.fillna(0)
samsung = samsung[::-1]

ma5 = samsung['현재가'].rolling(window=5).mean()
ma10 = samsung['현재가'].rolling(window=10).mean()
ma20 = samsung['현재가'].rolling(window=20).mean()
ma60 = samsung['현재가'].rolling(window=60).mean()
ma120 = samsung['현재가'].rolling(window=120).mean()
# print(ma5.tail(10))

samsung.insert(len(samsung.columns), "MA5", ma5)
samsung.insert(len(samsung.columns), "MA10", ma10)
samsung.insert(len(samsung.columns), "MA20", ma20)
samsung.insert(len(samsung.columns), "MA60", ma60)
samsung.insert(len(samsung.columns), "MA120", ma120)

samsung.rename(columns= {'현재가':'Price'}, inplace=True)
print(samsung)

plt.figure(num="Samsung")
plt.title("Samsung Stock Price", fontproperties=font)
plt.xlabel("일자",fontproperties=font)
plt.ylabel("현재가",fontproperties=font)
ax = plt.gca()

print(samsung)
samsung.plot(kind='line', ax=ax, y = ['Price', 'MA5', 'MA10', 'MA20', 'MA60', 'MA120'], x = '일자')
os.chdir("C:/Users/User/Desktop/Study")
plt.savefig('samsung1.png')
