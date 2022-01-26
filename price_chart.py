import os
from numpy import dtype
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl 
import matplotlib.font_manager as fm

class graph:
    def setdata(self, code, date, name):
        self.code = code
        self.date = date
        self.name = name

    def make_graph(self):
        plt.rcParams['axes.unicode_minus'] = False
        plt.rc('font', family='NanumBarunGothic')
        plt.rcParams["figure.figsize"] = (20,15)

        fontpath = 'C:/Users/User/Downloads/NanumFontSetup_TTF_GOTHIC/NanumGothic.ttf'
        font = fm.FontProperties(fname=fontpath, size=15)

        file_path = "C:/CRAproject/today_" + self.date + "/" + self.code + ".csv"
        print(file_path)
        thing = pd.read_csv(file_path, parse_dates=['일자'], dtype={'종목코드' : str})
        thing = thing.fillna(0)
        thing = thing[::-1]

        ma5 = thing['현재가'].rolling(window=5).mean()
        ma10 = thing['현재가'].rolling(window=10).mean()
        ma20 = thing['현재가'].rolling(window=20).mean()
        ma60 = thing['현재가'].rolling(window=60).mean()
        ma120 = thing['현재가'].rolling(window=120).mean()

        #moving average column addition
        thing.insert(len(thing.columns), "MA5", ma5)
        thing.insert(len(thing.columns), "MA10", ma10)
        thing.insert(len(thing.columns), "MA20", ma20)
        thing.insert(len(thing.columns), "MA60", ma60)
        thing.insert(len(thing.columns), "MA120", ma120)

        #column name change
        thing.rename(columns= {'현재가':'Price'}, inplace=True)
        print(thing)

        plt.figure(num=self.name)
        plt.title(self.name + " 주가 차트", fontproperties=font)
        plt.xlabel("일자",fontproperties=font)
        plt.ylabel("현재가",fontproperties=font)
        ax = plt.gca()

        print(thing)
        thing.plot(kind='line', ax=ax, y = ['Price', 'MA5', 'MA10', 'MA20', 'MA60', 'MA120'], x = '일자')
        os.chdir("C:/Users/User/Desktop/Study")
        plt.savefig(self.name + ".png")





