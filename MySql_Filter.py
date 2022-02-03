from datetime import date
import pymysql

class filter:
    print_sql_part = "종목코드 , 종목명, 연중최고, 연중최저, 시가총액, PER, EPS, ROE, PBR, EV, BPS, 매출액, 영업이익, 당기순이익, 현재가, Theme, Dividends, Dividends_Rate"

    def setdata(self, min, max, detail, count):
        self.min = min
        self.max = max
        self.detail = detail
        self.count = count

    def getTheme(self, theme_exist, theme_code):
        self.theme_exist = theme_exist
        self.theme_code = theme_code
    
    def getNoTheme(self, theme_exist):
        self.theme_exist = theme_exist
        
    def setdate(self, date):
        self.date = date

    def filtersql(self):
        return self.filtersql

    def filtering(self):
        table_name = "date_" + self.date

        #mysql table filtering
        if self.theme_exist == 'Y':
            self.sql = "SELECT %s FROM " + table_name + " WHERE Theme = " + self.theme_code
            if self.detail == 'Y':
                if int(self.min[0]) != 0 or int(self.max[0]) != 0 :
                    self.sql = self.sql + " AND 시가총액 BETWEEN '" + self.min[0] + "' AND '" + self.max[0] + "'"
                elif int(self.min[1]) != 0 or int(self.max[1]) != 0 :
                    self.sql = self.sql + " AND PER BETWEEN '" + self.min[1] + "' AND '" + self.max[1] + "'"
                elif int(self.min[2]) != 0 or int(self.max[2]) != 0 :
                    self.sql = self.sql + " AND EPS BETWEEN '" + self.min[2] + "' AND '" + self.max[2] + "'"
                elif int(self.min[3]) != 0 or int(self.max[3]) != 0 :
                    self.sql = self.sql + " AND ROE BETWEEN '" + self.min[3] + "' AND '" + self.max[3] + "'"
                elif int(self.min[4]) != 0 or int(self.max[4]) != 0 :
                    self.sql = self.sql + " AND PBR BETWEEN '" + self.min[4] + "' AND '" + self.max[4] + "'"
                elif int(self.min[5]) != 0 or int(self.max[5]) != 0 :
                    self.sql = self.sql + " AND EV BETWEEN '" + self.min[5] + "' AND '" + self.max[5] + "'"
                elif int(self.min[6]) != 0 or int(self.max[6]) != 0 :
                    self.sql = self.sql + " AND BPS BETWEEN '" + self.min[6] + "' AND '" + self.max[6] + "'"
                elif int(self.min[7]) != 0 or int(self.max[7]) != 0 :
                    self.sql = self.sql + " AND 매출액 BETWEEN '" + self.min[7] + "' AND '" + self.max[7] + "'"
                elif int(self.min[8]) != 0 or int(self.max[8]) != 0 :
                    self.sql = self.sql + " AND 영업이익 BETWEEN '" + self.min[8] + "' AND '" + self.max[8] + "'"
                elif int(self.min[9]) != 0 or int(self.max[9]) != 0 :
                    self.sql = self.sql + " AND 당기순이익 BETWEEN '" + self.min[9] + "' AND '" + self.max[9] + "'"
                elif int(self.min[10]) != 0 or int(self.max[10]) != 0 :
                    self.sql = self.sql + " AND Dividends BETWEEN '" + self.min[10] + "' AND '" + self.max[10] + "'"
                elif float(self.min[11]) != 0 or float(self.max[11]) != 0 :
                    self.sql = self.sql + " AND Dividends_Rate BETWEEN '" + self.min[11] + "' AND '" + self.max[11] + "'"
            self.filter_sql = self.sql % self.print_sql_part
        else:
            if self.detail == 'Y':
                self.sql = "SELECT %s FROM " + table_name + " WHERE "
                if int(self.min[0]) != 0 or int(self.max[0]) != 0 :
                    self.sql = self.sql + "시가총액 BETWEEN '" + self.min[0] + "' AND '" + self.max[0] + "'"
                elif int(self.min[1]) != 0 or int(self.max[1]) != 0 :
                    self.sql = self.sql + "PER BETWEEN '" + self.min[1] + "' AND '" + self.max[1] + "'"
                elif int(self.min[2]) != 0 or int(self.max[2]) != 0 :
                    self.sql = self.sql + "EPS BETWEEN '" + self.min[2] + "' AND '" + self.max[2] + "'"
                elif int(self.min[3]) != 0 or int(self.max[3]) != 0 :
                    self.sql = self.sql + "ROE BETWEEN '" + self.min[3] + "' AND '" + self.max[3] + "'"
                elif int(self.min[4]) != 0 or int(self.max[4]) != 0 :
                    self.sql = self.sql + "PBR BETWEEN '" + self.min[4] + "' AND '" + self.max[4] + "'"
                elif int(self.min[5]) != 0 or int(self.max[5]) != 0 :
                    self.sql = self.sql + "EV BETWEEN '" + self.min[5] + "' AND '" + self.max[5] + "'"
                elif int(self.min[6]) != 0 or int(self.max[6]) != 0 :
                    self.sql = self.sql + "BPS BETWEEN '" + self.min[6] + "' AND '" + self.max[6] + "'"
                elif int(self.min[7]) != 0 or int(self.max[7]) != 0 :
                    self.sql = self.sql + "매출액 BETWEEN '" + self.min[7] + "' AND '" + self.max[7] + "'"
                elif int(self.min[8]) != 0 or int(self.max[8]) != 0 :
                    self.sql = self.sql + "영업이익 BETWEEN '" + self.min[8] + "' AND '" + self.max[8] + "'"
                elif int(self.min[9]) != 0 or int(self.max[9]) != 0 :
                    self.sql = self.sql + "당기순이익 BETWEEN '" + self.min[9] + "' AND '" + self.max[9] + "'"
                elif int(self.min[10]) != 0 or int(self.max[10]) != 0 :
                    self.sql = self.sql + "Dividends BETWEEN '" + self.min[10] + "' AND '" + self.max[10] + "'"
                elif float(self.min[11]) != 0 or float(self.max[11]) != 0 :
                    self.sql = self.sql + "Dividends_Rate BETWEEN '" + self.min[11] + "' AND '" + self.max[11] + "'"
            self.filter_sql = self.sql % self.print_sql_part


    def table_show(self):
        conn = pymysql.connect(host="localhost", user = 'root', password='Axenon!0927', db = 'daily_stock',charset = 'utf8') 
        curs = conn.cursor(pymysql.cursors.DictCursor)

        print("----------<Table List in Daily_Stock DB>----------\n")
        curs.execute("show tables")
        res = curs.fetchall()
        print(res)
        print("\n\n\n")

        conn.commit()
        conn.close()

    def filtering_show(self):
        conn = pymysql.connect(host="localhost", user = 'root', password='Axenon!0927', db = 'daily_stock',charset = 'utf8') 
        curs = conn.cursor(pymysql.cursors.DictCursor)
        #정렬 결과 보기 while loop
        sort_sql = ""
        while True:
            print("\n")
            temp_sql = self.filter_sql + sort_sql
            curs.execute(temp_sql)
            rows = curs.fetchall()
            # 정렬 한 결과 프린트
            temp = self.count
            for index, value in enumerate(rows, start = 1):
                self.count = int(self.count) -1
                if self.count < 0 :
                    break;
                print(index, value)
                print("\n")
            self.count = temp
            # 정렬 방식(시가총액, 매출액, 영업이익, 배당금, 배당수익률)
            sort_check = input("Would you like to sort out the data? (Y for yes) : ")
            if sort_check == 'Y':
                print("\n1. 시가총액\t2. 매출액\t3. 영업이익\t4. 배당금\t5. 배당수익률\n")
                sorting_type = input("By what criteria would you like to sort it out? (1 to 5) : ")
                if sorting_type == '1':
                    sort_sql = "ORDER BY 시가총액 DESC"
                elif sorting_type == '2':
                    sort_sql = "ORDER BY 매출액 DESC"
                elif sorting_type == '3':
                    sort_sql = "ORDER BY 영업이익 DESC"
                elif sorting_type == '4':
                    sort_sql = "ORDER BY Dividends DESC"        
                elif sorting_type == '5':
                    sort_sql = "ORDER BY Dividends_Rate DESC"
            else:
                analyze = input("\nDo you want to start analyzing these stocks? (Y for Yes) : ")
                if analyze == "Y":
                    print("\nAnalyzing these stocks...\n")
                    break;
                else:
                    continue;
                

        # sql에서 종목코드만 추출
        code_list = []
        name_list = []
        filter_sql = self.sql % "종목코드, 종목명" + sort_sql 
        # print(filter_sql)
        curs.execute(filter_sql)
        results = curs.fetchall()
        temp = self.count
        for index, value in enumerate(results, start = 1):
            self.count = int(self.count) -1
            if self.count < 0 :
                break;
            code_temp = str(value)
            code_list.append(code_temp[10:16])
            name_list.append(code_temp[27:-2])
            print(index, value)
        self.count = temp
        # code list, name 추출 완료
        self.code_list = code_list
        self.name_list = name_list
        # DB 닫기
        conn.commit()
        conn.close()
    
    def code_list(self):
        return self.code_list
    
    def name_list(self):
        return self.name_list











