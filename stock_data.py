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

            data_text = []

            curs.execute("select 종목코드 from " + table + " where 종목코드=" + code)
            result = curs.fetchone()
            temp = "종목코드 : " + str(result)[10:-2]
            data_text.append(temp)

            curs.execute("select 종목명 from " + table + " where 종목코드=" + code)
            result = curs.fetchone()
            temp = "종목명 : " + str(result)[9:-2]
            data_text.append(temp)

            curs.execute("select 연중최고 from " + table + " where 종목코드=" + code)
            result = curs.fetchone()
            temp = "연중최고 : " + str(result)[9:-1] + "원"
            data_text.append(temp)

            curs.execute("select 시가총액 from " + table + " where 종목코드=" + code)
            result = curs.fetchone()
            if int(str(result)[9:-1]) > 9999:
                div = int(str(result)[9:-1]) // 10000
                res = int(str(result)[9:-1]) % 10000
                temp = "시가총액 : " + str(div) + "조 " + str(res) + "억원"
                data_text.append(temp)
            else:
                res = int(str(result)[9:-1]) % 10000
                temp = "시가총액 : " + str(res) + "억원"
                data_text.append(temp)

            curs.execute("select PER from " + table + " where 종목코드=" + code)
            result = curs.fetchone()
            temp = "PER : " + str(result)[7:-1]
            data_text.append(temp)

            curs.execute("select EPS from " + table + " where 종목코드=" + code)
            result = curs.fetchone()
            temp = "EPS : " + str(result)[7:-1]
            data_text.append(temp)

            curs.execute("select PBR from " + table + " where 종목코드=" + code)
            result = curs.fetchone()
            temp = "PBR : " + str(result)[7:-1]
            data_text.append(temp)

            curs.execute("select ROE from " + table + " where 종목코드=" + code)
            result = curs.fetchone()
            temp = "ROE : " + str(result)[7:-1]
            data_text.append(temp)

            curs.execute("select EV from " + table + " where 종목코드=" + code)
            result = curs.fetchone()
            temp = "EV : " + str(result)[7:-1]
            data_text.append(temp)

            curs.execute("select BPS from " + table + " where 종목코드=" + code)
            result = curs.fetchone()
            temp = "BPS : " + str(result)[7:-1]
            data_text.append(temp)

            curs.execute("select 매출액 from " + table + " where 종목코드=" + code)
            result = curs.fetchone()
            if int(str(result)[8:-1]) > 9999:
                div = int(str(result)[8:-1]) // 10000
                res = int(str(result)[8:-1]) % 10000
                temp = "매출액 : " + str(div) + "조 " + str(res) + "억원"
                data_text.append(temp)
            else:
                res = int(str(result)[8:-1]) % 10000
                temp = "매출액 : " + str(res) + "억원"
                data_text.append(temp)

            curs.execute("select 영업이익 from " + table + " where 종목코드=" + code)
            result = curs.fetchone()
            if int(str(result)[9:-1]) > 9999:
                div = int(str(result)[9:-1]) // 10000
                res = int(str(result)[9:-1]) % 10000
                temp = "영업이익 : " + str(div) + "조 " + str(res) + "억원"
                data_text.append(temp)
            else:
                res = int(str(result)[9:-1]) % 10000
                temp = "영업이익 : " + str(res) + "억원"
                data_text.append(temp)

            curs.execute("select 당기순이익 from " + table + " where 종목코드=" + code)
            result = curs.fetchone()
            if int(str(result)[10:-1]) > 9999:
                div = int(str(result)[10:-1]) // 10000
                res = int(str(result)[10:-1]) % 10000
                temp = "당기순이익 : " + str(div) + "조 " + str(res) + "억원"
                data_text.append(temp)
            else:
                res = int(str(result)[10:-1]) % 10000
                temp = "당기순이익 : " + str(res) + "억원"
                data_text.append(temp)

            curs.execute("select 현재가 from " + table + " where 종목코드=" + code)
            result = curs.fetchone()
            temp = "현재가 : " + str(result)[7:-1] + "원"
            data_text.append(temp)

            curs.execute("select Dividends from " + table + " where 종목코드=" + code)
            result = curs.fetchone()
            temp = "배당금 : " + str(result)[13:-1] + "원"
            data_text.append(temp)

            curs.execute("select Dividends_Rate from " + table + " where 종목코드=" + code)
            result = curs.fetchone()
            temp = "배당률 : " + str(round(float(str(result)[18:-1]), 3) * 100) + "%"
            data_text.append(temp)

            data.append(data_text)
            print("\n")

        conn.commit()
        conn.close()

        self.data = data

        for element in self.data:
            for line in element:
                print(line)
            print("\n\n")   

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
