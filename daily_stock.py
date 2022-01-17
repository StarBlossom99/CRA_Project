import os
from numpy import datetime64, dtype, nan
import pandas as pd 
import pymysql 
import matplotlib.pyplot as plt 
import csv

import datetime
import time

now = datetime.datetime.now()
today = now.strftime("%Y%m%d")

conn = pymysql.connect(host="localhost", user = 'root', password='Axenon!0927', db = 'daily_stock',charset = 'utf8') 
curs = conn.cursor(pymysql.cursors.DictCursor)
dir_path = "C:\CRAproject/entire_%s" % today

create_sql = "CREATE TABLE date_%s(count int primary key auto_increment, 종목코드 varchar(10) null, 종목명 varchar(40) null, 연중최고 int null, 연중최저 int null, 시가총액 int null, PER float null, EPS float null, PBR float null, ROE float null, EV float null, BPS float null, 매출액 int null, 영업이익 int null, 당기순이익 int null, 시가 int null, 고가 int null, 저가 int null, 현재가 int null, 전일대비 int null, 등락율 float null, 거래량 int null, Theme int null default 0, Dividends float null default 0, Dividends_Rate float null default 0)" % today
curs.execute(create_sql)
#DB저장 과정
for (root, directories, files) in os.walk(dir_path):
    for file in files:
        if '.csv' in file:
            file_path = os.path.join(root, file)
            file_name = file_path[-10:-4]
            
            stores_info = pd.read_csv(file_path, encoding="utf8", sep=",", dtype={'종목코드' : str})
            stores_info = stores_info.fillna(0)
            print(file_name)
            for index, row in stores_info.iterrows():
                tu = ( index, str(row.종목코드), row.종목명, row.연중최고, row.연중최저, row.시가총액, row.PER, row.EPS, row.ROE, row.PBR, row.EV, row.BPS, row.매출액, row.영업이익, row.당기순이익, row.시가, row.고가, row.저가, row.현재가, row.전일대비, row.등락율, row.거래량) 
                curs.execute("INSERT IGNORE INTO date_" + today + "(count, 종목코드, 종목명, 연중최고, 연중최저, 시가총액, PER, EPS, ROE, PBR, EV, BPS, 매출액, 영업이익, 당기순이익, 시가, 고가, 저가, 현재가, 전일대비, 등락율, 거래량) values(%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s, %s)", tu)
conn.commit()
conn.close()