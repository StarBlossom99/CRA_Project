from datetime import date
import datetime
import matplotlib
from numpy import dtype
import pandas as pd
import matplotlib.pyplot as plt
from plotnine.ggplot import ggsave
from plotnine.scales.limits import alphalim
import seaborn as sns
import plotnine as p9


import matplotlib as mpl 
import matplotlib.font_manager as fm


plt.rcParams['axes.unicode_minus'] = False
plt.rc('font', family='NanumBarunGothic')


fontpath = 'C:/Users/User/Downloads/NanumFontSetup_TTF_GOTHIC/NanumGothic.ttf'
font = fm.FontProperties(fname=fontpath, size=15)


# stock = pd.read_csv('C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/sample4.csv', encoding="utf8")
# graph = p9.ggplot(data = stock, mapping=p9.aes(x='Market_cap', y='Take')) + p9.geom_point(alpha=0.3, color = 'blue')

# titanic = pd.read_csv('/content/sample_data/000100.csv', parse_dates=['일자'])
# print(titanic)
# tit = p9.ggplot(data = titanic, mapping=p9.aes(x='일자', y='현재가')) + p9.geom_line() + theme(axis.text.x = element_text(size=10))
# print(tit)

samsung = pd.read_csv('C:\CRAproject/today_20220119/005930.csv', parse_dates=['일자'], dtype={'종목코드' : str})
samsung = samsung.fillna(0)
samsung = samsung[::-1]
print(samsung.tail(10))
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
print(samsung)


sam = p9.ggplot(data= samsung, mapping=p9.aes(x='일자', y='현재가')) + p9.geom_line(color="black") + p9.geom_line(p9.aes(y='MA5'), color="blue")+ p9.geom_line(p9.aes(y='MA10'), color="red") + p9.geom_line(p9.aes(y='MA20'), color="yellow") + p9.geom_line(p9.aes(y='MA120'), color="green") + p9.geom_line(p9.aes(y='MA60'), color="purple") + p9.ggtitle("삼성전자") + p9.theme(text=p9.element_text(fontproperties=font))
sam = sam + p9.theme(legend_position="bottom", legend_direction="horizontal", legend_title_align="center", legend_box_spacing=0.4, legend_key=p9.element_blank())
print(sam)


#시간에 따른 주가 그래프 만들기
#sam = p9.ggplot(data = samsung, mapping=p9.aes(x='일자', y='현재가')) + p9.geom_line()
ggsave(plot = sam, filename = "005930_graph", width = 20, height = 15, path = "C:/Users/User/Desktop/Study")
