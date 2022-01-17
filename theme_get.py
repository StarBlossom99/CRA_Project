# -*- coding: utf-8 -*-
from pykiwoom.kiwoom import *
import datetime
import time
import pprint

import os
from numpy import dtype,nan
import pandas as pd 
import pymysql 
import matplotlib.pyplot as plt 
import csv


# kiwoom = Kiwoom()
# kiwoom.CommConnect(block=True)




themes = {'141','140','571','570','830','501','562','561','560','572','600','500','458','452','353','250','170','202','319','201','200','471','470','312','270','245','160','210','211','480','610','316','213','456','517','281','280','130','360','363','361','362','550','551','557','556','555','552','554','553','212','313','290','453','420','421','611','171','315','530','459','310','364','810','515','516','203','318','370','286','820','154','261','800','214','232','230','231','110','111','314','311','400','351','352','350','256','255','242','241','240','243','215','262','454','455','450','317','180','181','223','220','222','221','300','910','430','410','260','284','282','283','285','451','920','900','457','244','153','520','103','102','101','100','481','850','121','172','152','151','150','291','120','330','840','511','518','510','514','513','512','173'}


sum = 0

conn = pymysql.connect(host="localhost", user = 'root', password='Axenon!0927', db = 'today',charset = 'utf8') 
curs = conn.cursor(pymysql.cursors.DictCursor)

# curs.execute("ALTER TABLE date_20211228 ADD Dividends float null default 0")
dir_path = "C:\CRAproject/"


sql = "ALTER TABLE date_20211228 ADD Dividends_Rate float null default 0"
sql2 = "UPDATE date_20211228 SET Dividends_Rate = Dividends / 현재가 "
curs.execute(sql2)
# dividends = pd.read_csv("C:\CRAproject/Dividends.csv", encoding="utf8", sep=",", dtype={'종목코드' : str ,'주당배당금' : str})
# dividends = dividends.fillna(0)
# for index, row in dividends.iterrows():
#     print(row.종목코드)
#     tu = (row.주당배당금,row.종목코드)
#     sql = "UPDATE date_20211228 SET Dividends = %s WHERE 종목코드 = '%s'" % tu
#     print(sql)
#     curs.execute(sql)

# for (root, directories, files) in os.walk(dir_path):
#     for file in files:
#         if '.csv' in file:
#             file_path = os.path.join(root, file)
#             file_name = file_path[-10:-4]

#             stores_info = pd.read_csv(file_path, encoding="utf8", sep=",", dtype={'종목코드' : str})
#             stores_info2 = stores_info.fillna(0)
#             for index, row in stores_info2.iterrows():
#                 print(str(row.종목코드))
#                 tu = ( index, str(row.종목코드), row.종목명, row.연중최고, row.연중최저, row.시가총액, row.PER, row.EPS, row.ROE, row.PBR, row.EV, row.BPS, row.매출액, row.영업이익, row.당기순이익, row.시가, row.고가, row.저가, row.현재가, row.전일대비, row.등락율, row.거래량) 
#                 curs.execute("INSERT IGNORE INTO date_" + today + "(count, 종목코드, 종목명, 연중최고, 연중최저, 시가총액, PER, EPS, ROE, PBR, EV, BPS, 매출액, 영업이익, 당기순이익, 시가, 고가, 저가, 현재가, 전일대비, 등락율, 거래량) values(%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s, %s)", tu)

conn.commit()
conn.close()

for theme in themes:
    items = kiwoom.GetThemeGroupCode(theme)
    # print("theme code is " + theme + " count is " + str(len(items)))
    # print(items)
    sum = sum + len(items)
    for item in items:
        tu = (int(theme), item)
        sql = "UPDATE date_20211228 SET Theme = " + theme + " WHERE 종목코드 = '" + item + "'"
        print(sql)
        curs.execute(sql)

print("the end")
