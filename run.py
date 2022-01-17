# -*- coding: utf-8 -*-
from pykiwoom.kiwoom import *
import datetime
import time


import os
from numpy import dtype, nan
import pandas as pd 
import pymysql 
import matplotlib.pyplot as plt 
import csv




# 문자열로 오늘 날짜 얻기
now = datetime.datetime.now()
today = now.strftime("%Y%m%d")



# 날짜별로 전체 주식 정보를 한 테이블로 만들어서 DB에 등록
dir_path = "C:\CRAproject/today_20211225"

conn = pymysql.connect(host="localhost", user = 'root', password='Axenon!0927', db = 'today',charset = 'utf8') 
curs = conn.cursor(pymysql.cursors.DictCursor)

sql = "ALTER TABLE date_20211228 ADD Dividends float null"
curs.execute(sql)

for (root, directories, files) in os.walk(dir_path):
    for file in files:
        if '.csv' in file:
            file_path = os.path.join(root, file)
            file_name = file_path[-10:-4]

            stores_info = pd.read_csv(file_path, encoding="utf8", sep=",", dtype={'종목코드' : str})
            stores_info2 = stores_info.fillna(0)
            for index, row in stores_info2.iterrows():
                print(str(row.종목코드))
                tu = ( index, str(row.종목코드), row.종목명, row.연중최고, row.연중최저, row.시가총액, row.PER, row.EPS, row.ROE, row.PBR, row.EV, row.BPS, row.매출액, row.영업이익, row.당기순이익, row.시가, row.고가, row.저가, row.현재가, row.전일대비, row.등락율, row.거래량) 
                curs.execute("INSERT IGNORE INTO date_" + today + "(count, 종목코드, 종목명, 연중최고, 연중최저, 시가총액, PER, EPS, ROE, PBR, EV, BPS, 매출액, 영업이익, 당기순이익, 시가, 고가, 저가, 현재가, 전일대비, 등락율, 거래량) values(%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s, %s)", tu)

conn.commit()
conn.close()
print("the end")