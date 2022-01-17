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

stock = pd.read_csv('C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/sample4.csv', encoding="utf8")
graph = p9.ggplot(data = stock, mapping=p9.aes(x='Market_cap', y='Take')) + p9.geom_point(alpha=0.3, color = 'blue')

titanic = pd.read_csv('C:/CRAproject/train.csv')
tit = p9.ggplot(data = titanic, mapping=p9.aes(x='Age', y='Fare')) + p9.geom_point()

samsung = pd.read_csv('C:/CRAproject/stockdb/005930.csv', parse_dates=['일자'], dtype={'종목코드' : str})
samsung = samsung.fillna(0)
print(samsung)

sk = pd.read_csv('C:/CRAproject/stockdb/000660.csv', parse_dates=['일자'], dtype={'종목코드' : str})
sk = sk.fillna(0)
print(sk)

# 시간에 따른 주가 그래프 만들기
sam = p9.ggplot(data = samsung, mapping=p9.aes(x='일자', y='현재가')) + p9.geom_line()
ggsave(plot = sam, filename = "fifth_graph", path = "C:/Users/User/Desktop/Study")