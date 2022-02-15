import pandas as pd
import pymysql
import datetime
import os
import shutil
import time
from pykiwoom.kiwoom import *

theme_code_list = ['141', '140','571','570','830','501','562','561','560','572','600','500','458','452','353','250','170','202','319','201','200','471','470','312','270','245','160','210','211','480','610','316','213','456','517','281','280','130','360','363','361','362','550','551','557','556',
'555','552','554','553','212','313','290','453','420','421','611','171','315','530','459','310','364','810','515','516','203','318','370','286','820','154','261','800','214','232','230','231','110','111','314','311','400','351','352','350','256','255','242','241','240','243','215','262',
'454','455','450','317','180','181','223','220','222','221','300','910','430','410','260','284','282','283','285','451','920','900','457','244','153','520','103','102','101','100','481','850','121','172','152','151','150','291','120','330','840','511','518','510','514','513','512','173']

class dataload:
    now = datetime.datetime.now()
    today = now.strftime("%Y%m%d")

    #데이터 로드에 필요한 기본 값 세팅
    def setdata(self):
        #TEST 중인지 물어보기
        self.test = input("Is it test download? (Y for Yes) : ")

        if self.test == "Y":
            self.file_path = "C:/CRAproject/test/"
        else:
            self.file_path = "C:/CRAproject/"
    def settoday(self, date):
        self.today = date

    #데이터 다운로드 함수
    def download(self):
        #키움증권 로그인
        kiwoom = Kiwoom()
        kiwoom.CommConnect()

        kospi = kiwoom.GetCodeListByMarket('0')
        kosdaq = kiwoom.GetCodeListByMarket('10')
        codes = kospi + kosdaq

        print("\nYou have been logged in to the Kiwoom server.")

        #어떤 데이터 불러올것인지 조사
        print("\n1. Today(%s)'s Entire Stock Information 2. Entire Stock Price Information for 600 days" % self.today)
        which_data = input("\nWhat data do you want to get? ( 1 or 2 ) : ")

        
        if which_data == "1":
            #경고메세지
            load_check = input("\nCaution) This takes about three hours. Will you still do it? ( Y for Yes) : ")
            if load_check == "Y":
                today = self.today
                #폴더 만들기
                folder_name = "entire_%s" % today
                print(self.file_path + folder_name)
                
                #만약에 폴더가 이미 있으면
                #덮어쓰기 할건지 물어보보고 폴더 생성
                if (os.path.isdir(self.file_path + folder_name) == False):
                    os.mkdir(self.file_path + folder_name)
                    os.chdir(self.file_path + folder_name)
                else:
                    list = os.listdir(self.file_path + folder_name)
                    count = len(list)
                    print("folder has %s files\n" % count)
                    rmdir_check = input("That folder already exists. Do you want to delete the folder and create it again? ( Y for Yes) : ")
                    if rmdir_check == "Y":
                        shutil.rmtree(self.file_path + folder_name)
                        os.mkdir(self.file_path + folder_name)
                        os.chdir(self.file_path + folder_name)


                #해당 폴더에 csv파일 생성
                for i, code in enumerate(codes):
                    print(f"{i}/{len(codes)} {code}")
                    df = kiwoom.block_request("opt10001", 종목코드=code, output="주식기본정보", next=0)
                    out_name = f"{code}.csv"
                    df.to_csv(out_name)
                    time.sleep(3.6)
                    #test code
                    if self.test == "Y":
                        if i == 7:
                            break;
                        
                print("\nData Download End")

                #끝나면 DB(daily_stock)로 저장
                #mysql 연결
                conn = pymysql.connect(host="localhost", user = 'root', password='Axenon!0927', db = 'daily_stock', charset = 'utf8') 
                curs = conn.cursor(pymysql.cursors.DictCursor)

                dir_path = self.file_path + folder_name

                #만약에 이미 테이블이 있을 경우에 어떻게 대처?
                curs.execute("SELECT COUNT(*) FROM Information_schema.tables WHERE table_schema = 'daily_stock' AND table_name = 'date_%s'" % today)
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
                                tu = ( index, str(row.종목코드), row.종목명, abs(row.연중최고), abs(row.연중최저), row.시가총액, row.PER, row.EPS, row.ROE, row.PBR, row.EV, row.BPS, row.매출액, row.영업이익, row.당기순이익, abs(row.시가), abs(row.고가), abs(row.저가), abs(row.현재가), row.전일대비, row.등락율, row.거래량) 
                                curs.execute("INSERT IGNORE INTO date_" + today + "(count, 종목코드, 종목명, 연중최고, 연중최저, 시가총액, PER, EPS, ROE, PBR, EV, BPS, 매출액, 영업이익, 당기순이익, 시가, 고가, 저가, 현재가, 전일대비, 등락율, 거래량) values(%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s, %s)", tu)
                print("\nDB Upload Completed.")

                #테마 넣기
                for theme in theme_code_list:
                    items = kiwoom.GetThemeGroupCode(theme)
                    for item in items:
                        tu = (int(theme), item)
                        sql = "UPDATE date_" + today + " SET Theme = " + theme + " WHERE 종목코드 = '" + item + "'"
                        curs.execute(sql)
                print("\nTheme info added.")

                #배당금 정보 넣기
                #배당수익률 정보 넣기
                dividends = pd.read_csv("C:\CRAproject/Dividends.csv", encoding="utf8", sep=",", dtype={'종목코드' : str ,'주당배당금' : str})
                dividends = dividends.fillna(0)
                for index, row in dividends.iterrows():
                    tu = (row.주당배당금,row.종목코드)
                    sql = "UPDATE date_" + today + " SET Dividends = %s WHERE 종목코드 = '%s'" % tu
                    curs.execute(sql)
                    sql = "UPDATE date_" + today + " SET Dividends_Rate = %s/현재가 WHERE 종목코드 ='%s'" % tu
                    curs.execute(sql)
                print("\nDividends info added.")
                conn.commit()
                conn.close()

        elif which_data == "2":
            load_check = input("\nCaution) This takes about three hours. Will you still do it? ( Y for Yes) : ")
            if load_check == "Y":
                today = self.today
                #폴더 만들기
                folder_name = "today_%s" % today
                print(self.file_path + folder_name)
                
                #만약에 폴더가 이미 있으면
                #덮어쓰기 할건지 물어보보고 폴더 생성
                if (os.path.isdir(self.file_path + folder_name) == False):
                    os.mkdir(self.file_path + folder_name)
                    os.chdir(self.file_path + folder_name)
                else:
                    list = os.listdir(self.file_path + folder_name)
                    count = len(list)
                    print("folder has %s files\n" % count)
                    rmdir_check = input("That folder already exists. Do you want to delete the folder and create it again? ( Y for Yes) : ")
                    if rmdir_check == "Y":
                        shutil.rmtree(self.file_path + folder_name)
                        os.mkdir(self.file_path + folder_name)
                        os.chdir(self.file_path + folder_name)


                #해당 폴더에 csv파일 생성
                for i, code in enumerate(codes):
                    print(f"{i}/{len(codes)} {code}")
                    df = kiwoom.block_request("opt10081", 종목코드=code, 기준일자=today, 수정주가구분=1, output="주식일봉차트조회", next=0)
                    out_name = f"{code}.csv"
                    df.to_csv(out_name)
                    time.sleep(3.6)
                    #test code
                    if self.test == "Y":
                        if i == 7:
                            break;
                print("\nData Download End")


                #끝나면 DB(stock_price)로 저장
                #mysql 연결
                conn = pymysql.connect(host="localhost", user = 'root', password='Axenon!0927', db = 'stock_price',charset = 'utf8') 
                curs = conn.cursor(pymysql.cursors.DictCursor)
                dir_path = self.file_path + folder_name

                #DB저장 과정
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
                                tu = (row.일자, abs(row.현재가), row.거래량, row.거래대금, abs(row.시가), abs(row.고가), abs(row.저가))
                                curs.execute("INSERT IGNORE INTO " + today + "_" + file_name + "(일자, 현재가, 거래량, 거래대금, 시가, 고가, 저가) values (%s,%s,%s,%s,%s,%s,%s)", tu)
                print("\nDB Upload Completed.")
                conn.commit()
                conn.close()
        




