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

conn = pymysql.connect(host="localhost", user = 'root', password='Axenon!0927', db = 'stock_price',charset = 'utf8') 
curs = conn.cursor(pymysql.cursors.DictCursor)
dir_path = "C:\CRAproject/today_%s" % today

for (root, directories, files) in os.walk(dir_path):
    for file in files:
        if '.csv' in file:
            file_path = os.path.join(root, file)
            file_name = file_path[-10:-4]
            create_sql = "CREATE TABLE %s_%s(일자 date not null primary key, 현재가 int null, 거래량 int null, 거래대금 int null, 시가 int null, 고가 int null, 저가 int null)" % (today, file_name)
            curs.execute(create_sql)

            stores_info = pd.read_csv(file_path, encoding="utf8", sep=",")
            stores_info = stores_info.fillna(0)
            print(file_name)
            for index, row in stores_info.iterrows():
                tu = (row.일자, row.현재가, row.거래량, row.거래대금, row.시가, row.고가, row.저가)
                curs.execute("INSERT IGNORE INTO " + today + "_" + file_name + "(일자, 현재가, 거래량, 거래대금, 시가, 고가, 저가) values (%s,%s,%s,%s,%s,%s,%s)", tu)

conn.commit()
conn.close()