# #mysql 연결
# conn = pymysql.connect(host="localhost", user = 'root', password='Axenon!0927', db = 'daily_stock',charset = 'utf8') 
# curs = conn.cursor(pymysql.cursors.DictCursor)

# #DB안에 있는 테이블 목록 보여주기
# #날짜 입력해서 그날 기준 가져오기

# table_name = "date_" + today

# #mysql table filtering
# if theme_exist == 'Y':
#     sql = "SELECT %s FROM " + table_name + " WHERE Theme = " + theme_code
#     if det.check() == 'Y':
#         if int(self.min[0]) != 0 or int(self.max[0]) != 0 :
#             sql = sql + " AND 시가총액 BETWEEN '" + self.min[0] + "' AND '" + self.max[0] + "'"
#         elif int(self.min[1]) != 0 or int(self.max[1]) != 0 :
#             sql = sql + " AND PER BETWEEN '" + self.min[1] + "' AND '" + self.max[1] + "'"
#         elif int(self.min[2]) != 0 or int(self.max[2]) != 0 :
#             sql = sql + " AND EPS BETWEEN '" + self.min[2] + "' AND '" + self.max[2] + "'"
#         elif int(self.min[3]) != 0 or int(self.max[3]) != 0 :
#             sql = sql + " AND ROE BETWEEN '" + self.min[3] + "' AND '" + self.max[3] + "'"
#         elif int(self.min[4]) != 0 or int(self.max[4]) != 0 :
#             sql = sql + " AND PBR BETWEEN '" + self.min[4] + "' AND '" + self.max[4] + "'"
#         elif int(self.min[5]) != 0 or int(self.max[5]) != 0 :
#             sql = sql + " AND EV BETWEEN '" + self.min[5] + "' AND '" + self.max[5] + "'"
#         elif int(self.min[6]) != 0 or int(self.max[6]) != 0 :
#             sql = sql + " AND BPS BETWEEN '" + self.min[6] + "' AND '" + self.max[6] + "'"
#         elif int(self.min[7]) != 0 or int(self.max[7]) != 0 :
#             sql = sql + " AND 매출액 BETWEEN '" + self.min[7] + "' AND '" + self.max[7] + "'"
#         elif int(self.min[8]) != 0 or int(self.max[8]) != 0 :
#             sql = sql + " AND 영업이익 BETWEEN '" + self.min[8] + "' AND '" + self.max[8] + "'"
#         elif int(self.min[9]) != 0 or int(self.max[9]) != 0 :
#             sql = sql + " AND 당기순이익 BETWEEN '" + self.min[9] + "' AND '" + self.max[9] + "'"
#         elif int(self.min[10]) != 0 or int(self.max[10]) != 0 :
#             sql = sql + " AND Dividends BETWEEN '" + self.min[10] + "' AND '" + self.max[10] + "'"
#         elif float(self.min[11]) != 0 or float(self.max[11]) != 0 :
#             sql = sql + " AND Dividends_Rate BETWEEN '" + self.min[11] + "' AND '" + self.max[11] + "'"
#     filter_sql = sql % print_sql_part
# else:
#     if det.check() == 'Y':
#         sql = "SELECT %s FROM " + table_name + " WHERE "
#         if int(self.min[0]) != 0 or int(self.max[0]) != 0 :
#             sql = sql + "시가총액 BETWEEN '" + self.min[0] + "' AND '" + self.max[0] + "'"
#         elif int(self.min[1]) != 0 or int(self.max[1]) != 0 :
#             sql = sql + "PER BETWEEN '" + self.min[1] + "' AND '" + self.max[1] + "'"
#         elif int(self.min[2]) != 0 or int(self.max[2]) != 0 :
#             sql = sql + "EPS BETWEEN '" + self.min[2] + "' AND '" + self.max[2] + "'"
#         elif int(self.min[3]) != 0 or int(self.max[3]) != 0 :
#             sql = sql + "ROE BETWEEN '" + self.min[3] + "' AND '" + self.max[3] + "'"
#         elif int(self.min[4]) != 0 or int(self.max[4]) != 0 :
#             sql = sql + "PBR BETWEEN '" + self.min[4] + "' AND '" + self.max[4] + "'"
#         elif int(self.min[5]) != 0 or int(self.max[5]) != 0 :
#             sql = sql + "EV BETWEEN '" + self.min[5] + "' AND '" + self.max[5] + "'"
#         elif int(self.min[6]) != 0 or int(self.max[6]) != 0 :
#             sql = sql + "BPS BETWEEN '" + self.min[6] + "' AND '" + self.max[6] + "'"
#         elif int(self.min[7]) != 0 or int(self.max[7]) != 0 :
#             sql = sql + "매출액 BETWEEN '" + self.min[7] + "' AND '" + self.max[7] + "'"
#         elif int(self.min[8]) != 0 or int(self.max[8]) != 0 :
#             sql = sql + "영업이익 BETWEEN '" + self.min[8] + "' AND '" + self.max[8] + "'"
#         elif int(self.min[9]) != 0 or int(self.max[9]) != 0 :
#             sql = sql + "당기순이익 BETWEEN '" + self.min[9] + "' AND '" + self.max[9] + "'"
#         elif int(self.min[10]) != 0 or int(self.max[10]) != 0 :
#             sql = sql + "Dividends BETWEEN '" + self.min[10] + "' AND '" + self.max[10] + "'"
#         elif float(self.min[11]) != 0 or float(self.max[11]) != 0 :
#             sql = sql + "Dividends_Rate BETWEEN '" + self.min[11] + "' AND '" + self.max[11] + "'"
#     filter_sql = sql % print_sql_part

