import os
from numpy import nan
import pandas as pd 
import pymysql 
import matplotlib.pyplot as plt 
import csv


dir_path = "C:\CRAproject\stockdb"

conn = pymysql.connect(host="localhost", user = 'root', password='Axenon!0927', db = 'stock',charset = 'utf8') 
curs = conn.cursor(pymysql.cursors.DictCursor)

for (root, directories, files) in os.walk(dir_path):
    for file in files:
        if '.csv' in file:
            file_path = os.path.join(root, file)
            file_name = file_path[-10:-4]
            print(file_name)

            sql = "CREATE TABLE stock_" + file_name + "( count int null , 현재가 int null , 거래량 int null , 거래대금 int null , 일자 date not null primary key, 시가 int null, 고가 int null, 저가 int null)"
            print(sql)
            curs.execute(sql)

            stores_info = pd.read_csv(file_path, encoding="utf8", sep=",")

            for index, row in stores_info.iterrows():
                tu = ( index, row.현재가, row.거래량, row.거래대금, row.일자, row.시가, row.고가, row.저가) 
                curs.execute("INSERT IGNORE INTO stock_" + file_name + "(count, 현재가, 거래량, 거래대금, 일자, 시가, 고가, 저가) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)" ,tu)
       
conn.commit()
conn.close()
print("the end")
           