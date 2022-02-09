import pandas as pd
import pymysql
import os
import price_chart

class stock_data():
    def setdata(self, code_list, name_list, date):
        self.code_list = code_list
        self.name_list = name_list
        self.date = date

    def get_stock_data(self):
        conn = pymysql.connect(host="localhost", user = 'root', password='Axenon!0927', db = 'daily_stock',charset = 'utf8') 
        curs = conn.cursor(pymysql.cursors.DictCursor)

        data = []
        
        for code in self.code_list:
            table = "date_" + self.date
            curs.execute("select 종목코드, 종목명, 연중최고, 연중최저, 시가총액, PER, EPS, PBR, ROE, EV, EPS, 매출액, 영업이익, 당기순이익, 현재가, Dividends, Dividends_Rate from " + table + " where 종목코드=" + code)
            result = curs.fetchall()

            data.append(result)
            print("\n")

        self.data = data
        return self.data

    def make_price_chart(self):
        #폴더 내 파일 삭제
        for file in os.scandir("C:/Users/User/Desktop/Study/Test"):
            os.remove(file.path)
            
        for index, code in enumerate(self.code_list, start= 1):
            inst = price_chart.graph()
            inst.setdata(code, self.date, self.name_list[index-1])
            inst.make_graph()
        print("The stock price chart of the selected stocks has been created.\n\n")