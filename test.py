from pykiwoom.kiwoom import *
import datetime
import time


import os
from numpy import nan
import pandas as pd 
import pymysql 
import matplotlib.pyplot as plt 
import csv

conn = pymysql.connect(host="localhost", user = 'root', password='Axenon!0927', db = 'daily_stock',charset = 'utf8') 
curs = conn.cursor(pymysql.cursors.DictCursor)

data_text = []

curs.execute("select 종목코드 from date_20220203 where 종목코드=005930")
result = curs.fetchone()
temp = "종목코드 : " + str(result)[10:-2]
data_text.append(temp)
# print(temp)

curs.execute("select 종목명 from date_20220203 where 종목코드=005930")
result = curs.fetchone()
temp = "종목명 : " + str(result)[9:-2]
data_text.append(temp)
# print(temp)

curs.execute("select 연중최고 from date_20220203 where 종목코드=005930")
result = curs.fetchone()
temp = "연중최고 : " + str(result)[9:-1] + "원"
data_text.append(temp)
# print(temp)

curs.execute("select 시가총액 from date_20220203 where 종목코드=005930")
result = curs.fetchone()
if int(str(result)[9:-1]) > 9999:
    div = int(str(result)[9:-1]) // 10000
    res = int(str(result)[9:-1]) % 10000
    temp = "시가총액 : " + str(div) + "조 " + str(res) + "억원"
    data_text.append(temp)
    # print(temp)
else:
    res = int(str(result)[9:-1]) % 10000
    temp = "시가총액 : " + str(res) + "억원"
    data_text.append(temp)
    # print(temp)

curs.execute("select PER from date_20220203 where 종목코드=005930")
result = curs.fetchone()
temp = "PER : " + str(result)[7:-1]
data_text.append(temp)
# print(temp)

curs.execute("select EPS from date_20220203 where 종목코드=005930")
result = curs.fetchone()
temp = "EPS : " + str(result)[7:-1]
data_text.append(temp)
# print(temp)

curs.execute("select PBR from date_20220203 where 종목코드=005930")
result = curs.fetchone()
temp = "PBR : " + str(result)[7:-1]
data_text.append(temp)
# print(temp)

curs.execute("select ROE from date_20220203 where 종목코드=005930")
result = curs.fetchone()
temp = "ROE : " + str(result)[7:-1]
data_text.append(temp)
# print(temp)

curs.execute("select EV from date_20220203 where 종목코드=005930")
result = curs.fetchone()
temp = "EV : " + str(result)[7:-1]
data_text.append(temp)
# print(temp)

curs.execute("select BPS from date_20220203 where 종목코드=005930")
result = curs.fetchone()
temp = "BPS : " + str(result)[7:-1]
data_text.append(temp)
# print(temp)

curs.execute("select 매출액 from date_20220203 where 종목코드=005930")
result = curs.fetchone()
if int(str(result)[8:-1]) > 9999:
    div = int(str(result)[8:-1]) // 10000
    res = int(str(result)[8:-1]) % 10000
    temp = "매출액 : " + str(div) + "조 " + str(res) + "억원"
    # print(temp)
    data_text.append(temp)
else:
    res = int(str(result)[8:-1]) % 10000
    temp = "매출액 : " + str(res) + "억원"
    # print(temp)
    data_text.append(temp)

curs.execute("select 영업이익 from date_20220203 where 종목코드=005930")
result = curs.fetchone()
if int(str(result)[9:-1]) > 9999:
    div = int(str(result)[9:-1]) // 10000
    res = int(str(result)[9:-1]) % 10000
    temp = "영업이익 : " + str(div) + "조 " + str(res) + "억원"
    data_text.append(temp)
    # print(temp)
else:
    res = int(str(result)[9:-1]) % 10000
    temp = "영업이익 : " + str(res) + "억원"
    data_text.append(temp)
    # print(temp)

curs.execute("select 당기순이익 from date_20220203 where 종목코드=005930")
result = curs.fetchone()
if int(str(result)[10:-1]) > 9999:
    div = int(str(result)[10:-1]) // 10000
    res = int(str(result)[10:-1]) % 10000
    temp = "당기순이익 : " + str(div) + "조 " + str(res) + "억원"
    data_text.append(temp)
    # print(temp)
else:
    res = int(str(result)[10:-1]) % 10000
    temp = "당기순이익 : " + str(res) + "억원"
    data_text.append(temp)
    # print(temp)

curs.execute("select 현재가 from date_20220203 where 종목코드=005930")
result = curs.fetchone()
temp = "현재가 : " + str(result)[7:-1] + "원"
data_text.append(temp)
# print(temp)

curs.execute("select Dividends from date_20220203 where 종목코드=005930")
result = curs.fetchone()
temp = "배당금 : " + str(result)[13:-1] + "원"
data_text.append(temp)
# print(temp)

curs.execute("select Dividends_Rate from date_20220203 where 종목코드=005930")
result = curs.fetchone()
temp = "배당률 : " + str(round(float(str(result)[18:-1]), 3) * 100) + "%"
data_text.append(temp)
# print(temp)

for element in data_text:
    print(element)