# print(filter_sql)

# #정렬 결과 보기 while loop
# sort_sql = ""
# while True:
#     print("\n")
#     temp_sql = filter_sql + sort_sql
#     curs.execute(temp_sql)
#     rows = curs.fetchall()
#     # 정렬 한 결과 프린트
#     temp = self.count
#     for index, value in enumerate(rows, start = 1):
#         self.count = int(self.count) -1
#         if self.count < 0 :
#             break;
#         print(index, value)
#         print("\n")
#     self.count = temp
#     # 정렬 방식(시가총액, 매출액, 영업이익, 배당금, 배당수익률)
#     sort_check = input("Would you like to sort out the data? (Y for yes) : ")
#     if sort_check == 'Y':
#         print("\n1. 시가총액\t2. 매출액\t3. 영업이익\t4. 배당금\t5. 배당수익률\n")
#         sorting_type = input("By what criteria would you like to sort it out? (1 to 5) : ")
#         if sorting_type == '1':
#             sort_sql = "ORDER BY 시가총액 DESC"
#         elif sorting_type == '2':
#             sort_sql = "ORDER BY 매출액 DESC"
#         elif sorting_type == '3':
#             sort_sql = "ORDER BY 영업이익 DESC"
#         elif sorting_type == '4':
#             sort_sql = "ORDER BY Dividends DESC"        
#         elif sorting_type == '5':
#             sort_sql = "ORDER BY Dividends_Rate DESC"
#     else:
#         analyze = input("\nDo you want to start analyzing these stocks? (Y for Yes) : ")
#         if analyze == "Y":
#             print("\nAnalyzing these stocks...\n")
#             break;
#         else:
#             continue;
        

# # sql에서 종목코드만 추출
# code_list = []
# name_list = []
# filter_sql = sql % "종목코드, 종목명" + sort_sql 
# # print(filter_sql)
# curs.execute(filter_sql)
# results = curs.fetchall()
# temp = self.count
# for index, value in enumerate(results, start = 1):
#     self.count = int(self.count) -1
#     if self.count < 0 :
#         break;
#     code_temp = str(value)
#     code_list.append(code_temp[10:16])
#     name_list.append(code_temp[27:-2])
#     print(index, value)
# self.count = temp
# # code list, name 추출 완료

# # DB 닫기
# conn.commit()
# conn.close()