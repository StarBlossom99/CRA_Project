#-*-coding: utf-8-*-
import pandas as pd
import pymysql 
import os
import datetime
import time
from pykiwoom.kiwoom import *

theme_code_list = ['141', '140','571','570','830','501','562','561','560','572','600','500','458','452','353','250','170','202','319','201','200','471','470','312','270','245','160','210','211','480','610','316','213','456','517','281','280','130','360','363','361','362','550','551','557','556',
'555','552','554','553','212','313','290','453','420','421','611','171','315','530','459','310','364','810','515','516','203','318','370','286','820','154','261','800','214','232','230','231','110','111','314','311','400','351','352','350','256','255','242','241','240','243','215','262',
'454','455','450','317','180','181','223','220','222','221','300','910','430','410','260','284','282','283','285','451','920','900','457','244','153','520','103','102','101','100','481','850','121','172','152','151','150','291','120','330','840','511','518','510','514','513','512','173']
det_a = [0,0,0,0,0,0,0,0,0,0,0,0]
det_b = [0,0,0,0,0,0,0,0,0,0,0,0]
print_sql_part = "종목코드 , 종목명, 연중최고, 연중최저, 시가총액, PER, EPS, ROE, PBR, EV, BPS, 매출액, 영업이익, 당기순이익, 현재가, Theme, Dividends, Dividends_Rate"


# 프로그램 시작
print("=" * 70)
print("Welcome to StocKid Program")
print("=" * 70)
#데이터 새로 불러올것인지(login 할지 안할지 여부)
data_load_check = input("Do you want to load new data? (Y for Yes) : ")
if data_load_check == 'Y':
    now = datetime.datetime.now()
    today = now.strftime("%Y%m%d")
    #날짜 이용, 데이터 불러올것인지 조사
    data_load = input("\nDo you want to load the data of %s? (Y for Yes) : " % today)
    #불러오기
    if data_load == "Y":
        #키움 로그인
        kiwoom = Kiwoom()
        kiwoom.CommConnect()

        kospi = kiwoom.GetCodeListByMarket('0')
        kosdaq = kiwoom.GetCodeListByMarket('10')
        codes = kospi + kosdaq
        print("\nYou have been logged in to the Kiwoom server.")
        #어떤 데이터 불러올것인지 조사
        print("\n1. Today(%s)'s Entire Stock Information 2. Entire Stock Price Information for 600 days" % today)
        which_data = input("\nWhat data do you want to get? ( 1 or 2 ) : ")
        #오늘 날짜의 전체 주식 정보
        if which_data == "1":
            #경고 메세지 (3시간 걸림)
            load_check = input("\nCaution) This takes about three hours. Will you still do it? ( Y for Yes) : ")
            #수행
            if load_check == "Y":
                #폴더 만들기
                os.mkdir("C:\CRAproject/entire_%s" % today)
                os.chdir("C:\CRAproject/entire_%s" % today)
                #해당 폴더에 csv파일 생성
                for i, code in enumerate(codes):
                    print(f"{i}/{len(codes)} {code}")
                    df = kiwoom.block_request("opt10001", 종목코드=code, output="주식기본정보", next=0)
                    out_name = f"{code}.csv"
                    df.to_csv(out_name)
                    time.sleep(3.6)
                    if i == 10:
                        break;
                print("\nData Download End")

                #끝나면 DB(daily_stock)로 저장
                #mysql 연결
                conn = pymysql.connect(host="localhost", user = 'root', password='Axenon!0927', db = 'daily_stock', charset = 'utf8') 
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
            #경고 메세지 (3시간 걸림)
            load_check = input("\nCaution) This takes about three hours. Will you still do it? ( Y for Yes) : ")
            #수행
            if load_check == "Y":
                #폴더 만들기
                os.mkdir("C:\CRAproject/today_%s" % today)
                os.chdir("C:\CRAproject/today_%s" % today)
                #해당 폴더에 csv파일 생성
                for i, code in enumerate(codes):
                    print(f"{i}/{len(codes)} {code}")
                    df = kiwoom.block_request("opt10081", 종목코드=code, 기준일자=today, 수정주가구분=1, output="주식일봉차트조회", next=0)
                    out_name = f"{code}.csv"
                    df.to_csv(out_name)
                    time.sleep(3.6)
                    if i == 10:
                        break;
                print("\nData Download End")
                #끝나면 DB(stock_price)로 저장
                #mysql 연결
                conn = pymysql.connect(host="localhost", user = 'root', password='Axenon!0927', db = 'stock_price',charset = 'utf8') 
                curs = conn.cursor(pymysql.cursors.DictCursor)
                dir_path = "C:\CRAproject/today_%s" % today

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
                                tu = (row.일자, row.현재가, row.거래량, row.거래대금, row.시가, row.고가, row.저가)
                                curs.execute("INSERT IGNORE INTO " + today + "_" + file_name + "(일자, 현재가, 거래량, 거래대금, 시가, 고가, 저가) values (%s,%s,%s,%s,%s,%s,%s)", tu)
                print("\nDB Upload Completed.")
                conn.commit()
                conn.close()
                    
