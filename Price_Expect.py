import pandas as pd
import pymysql

class Rt_expect:
    def setdata(self, interest_rate, date, code_list, target_rate):
        self.interest_rate = interest_rate
        self.code_list = code_list
        self.date = date
        self.target_rate = target_rate

    def make_return_expect(self):
        conn = pymysql.connect(host="localhost", user = 'root', password='Axenon!0927', db = 'daily_stock',charset = 'utf8') 
        curs = conn.cursor(pymysql.cursors.DictCursor)

        per_list = []
        name_list = []
        
        for code in self.code_list:
            sql = "select PER from date_" + self.date + " where 종목코드 = " + code
            # print(sql)
            curs.execute(sql)
            res = curs.fetchall()
            # print(res)
            temp = str(res[0])
            per_list.append(temp[8:-1])
        
        for code in self.code_list:
            sql = "select 종목명 from date_" + self.date + " where 종목코드 = " + code
            # print(sql)
            curs.execute(sql)
            res = curs.fetchall()
            # print(res)
            temp = str(res[0])
            name_list.append(temp[8:-1])

        self.per_list = per_list
        self.name_list = name_list

    def print_result(self):
        
        for value in self.return_list:
            print(value)

    def make_return_list(self):
        return_list = []
        profit_list = []
        print("<Expected Return Rate on the selected stocks>\n\n")
        for value, name, code in zip(self.per_list, self.name_list, self.code_list):
            per = float(value)
            if per == 0:
                expect = 0
            else:
                expect = (1 / per - self.interest_rate) * 100
                
            if round(expect,2) >= self.target_rate:
                return_temp = "\033[32m" + name + "\n종목코드 : " + code + "\n기대 수익률 : " + str(round(expect,2)) + "%\n" + "\033[0m"
            else:
                return_temp = "\033[0m" + name + "\n종목코드 : " + code + "\n기대 수익률 : " + str(round(expect,2)) + "%\n"
            return_list.append(return_temp)
            profit_list.append(expect)

        self.return_list = return_list
        self.profit_list = profit_list

    def get_return_list(self):
        return self.return_list
    
    def get_profit_list(self):
        return self.profit_list