#DB table csv 파일로 빼는 part

while True:
    # 투자 기간 입력
    period = input("Please enter the period(month) you want to invest in : ")
    # print(period)

    # 목표 수익률 입력
    target_rate = input("\nPlease enter your target rate(%) of return : ")
    # print(target_rate)

    theme_exist = input("\nIs there any field you want to invest in ? (Y for yes , N for anything else) : ")
    if theme_exist == 'Y':
        while True :
            #테마 코드 리스트 출력
            print("="*200)
            print("%-18s\t%s\t%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-25s\t%s\n\n%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-17s\t%s\n\n%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-25s\t%s\n\n%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-25s\t%s\n\n%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-18s\t%s\t%-25s\t%s\n\n%-17s\t%s\t%-18s\t%s\t%-25s\t%s\t%-25s\t%s\t%-17s\t%s\n\n%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-17s\t%s\n\n%-17s\t%s\t%-17s\t%s\t%-17s\t%s\t%-17s\t%s\t%-17s\t%s\n\n%-17s\t%s\t%-17s\t%s\t%-25s\t%s\t%-24s\t%s\t%-17s\t%s\n\n%-17s\t%s\t%-17s\t%s\t%-25s\t%s\t%-17s\t%s\t%-17s\t%s\n\n%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-25s\t%s\n\n%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-25s\t%s\n\n%-17s\t%s\t%-17s\t%s\t%-25s\t%s\t%-25s\t%s\t%-17s\t%s\n\n%-17s\t%s\t%-25s\t%s\t%-25s\t%s\t%-17s\t%s\t%-25s\t%s\n\n%-25s\t%s\t%-17s\t%s\t%-25s\t%s\t%-17s\t%s\t%-25s\t%s\n\n%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-17s\t%s\n\n%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-25s\t%s\n\n%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-17s\t%s\t%-17s\t%s\n\n%-17s\t%s\t%-17s\t%s\t%-25s\t%s\t%-25s\t%s\t%-25s\t%s\n\n%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-25s\t%s\n\n%-25s\t%s\t%-25s\t%s\t%-17s\t%s\t%-17s\t%s\t%-25s\t%s\n\n%-17s\t%s\t%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-17s\t%s\n\n%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-17s\t%s\t%-17s\t%s\n\n%-17s\t%s\t%-17s\t%s\t%-25s\t%s\t%-25s\t%s\t%-25s\t%s\n\n%-17s\t%s\t%-17s\t%s\t%-17s\t%s\t%-17s\t%s\t%-25s\t%s\n\n%-25s\t%s\t%-17s\t%s\t%-25s\t%s\t%-25s\t%s\t%-25s\t%s\n\n%-25s\t%s\t%-25s\t%s\t%-17s\t%s\t%-25s\t%s\t%-25s\t%s\n\n%-25s\t%s\t%-17s\t%s\t%-17s\t%s\t%-25s\t%s\t%-17s\t%s\n\n%-17s\t%s\t%-25s\t%s" % ('2차전지_소재(양극화물질등)','141','2차전지_완제품','140','AMOLED_소재','571','AMOLED_장비','570','Cheap-Chic_저가실용품','830','FPCB(연성회로기판)','501','LCD_부품                   ','562','LCD_소재','561','LCD_장비','560','LED','        572','LPG(액화석유가스)','600','PCB(인쇄회로기판)','500','SI(시스템통합)','458','SNS(Social Network Service)','452','U-헬스케어','353','가구','250','강관','170','거푸집','202','건강식품','319','건설_국내주택','201','건설_해외건설','200','게임_모바일','471','게임_온라인','470','곡물가공품_설탕/밀가루/유지','312','교육','270','그린카_하이브리드카/전기차','245','금형/몰드베이스','160','기계_건설기계','210','기계_공작기계','211','네트워크/광통신','480','도시가스','610','라면','316','로봇_지능형','213','모바일솔루션','456','무선충전기관련주','517','미디어_디지털방송전환','281','미디어_방송광고','280','바이오_디젤/에탄올','130','바이오_바이오시밀러/베터','360','바이오_유전체분석','363','바이오_줄기세포치료제','361','바이오_진단/백신','362','반도체_생산','550','반도체_설계(fabless)','551','반도체_시스템반도체','557','반도체_전공정소재','556','반도체_전공정장비','555','반도체_후공정','552','반도체_후공정소재','554','반도체_후공정장비','553','방위산업','212','배합사료','313','백화점','290','보안_인터넷','453','보험_생명보험','420','보험_손해보험','421','부탄가스','611','비철금속주','171','빙과','315','셋톱박스','530','소프트웨어_자동차용','459','수산물/수산가공품','310','슈퍼박테리아','364','스마트 그리드','810','스마트폰_삼성전자관련주','515','스마트폰_애플 관련주','516','시멘트','203','식자재유통','318','신약개발/기술수출','370','에니메이션','286','엔젤산업','820','엔지니어링 플라스틱','154','여행','261','온실가스배출저감','800','우주항공','214','운송_육상운송','232','운송_항공','230','운송_해운','231','원자력_기자재','110','원자력_설계시공','111','유가공','314','육계','311','은행','400','의료기기','351','의료기기_안과','352','의료기기_치아','350','의복_OEM','256','의복_아웃도어','255','자동차_블랙박스관련주','242','자동차_전장화 수혜','241','자동차_차량경량화 수혜','240','자동차_차량용 반도체','243','자원개발 E&P','215','전기자전거','262','전자결제','454','전자결제_B2B','455','전자책_e-book','450','제과스낵','317','제지_골판지','180','제지_기타','181','조선_Eco선','223','조선_LNG보냉재','220','조선_해양플랜트','222','조선_해양플랜트기자재','221','주류','300','중국_내수소비 확대','910','증권','430','창투','410','카지노','260','컨텐츠_메니지먼트','284','컨텐츠_영상','282','컨텐츠_음원','283','컨텐츠_한류','285','컴퓨터전화통합(CTI)','451','코스닥_라이징스타','920','코스닥_히든챔피언','900','클라우드 컴퓨팅','457','타이어','244','탄소섬유','153','태블릿 PC','520','태양광_발전/설치/운영','103','태양광_부품/소재/장비','102','태양광_잉곳/웨이퍼/셀/모듈','101','태양광_폴리실리콘','100','통신장비','481','폐기물처리','850','풍력_단조/기자재','121','합금철','172','합성고무','152','합성섬유_원료','151','합성수지','150','홈쇼핑','291','화력_발전기자재','120','화장품','330','환경산업','840','휴대폰_RF부품','511','휴대폰_베트남현지법인','518','휴대폰_수동부품','510','휴대폰_카메라','514','휴대폰_케이스/기구물','513','휴대폰_터치스크린','512','희소금속','173'))
            print("="*200)
            #테마 입력
            theme_code = input("\nLook at the theme code list and enter the code for the field you want to invest in. : ")
            if str(theme_code) in theme_code_list:
                break;
            else:
                print("\ntheme code %s doesn't exist in code list, please try again" % theme_code)
                continue;

    # 추천 받고 싶은 종목의 개수를 입력
    while True:
        count = input("\nHow many stocks would you like to recommend? (1 to 15) : ")
        if int(count) >= 1 and int(count) <= 15:
            break;
        else:
            print("\nplease input valid input (1 to 15)")
            continue;
    
    # 세부 필터를 사용할 것인지 묻기
    detail_filter = input("\nDo you want to use detail filter? (Y for yes , N for anything else) : ")
    if detail_filter == 'Y':
        print("\nDetailed filter is used.\n")
        #세부 필터 입력 받기
        while True:
            #필터 코드 입력 받기
            detail_code = 0
            while True:
                print("%-15s\t%-15s\t%-15s\t%-15s\n%-15s\t%-15s\t%-15s\t%-15s\n%-15s\t%-15s\t%-15s\t%-15s\n" % ("1. Market Cap(시가 총액)", "2. PER(주가수익률)", "3. EPS(주당 순이익)", "4. ROE(자기자본 이익률)" , "5, PBR(주가 순 자산비율)", "6. EV(기업 가치)", "7. BPS(주당 순 자산가치)", "8. Sales(매출액)", "9. Operating Profit(영업 이익)", "10. Net Profit(당기 순이익)", "11. Dividends(배당금)", "12. Dividend Yield(배당 수익률)"))
                detail_code = input("\nPlease enter the number of the filter you want to use (1 to 12) : ")
                # 필터 코드 검사
                if int(detail_code) >= 1 and int(detail_code) <= 12:
                    break;
                else:
                    print("please input valid detail code (1 to 12)")
                    continue;

            detail_code = int(detail_code)       
            # 필터 코드 switch loop
            if detail_code == 1:
                while True:
                    print("\nPlease enter the Market Cap(시가 총액) range. (unit : 100 million won)")
                    det_a[0] = input("\nPlease enter the minimum value : ")
                    det_b[0] = input("\nPlease enter the maximum value : ")
                    if int(det_a[0]) >= int(det_b[0]):
                        print("maximun value is less than minimum value, please enter valid input")
                        continue;
                    else:
                        break;
            elif detail_code == 2:
                while True:
                    print("\nPlease enter the PER(주가수익률) range.")
                    det_a[1] = input("\nPlease enter the minimum value : ")
                    det_b[1] = input("\nPlease enter the maximum value : ")
                    if int(det_a[1]) >= int(det_b[1]):
                        print("maximun value is less than minimum value, please enter valid input")
                        continue;
                    else:
                        break;
            elif detail_code == 3:
                while True:
                    print("\nPlease enter the EPS(주당 순이익) range. (unit : won)")
                    det_a[2] = input("\nPlease enter the minimum value : ")
                    det_b[2] = input("\nPlease enter the maximum value : ")
                    if int(det_a[2]) >= int(det_b[2]):
                        print("maximun value is less than minimum value, please enter valid input")
                        continue;
                    else:
                        break;
            elif detail_code == 4:
                while True:
                    print("\nPlease enter the ROE(자기자본 이익률) range. ")
                    det_a[3] = input("\nPlease enter the minimum value : ")
                    det_b[3] = input("\nPlease enter the maximum value : ")
                    if int(det_a[3]) >= int(det_b[3]):
                        print("maximun value is less than minimum value, please enter valid input")
                        continue;
                    else:
                        break;
            elif detail_code == 5:
                while True:
                    print("\nPlease enter the PBR(주가 순 자산비율) range.")
                    det_a[4] = input("\nPlease enter the minimum value : ")
                    det_b[4] = input("\nPlease enter the maximum value : ")
                    if int(det_a[0]) >= int(det_b[4]):
                        print("maximun value is less than minimum value, please enter valid input")
                        continue;
                    else:
                        break;
            elif detail_code == 6:
                while True:
                    print("\nPlease enter the EV(기업 가치) range.")
                    det_a[5] = input("\nPlease enter the minimum value : ")
                    det_b[5] = input("\nPlease enter the maximum value : ")
                    if int(det_a[5]) >= int(det_b[5]):
                        print("maximun value is less than minimum value, please enter valid input")
                        continue;
                    else:
                        break;
            elif detail_code == 7:
                while True:
                    print("\nPlease enter the BPS(주당 순 자산가치) range.")
                    det_a[6] = input("\nPlease enter the minimum value : ")
                    det_b[6] = input("\nPlease enter the maximum value : ")
                    if int(det_a[6]) >= int(det_b[6]):
                        print("maximun value is less than minimum value, please enter valid input")
                        continue;
                    else:
                        break;
            elif detail_code == 8:
                while True:
                    print("\nPlease enter the Sales(매출액) range. (unit : 100 million won)")
                    det_a[7] = input("\nPlease enter the minimum value : ")
                    det_b[7] = input("\nPlease enter the maximum value : ")
                    if int(det_a[7]) >= int(det_b[7]):
                        print("maximun value is less than minimum value, please enter valid input")
                        continue;
                    else:
                        break;
            elif detail_code == 9:
                while True:
                    print("\nPlease enter the Operating Profit(영업 이익) range. (unit : 100 million won)")
                    det_a[8] = input("\nPlease enter the minimum value : ")
                    det_b[8] = input("\nPlease enter the maximum value : ")
                    if int(det_a[8]) >= int(det_b[8]):
                        print("maximun value is less than minimum value, please enter valid input")
                        continue;
                    else:
                        break;
            elif detail_code == 10:
                while True:
                    print("\nPlease enter Net Profit(당기 순이익) range. (unit : 100 million won)")
                    det_a[9] = input("\nPlease enter the minimum value : ")
                    det_b[9] = input("\nPlease enter the maximum value : ")
                    if int(det_a[9]) >= int(det_b[9]):
                        print("maximun value is less than minimum value, please enter valid input")
                        continue;
                    else:
                        break;
            elif detail_code == 11:
                while True:
                    print("\nPlease enter the Dividends(배당금) range. (unit : won)")
                    det_a[10] = input("\nPlease enter the minimum value : ")
                    det_b[10] = input("\nPlease enter the maximum value : ")
                    if int(det_a[10]) >= int(det_b[10]):
                        print("maximun value is less than minimum value, please enter valid input")
                        continue;
                    else:
                        break;
            elif detail_code == 12:
                while True:
                    print("\nPlease enter the Dividends_Rate Yield(배당 수익률) range. ")
                    det_a[11] = input("\nPlease enter the minimum value : ")
                    det_b[11] = input("\nPlease enter the maximum value : ")
                    if float(det_a[11]) >= float(det_b[11]):
                        print("maximun value is less than minimum value, please enter valid input")
                        continue;
                    else:
                        break;

            # 추가 필터 사용할 것인지 묻기
            detail_filter_check = input("\nDo you want to use another filter? (Y for Yes) : ")
            if detail_filter_check == 'Y':
                continue;
            else:
                break;
        # 필터 입력 종료
    else:
        print("\nDetailed filter is not used.\n")
    #세부 필터 종료


    # 지금까지 입력확인
    # print("\nperiod is %s\ttarget rate is %s\ttheme is %s\tcount is %s\tdetailed filter is %s\t" % (period, target_rate, theme_code,count, detail_filter))
    # print(det_a)
    # print(det_b)
    table_name = "date_" + today
    #mysql 연결
    conn = pymysql.connect(host="localhost", user = 'root', password='Axenon!0927', db = 'daily_stock',charset = 'utf8') 
    curs = conn.cursor(pymysql.cursors.DictCursor)

    #mysql table filtering
    if theme_exist == 'Y':
        sql = "SELECT %s FROM " + table_name + " WHERE Theme = " + theme_code
        if detail_filter == 'Y':
            if int(det_a[0]) != 0 or int(det_b[0]) != 0 :
                sql = sql + " AND 시가총액 BETWEEN '" + det_a[0] + "' AND '" + det_b[0] + "'"
            elif int(det_a[1]) != 0 or int(det_b[1]) != 0 :
                sql = sql + " AND PER BETWEEN '" + det_a[1] + "' AND '" + det_b[1] + "'"
            elif int(det_a[2]) != 0 or int(det_b[2]) != 0 :
                sql = sql + " AND EPS BETWEEN '" + det_a[2] + "' AND '" + det_b[2] + "'"
            elif int(det_a[3]) != 0 or int(det_b[3]) != 0 :
                sql = sql + " AND ROE BETWEEN '" + det_a[3] + "' AND '" + det_b[3] + "'"
            elif int(det_a[4]) != 0 or int(det_b[4]) != 0 :
                sql = sql + " AND PBR BETWEEN '" + det_a[4] + "' AND '" + det_b[4] + "'"
            elif int(det_a[5]) != 0 or int(det_b[5]) != 0 :
                sql = sql + " AND EV BETWEEN '" + det_a[5] + "' AND '" + det_b[5] + "'"
            elif int(det_a[6]) != 0 or int(det_b[6]) != 0 :
                sql = sql + " AND BPS BETWEEN '" + det_a[6] + "' AND '" + det_b[6] + "'"
            elif int(det_a[7]) != 0 or int(det_b[7]) != 0 :
                sql = sql + " AND 매출액 BETWEEN '" + det_a[7] + "' AND '" + det_b[7] + "'"
            elif int(det_a[8]) != 0 or int(det_b[8]) != 0 :
                sql = sql + " AND 영업이익 BETWEEN '" + det_a[8] + "' AND '" + det_b[8] + "'"
            elif int(det_a[9]) != 0 or int(det_b[9]) != 0 :
                sql = sql + " AND 당기순이익 BETWEEN '" + det_a[9] + "' AND '" + det_b[9] + "'"
            elif int(det_a[10]) != 0 or int(det_b[10]) != 0 :
                sql = sql + " AND Dividends BETWEEN '" + det_a[10] + "' AND '" + det_b[10] + "'"
            elif float(det_a[11]) != 0 or float(det_b[11]) != 0 :
                sql = sql + " AND Dividends_Rate BETWEEN '" + det_a[11] + "' AND '" + det_b[11] + "'"
        filter_sql = sql % print_sql_part
    else:
        if detail_filter == 'Y':
            sql = "SELECT %s FROM " + table_name + " WHERE "
            if int(det_a[0]) != 0 or int(det_b[0]) != 0 :
                sql = sql + "시가총액 BETWEEN '" + det_a[0] + "' AND '" + det_b[0] + "'"
            elif int(det_a[1]) != 0 or int(det_b[1]) != 0 :
                sql = sql + "PER BETWEEN '" + det_a[1] + "' AND '" + det_b[1] + "'"
            elif int(det_a[2]) != 0 or int(det_b[2]) != 0 :
                sql = sql + "EPS BETWEEN '" + det_a[2] + "' AND '" + det_b[2] + "'"
            elif int(det_a[3]) != 0 or int(det_b[3]) != 0 :
                sql = sql + "ROE BETWEEN '" + det_a[3] + "' AND '" + det_b[3] + "'"
            elif int(det_a[4]) != 0 or int(det_b[4]) != 0 :
                sql = sql + "PBR BETWEEN '" + det_a[4] + "' AND '" + det_b[4] + "'"
            elif int(det_a[5]) != 0 or int(det_b[5]) != 0 :
                sql = sql + "EV BETWEEN '" + det_a[5] + "' AND '" + det_b[5] + "'"
            elif int(det_a[6]) != 0 or int(det_b[6]) != 0 :
                sql = sql + "BPS BETWEEN '" + det_a[6] + "' AND '" + det_b[6] + "'"
            elif int(det_a[7]) != 0 or int(det_b[7]) != 0 :
                sql = sql + "매출액 BETWEEN '" + det_a[7] + "' AND '" + det_b[7] + "'"
            elif int(det_a[8]) != 0 or int(det_b[8]) != 0 :
                sql = sql + "영업이익 BETWEEN '" + det_a[8] + "' AND '" + det_b[8] + "'"
            elif int(det_a[9]) != 0 or int(det_b[9]) != 0 :
                sql = sql + "당기순이익 BETWEEN '" + det_a[9] + "' AND '" + det_b[9] + "'"
            elif int(det_a[10]) != 0 or int(det_b[10]) != 0 :
                sql = sql + "Dividends BETWEEN '" + det_a[10] + "' AND '" + det_b[10] + "'"
            elif float(det_a[11]) != 0 or float(det_b[11]) != 0 :
                sql = sql + "Dividends_Rate BETWEEN '" + det_a[11] + "' AND '" + det_b[11] + "'"
        filter_sql = sql % print_sql_part
    
    print(filter_sql)

    #정렬 결과 보기 while loop
    sort_sql = ""
    while True:
        print("\n")
        temp_sql = filter_sql + sort_sql
        curs.execute(temp_sql)
        rows = curs.fetchall()
        # 정렬 한 결과 프린트
        temp = count
        for index, value in enumerate(rows, start = 1):
            count = int(count) -1
            if count < 0 :
                break;
            print(index, value)
            print("\n")
        count = temp
        # 정렬 방식(시가총액, 매출액, 영업이익, 배당금, 배당수익률)
        sort_check = input("Would you like to sort out the data? (Y for yes) : ")
        sort_sql = ""
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
            print("\nAnalyzing these stocks...")
            break;

    # sql에서 종목코드만 추출
    code_list = []
    filter_sql = sql % "종목코드" + sort_sql 
    #print(filter_sql)
    curs.execute(filter_sql)
    results = curs.fetchall()
    temp = count
    for index, value in enumerate(results, start = 1):
        count = int(count) -1
        if count < 0 :
            break;
        code_temp = str(value)
        code_list.append(code_temp[10:16])
        print(index, value)
    count = temp
    # code list 추출 완료
    print(code_list)

    # DB 닫기
    conn.commit()
    conn.close()
    break;

print("program ends")

